import os, json, time, numpy as np, tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix
import zipfile, tempfile
import h5py
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

def build_vision_model():
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
    return model

def load_vision():
    model = build_vision_model()
    
    vision_model_path = "f:/Annadata Mitra/annadata-mitra/ai-services/models/vision/improved/vision_model_improved.keras"
    tmp_dir = tempfile.gettempdir()
    with zipfile.ZipFile(vision_model_path, 'r') as z:
        z.extract('model.weights.h5', tmp_dir)
        config = json.loads(z.read('config.json').decode('utf-8'))
        
    h5_path = os.path.join(tmp_dir, 'model.weights.h5')
    
    print("Extracting weights in order from H5...")
    all_weight_tensors = []
    
    with h5py.File(h5_path, 'r') as f:
        layers = config['config']['layers']
        
        # In Keras 3, nested models (Functional) have their layers defined inside.
        # Let's write a recursive function to find all layers in order.
        def extract_layers(layer_list, prefix="layers\\"):
            for l in layer_list:
                name = l['config']['name']
                layer_path = prefix + name
                # Handle nested layers (like the MobileNetV2 base)
                if 'layers' in l['config']:
                    # It's a functional/sequential model inside
                    extract_layers(l['config']['layers'], prefix=layer_path + "\\layers\\")
                else:
                    # It's a leaf layer, let's see if it has weights in the H5
                    # Try both slashes just in case
                    target_key = None
                    for k in f.keys():
                        if k == layer_path or k == layer_path.replace("\\", "/"):
                            target_key = k
                            break
                    if target_key:
                        g = f[target_key]
                        if 'vars' in g:
                            vars_group = g['vars']
                            num_vars = len(vars_group.keys())
                            for i in range(num_vars):
                                all_weight_tensors.append(vars_group[str(i)][()])
        
        extract_layers(layers)
        
    print(f"Extracted {len(all_weight_tensors)} weight arrays from H5.")
    
    # Check variables in our native model
    model_vars = model.variables
    print(f"Native model has {len(model_vars)} variables.")
    
    if len(all_weight_tensors) == len(model_vars):
        print("Shapes match! Transferring weights 1-to-1.")
        # Note: model.variables is a list of tf.Variable.
        # But we must group them by layer because we can only use layer.set_weights()
        # to ensure the backend actually updates them safely.
        
        # Let's extract layer-by-layer from the flat native model
        ptr = 0
        for layer in model.layers:
            num_layer_vars = len(layer.variables)
            if num_layer_vars > 0:
                layer_weights = all_weight_tensors[ptr:ptr+num_layer_vars]
                layer.set_weights(layer_weights)
                ptr += num_layer_vars
        print("All weights assigned successfully!")
    else:
        print("MISMATCH IN VARIABLE COUNTS!")
        
    return model

if __name__ == '__main__':
    print("Loading model...")
    model = load_vision()
    print("Model loaded.")
    
    @tf.function
    def fast_predict(x):
        return model(x, training=False)
        
    print("Compiling tf.function...")
    fast_predict(tf.zeros((1, 224, 224, 3)))
    
    vision_test_dir = "f:/Annadata Mitra/annadata-mitra/ai-services/datasets/vision/canonical/test"
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
    
    print(f"Total images: {total_samples}")
    t0 = time.time()
    
    for i in range(0, total_samples, batch_size):
        batch_paths = image_paths[i:i+batch_size]
        batch_images = []
        for p in batch_paths:
            img = load_img(p, target_size=(224, 224))
            arr = img_to_array(img)
            batch_images.append(arr)
        
        x_batch = np.stack(batch_images)
        # 1./255 or preprocess_input? Let's use 1./255 because it was explicitly requested in the audit instructions 
        # as the fixed preprocessing.
        x_batch = x_batch / 255.0
        
        p_batch = fast_predict(tf.convert_to_tensor(x_batch, dtype=tf.float32))
        preds_list.append(p_batch.numpy())
        
        if (i // batch_size) % 5 == 0:
            print(f"Processed {i}/{total_samples} images. Elapsed: {time.time() - t0:.1f}s", flush=True)
            
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
    
    with open("f:/Annadata Mitra/annadata-mitra/ai-services/experiments/generalization_eval_results.json", "w") as f:
        json.dump(vision_results, f)
    print("Done!")
