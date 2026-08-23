import logging
import os
import json
import numpy as np

try:
    import tensorflow as tf
except ImportError:
    logging.info("Tensorflow not found. Please run: pip install tensorflow")
    exit(1)

def train_dummy_vision_model():
    logging.info("Generating dummy vision model...")
    
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(224, 224, 3),
        include_top=False,
        weights='imagenet'
    )
    base_model.trainable = False
    
    model = tf.keras.Sequential([
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(256, activation='relu'),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(10, activation='softmax') # 10 classes
    ])
    
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    # Save model
    model_dir = os.path.join(os.path.dirname(__file__), '../models')
    os.makedirs(model_dir, exist_ok=True)
    
    model_path = os.path.join(model_dir, 'vision_model.h5')
    
    # This will save a model with untrained weights in the dense layers,
    # which is fine for our placeholder/MVP requirement.
    model.save(model_path)
    logging.info(f"Dummy model saved to {model_path}")
    
    # Generate and save class names
    class_names = [
        "early_blight", "late_blight", "powdery_mildew", "leaf_rust", 
        "bacterial_wilt", "yellow_mosaic", "downy_mildew", "anthracnose", 
        "leaf_curl", "healthy"
    ]
    
    class_names_path = os.path.join(model_dir, 'class_names.json')
    with open(class_names_path, 'w') as f:
        json.dump(class_names, f, indent=4)
        
    logging.info(f"Class names saved to {class_names_path}")

if __name__ == '__main__':
    train_dummy_vision_model()
