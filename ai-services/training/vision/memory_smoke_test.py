import os
import sys
import psutil
import tensorflow as tf
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / (1024 * 1024)

def run_smoke_test():
    # Set threading as in train.py
    tf.config.threading.set_inter_op_parallelism_threads(1)
    tf.config.threading.set_intra_op_parallelism_threads(2)
    
    logger.info(f"Initial Memory Usage: {get_memory_usage():.2f} MB")
    
    from training.vision import config
    from training.vision.dataset_loader import load_datasets
    from training.vision.model_builder import build_model
    
    logger.info("Loading Datasets...")
    train_ds, val_ds, test_ds, class_names = load_datasets()
    
    logger.info(f"Memory Usage after Dataset Load: {get_memory_usage():.2f} MB")
    
    logger.info("Building Model...")
    model = build_model(len(class_names))
    
    logger.info(f"Memory Usage after Model Build: {get_memory_usage():.2f} MB")
    
    logger.info(f"Batch Size from config: {config.BATCH_SIZE}")
    
    # Custom training loop for memory smoke test
    optimizer = tf.keras.optimizers.Adam(learning_rate=config.INITIAL_LR)
    loss_fn = tf.keras.losses.CategoricalCrossentropy()
    
    # Train for 10 batches
    logger.info("Processing 10 Training Batches...")
    train_iterator = iter(train_ds)
    peak_mem = get_memory_usage()
    
    try:
        for i in range(10):
            images, labels = next(train_iterator)
            
            with tf.GradientTape() as tape:
                predictions = model(images, training=True)
                loss = loss_fn(labels, predictions)
                
            gradients = tape.gradient(loss, model.trainable_variables)
            optimizer.apply_gradients(zip(gradients, model.trainable_variables))
            
            current_mem = get_memory_usage()
            if current_mem > peak_mem:
                peak_mem = current_mem
                
            logger.info(f"Train Batch {i+1}/10 Complete - Current Mem: {current_mem:.2f} MB")
    except Exception as e:
        logger.error(f"Error during training batches: {e}")
        return False
        
    # Validation for 3 batches
    logger.info("Processing 3 Validation Batches...")
    val_iterator = iter(val_ds)
    
    try:
        for i in range(3):
            images, labels = next(val_iterator)
            predictions = model(images, training=False)
            
            current_mem = get_memory_usage()
            if current_mem > peak_mem:
                peak_mem = current_mem
                
            logger.info(f"Validation Batch {i+1}/3 Complete - Current Mem: {current_mem:.2f} MB")
    except Exception as e:
        logger.error(f"Error during validation batches: {e}")
        return False
        
    logger.info(f"Peak Memory Usage During Test: {peak_mem:.2f} MB")
    logger.info("Memory Smoke Test SUCCESS - No RESOURCE_EXHAUSTED errors encountered.")
    return True

if __name__ == "__main__":
    success = run_smoke_test()
    if not success:
        sys.exit(1)
