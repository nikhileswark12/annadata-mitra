import tensorflow as tf

def get_data_augmentation():
    """
    Returns a keras Sequential model containing standard image augmentations.
    This should only be applied during training.
    """
    return tf.keras.Sequential([
        tf.keras.layers.RandomFlip("horizontal_and_vertical"),
        tf.keras.layers.RandomRotation(0.2),
        tf.keras.layers.RandomZoom(0.2),
        tf.keras.layers.RandomContrast(0.2),
        tf.keras.layers.RandomBrightness(0.2),
    ], name="data_augmentation")
