import tensorflow as tf
from training.vision.augmentations import get_data_augmentation
from training.vision import config

def build_model(num_classes):
    """
    Builds a robust, pure local CNN without any external pretrained weights.
    Uses standard Conv2D blocks with BatchNormalization, MaxPooling, and Dropout.
    """
    inputs = tf.keras.Input(shape=config.INPUT_SHAPE)
    
    # 1. Data Augmentation (active only during training)
    x = get_data_augmentation()(inputs)
    
    # 2. Custom CNN Blocks
    for filters in config.CNN_FILTERS:
        x = tf.keras.layers.Conv2D(filters, (3, 3), padding='same')(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Activation('relu')(x)
        x = tf.keras.layers.MaxPooling2D((2, 2))(x)
        
    # 3. Top Layers
    x = tf.keras.layers.GlobalAveragePooling2D()(x)
    x = tf.keras.layers.Dropout(config.DROPOUT_RATE)(x)
    
    # 4. Classification Layer
    outputs = tf.keras.layers.Dense(num_classes, activation='softmax', name='classification_head')(x)
    
    model = tf.keras.Model(inputs, outputs, name='Annadata_Local_Vision_Model')
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=config.INITIAL_LR),
        loss='categorical_crossentropy',
        metrics=['accuracy', tf.keras.metrics.TopKCategoricalAccuracy(k=3, name='top_3_accuracy')]
    )
    
    return model
