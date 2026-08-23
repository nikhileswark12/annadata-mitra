import tensorflow as tf

class DummyLayer(tf.keras.layers.Layer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    def call(self, inputs):
        return inputs

try:
    model = tf.keras.models.load_model(
        'f:/Annadata Mitra/annadata-mitra/ai-services/models/vision/improved/vision_model_improved.keras',
        compile=False,
        custom_objects={'data_augmentation': DummyLayer, 'Sequential': tf.keras.Sequential}
    )
    print("SUCCESS")
    model.summary()
except Exception as e:
    import traceback
    traceback.print_exc()
