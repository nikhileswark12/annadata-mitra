import os
import tensorflow as tf
from training.vision import config
import logging

logger = logging.getLogger(__name__)

def train_model(model, train_ds, val_ds, epochs=config.EPOCHS):
    """
    Executes the training loop with modern standard callbacks.
    """
    logger.info(f"Starting training for {epochs} epochs...")
    
    checkpoint_path = os.path.join(config.EXPORT_DIR, 'checkpoints', 'best_model.keras')
    os.makedirs(os.path.dirname(checkpoint_path), exist_ok=True)
    
    callbacks = [
        tf.keras.callbacks.ModelCheckpoint(
            filepath=checkpoint_path,
            save_best_only=True,
            monitor='val_accuracy',
            mode='max',
            verbose=1
        ),
        tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=config.PATIENCE_EARLY_STOP,
            restore_best_weights=True,
            verbose=1
        ),
        tf.keras.callbacks.ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.2,
            patience=config.PATIENCE_REDUCE_LR,
            min_lr=config.MIN_LR,
            verbose=1
        ),
        tf.keras.callbacks.TensorBoard(
            log_dir=os.path.join(config.EXPORT_DIR, 'logs'),
            histogram_freq=1
        )
    ]
    
    history = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=epochs,
        callbacks=callbacks
    )
    
    logger.info("Training complete.")
    return history
