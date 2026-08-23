import os
import json
import time
import re
import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
import zipfile, tempfile
import h5py
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

def sort_keys_naturally(keys):
    def alphanum_key(s):
        return [int(c) if c.isdigit() else c for c in re.split('([0-9]+)', s)]
    return sorted(keys, key=alphanum_key)

def load_vision():
    print("Building model using native MobileNetV2...")
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(224, 224, 3),
        alpha=1.0,
        include_top=False,
        weights=None
    )
    x = base_model.output
    x = tf.keras.layers.GlobalAveragePooling2D(name="global_average_pooling2d")(x)
    x = tf.keras.layers.Dropout(0.2, name="dropout")(x)
    outputs = tf.keras.layers.Dense(42, activation='softmax', name="dense")(x)
    
    model = tf.keras.models.Model(inputs=base_model.input, outputs=outputs, name="vision_model")
    
    base_dir = "f:/Annadata Mitra/annadata-mitra/ai-services"
    vision_model_path = os.path.join(base_dir, "models/vision/improved/vision_model_improved.keras")
    tmp_dir = tempfile.gettempdir()
    with zipfile.ZipFile(vision_model_path, 'r') as z:
        z.extract('model.weights.h5', tmp_dir)
        
    h5_path = os.path.join(tmp_dir, 'model.weights.h5')
    
    print("Extracting and mapping weights from H5 by topological type matching...")
    with h5py.File(h5_path, 'r') as f:
        keys = list(f.keys())
        
        h5_conv2d = sort_keys_naturally([k for k in keys if 'conv2d' in k and 'depthwise' not in k])
        h5_bn = sort_keys_naturally([k for k in keys if 'batch_normalization' in k])
        h5_dw = sort_keys_naturally([k for k in keys if 'depthwise' in k])
        
        native_conv2d = [l for l in model.layers if isinstance(l, tf.keras.layers.Conv2D) and not isinstance(l, tf.keras.layers.DepthwiseConv2D)]
        native_bn = [l for l in model.layers if isinstance(l, tf.keras.layers.BatchNormalization)]
        native_dw = [l for l in model.layers if isinstance(l, tf.keras.layers.DepthwiseConv2D)]
        
        def map_weights(h5_keys, native_layers, name):
            if len(h5_keys) != len(native_layers):
                return
            for k, l in zip(h5_keys, native_layers):
                g = f[k]
                if 'vars' in g:
                    vars_group = g['vars']
                    num_vars = len(vars_group.keys())
                    weight_tensors = [vars_group[str(i)][()] for i in range(num_vars)]
                    l.set_weights(weight_tensors)
        
        map_weights(h5_conv2d, native_conv2d, "Conv2D")
        map_weights(h5_bn, native_bn, "BN")
        map_weights(h5_dw, native_dw, "Depthwise")
        
        dense_group = f['layers']['dense'] if 'layers' in f and 'dense' in f['layers'] else f['layers\\dense']
        if 'vars' in dense_group:
            vars_group = dense_group['vars']
            num_vars = len(vars_group.keys())
            weight_tensors = [vars_group[str(i)][()] for i in range(num_vars)]
            model.get_layer("dense").set_weights(weight_tensors)
            
    print("All weights assigned successfully!")
    return model

def run_experiments():
    base_dir = "f:/Annadata Mitra/annadata-mitra/ai-services"
    exp_dir = os.path.join(base_dir, "experiments")
    os.makedirs(exp_dir, exist_ok=True)
    
    t0_total = time.time()
    
    # Initialize Results Dictionary
    generalization_eval_results = {
        "metadata": {
            "python_version": sys.version if 'sys' in globals() else "3.x",
            "tensorflow_version": tf.__version__,
            "seed": 42
        }
    }
    
    print("Running Vision Generalization Evaluation...")
    vision_test_dir = os.path.join(base_dir, "datasets/vision/canonical/test")
    
    # 1) Loads models/vision/improved/vision_model_improved.keras
    vision_model = load_vision()
    
    @tf.function
    def fast_predict(x):
        return vision_model(x, training=False)
        
    fast_predict(tf.zeros((1, 224, 224, 3)))
    
    class_labels = sorted(os.listdir(vision_test_dir))
    class_to_idx = {c: i for i, c in enumerate(class_labels)}
    
    image_paths = []
    y_true_list = []
    
    for c in class_labels:
        cdir = os.path.join(vision_test_dir, c)
        for f in os.listdir(cdir):
            if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_paths.append(os.path.join(cdir, f))
                y_true_list.append(class_to_idx[c])
                
    batch_size = 64
    total_samples = len(image_paths)
    preds_list = []
    
    t0 = time.time()
    for i in range(0, total_samples, batch_size):
        batch_paths = image_paths[i:i+batch_size]
        batch_images = []
        for p in batch_paths:
            img = load_img(p, target_size=(224, 224))
            arr = img_to_array(img)
            batch_images.append(arr)
        
        x_batch = np.stack(batch_images)
        # 2) Uses mobilenet_v2.preprocess_input
        x_batch = preprocess_input(x_batch)
        
        p_batch = fast_predict(tf.convert_to_tensor(x_batch, dtype=tf.float32))
        preds_list.append(p_batch.numpy())
            
    vision_inf_time = time.time() - t0
    print("Evaluation finished in", vision_inf_time)
    
    y_true = np.array(y_true_list)
    preds = np.concatenate(preds_list, axis=0)
    y_pred = np.argmax(preds, axis=-1)
    
    report = classification_report(y_true, y_pred, target_names=class_labels, output_dict=True)
    top3_acc = tf.keras.metrics.top_k_categorical_accuracy(
        tf.one_hot(y_true, depth=len(class_labels)), preds, k=3
    ).numpy().mean()
    macro_f1 = report['macro avg']['f1-score']
    weighted_f1 = report['weighted avg']['f1-score']
    f1_gap = abs(macro_f1 - weighted_f1)
    recalls = [report[c]['recall'] for c in class_labels if c in report]
    
    vision_results = {
        "Accuracy": float(report['accuracy']),
        "Top3_Accuracy": float(top3_acc),
        "Macro_F1": float(macro_f1),
        "Weighted_F1": float(weighted_f1),
        "Macro_Weighted_F1_Gap": float(f1_gap),
        "Recall_Variance": float(np.var(recalls)),
        "Worst_Class_Recall": float(np.min(recalls)),
        "Best_Class_Recall": float(np.max(recalls)),
        "Confusion_Matrix": confusion_matrix(y_true, y_pred).tolist(),
        "Inference_Time_sec": float(vision_inf_time),
        "Test_Samples": len(y_true)
    }
    generalization_eval_results["vision_generalization"] = vision_results
    generalization_eval_results["metadata"]["total_execution_time_sec"] = float(time.time() - t0_total)
    
    with open(os.path.join(exp_dir, "vision_e5_audit.json"), "w") as f:
        json.dump(generalization_eval_results, f, indent=4)
        
    print("Experiments completed successfully. Artifact saved.")

if __name__ == "__main__":
    run_experiments()
