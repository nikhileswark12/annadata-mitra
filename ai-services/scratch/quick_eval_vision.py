import os, json, time, numpy as np, tensorflow as tf
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report, confusion_matrix
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import zipfile, tempfile

def load_vision():
    vision_model_path = "f:/Annadata Mitra/annadata-mitra/ai-services/models/vision/improved/vision_model_improved.keras"
    with zipfile.ZipFile(vision_model_path, 'r') as z:
        config = json.loads(z.read('config.json').decode('utf-8'))
        config['module'] = "keras.src.models.functional"
        if 'compile_config' in config:
            del config['compile_config']
        layers = config['config']['layers']
        layers_to_remove = ['data_augmentation', 'tf.math.truediv', 'tf.math.subtract']
        new_layers = [l for l in layers if l['config']['name'] not in layers_to_remove]
        for l in new_layers:
            if 'inbound_nodes' in l and l['inbound_nodes']:
                nodes = l['inbound_nodes'][0]
                if nodes and isinstance(nodes[0], str):
                    if nodes[0] in layers_to_remove:
                        nodes[0] = 'input_1'
                        nodes[1] = 0
                else:
                    for node in nodes:
                        if isinstance(node, list) and len(node) > 0 and node[0] in layers_to_remove:
                            node[0] = 'input_1'
                            node[1] = 0
        config['config']['layers'] = new_layers
        
        def fix_keras3_compat(obj):
            if isinstance(obj, dict):
                class_name = obj.get('class_name')
                if class_name == 'BatchNormalization':
                    if 'config' in obj and 'axis' in obj['config']:
                        if isinstance(obj['config']['axis'], list):
                            obj['config']['axis'] = obj['config']['axis'][0]
                if class_name == 'DepthwiseConv2D':
                    if 'config' in obj and 'groups' in obj['config']:
                        del obj['config']['groups']
                for v in obj.values():
                    fix_keras3_compat(v)
            elif isinstance(obj, list):
                for item in obj:
                    fix_keras3_compat(item)
                    
        config_str = json.dumps(config).replace('keras.src.engine.functional', 'keras.src.models.functional')
        config = json.loads(config_str)
        fix_keras3_compat(config)
        
        from tensorflow.keras.models import model_from_json
        vision_model = model_from_json(json.dumps(config))
        tmp_dir = tempfile.gettempdir()
        z.extract('model.weights.h5', tmp_dir)
        h5_path = os.path.join(tmp_dir, 'model.weights.h5')
        legacy_path = os.path.join(tmp_dir, 'legacy_weights2.h5')
        if os.path.exists(legacy_path):
            os.remove(legacy_path)
        os.rename(h5_path, legacy_path)
        vision_model.load_weights(legacy_path, by_name=True)
    return vision_model

if __name__ == '__main__':
    from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
    print("Loading model...")
    model = load_vision()
    print("Model loaded. Initializing datagen...")
    vision_test_dir = "f:/Annadata Mitra/annadata-mitra/ai-services/datasets/vision/canonical/test"
    datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
    test_generator = datagen.flow_from_directory(
        vision_test_dir,
        target_size=(224, 224),
        batch_size=256,
        class_mode='categorical',
        shuffle=False
    )
    print("Evaluating...")
    t0 = time.time()
    preds = model.predict(test_generator, steps=len(test_generator), verbose=2)
    vision_inf_time = time.time() - t0
    print("Evaluation finished in", vision_inf_time)
    
    y_pred = np.argmax(preds, axis=1)
    y_true = test_generator.classes
    class_labels = list(test_generator.class_indices.keys())
    
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
        "Test_Samples": test_generator.samples
    }
    
    with open("f:/Annadata Mitra/annadata-mitra/ai-services/experiments/vision_results_temp.json", "w") as f:
        json.dump(vision_results, f)
    print("Done!")
