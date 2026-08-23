import tensorflow as tf
from training.vision import config

def load_datasets():
    """
    Loads train, validation, and test datasets using tf.keras.utils.image_dataset_from_directory.
    Applies performance optimizations like caching and prefetching.
    """
    AUTOTUNE = tf.data.AUTOTUNE
    
    # Load raw datasets
    train_ds = tf.keras.utils.image_dataset_from_directory(
        config.TRAIN_DIR,
        image_size=config.IMAGE_SIZE,
        batch_size=config.BATCH_SIZE,
        shuffle=True,
        label_mode='categorical'
    )
    
    val_ds = tf.keras.utils.image_dataset_from_directory(
        config.VAL_DIR,
        image_size=config.IMAGE_SIZE,
        batch_size=config.BATCH_SIZE,
        shuffle=False,
        label_mode='categorical'
    )
    
    test_ds = tf.keras.utils.image_dataset_from_directory(
        config.TEST_DIR,
        image_size=config.IMAGE_SIZE,
        batch_size=config.BATCH_SIZE,
        shuffle=False,
        label_mode='categorical'
    )
    
    # Extract class names mapping
    class_names = train_ds.class_names
    
    # Normalization layer (Scale images to [0, 1])
    normalization_layer = tf.keras.layers.Rescaling(1./255)
    
    # Optimize datasets
    train_ds = train_ds.map(lambda x, y: (normalization_layer(x), y), num_parallel_calls=AUTOTUNE)
    train_ds = train_ds.prefetch(buffer_size=1)
    
    val_ds = val_ds.map(lambda x, y: (normalization_layer(x), y), num_parallel_calls=AUTOTUNE)
    val_ds = val_ds.prefetch(buffer_size=1)
    
    test_ds = test_ds.map(lambda x, y: (normalization_layer(x), y), num_parallel_calls=AUTOTUNE)
    test_ds = test_ds.prefetch(buffer_size=1)
    
    return train_ds, val_ds, test_ds, class_names
