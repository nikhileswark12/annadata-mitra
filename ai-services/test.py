import tensorflow as tf

class FixedBatchNormalization(tf.keras.layers.BatchNormalization):
    def __init__(self, **kwargs):
        if 'axis' in kwargs and isinstance(kwargs['axis'], list):
            kwargs['axis'] = kwargs['axis'][0]
        super().__init__(**kwargs)

tf.keras.utils.get_custom_objects().update({'BatchNormalization': FixedBatchNormalization})
tf.keras.models.load_model('f:/Annadata Mitra/annadata-mitra/ai-services/models/vision/vision_model.keras')
print("Model loaded successfully!")
