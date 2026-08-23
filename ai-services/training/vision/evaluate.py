import os
import json
import numpy as np
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import pandas as pd
from training.vision import config
import logging

logger = logging.getLogger(__name__)

def evaluate_model(model, test_ds, class_names):
    """
    Evaluates the model on the test dataset and calculates comprehensive metrics.
    """
    logger.info("Evaluating model on test dataset...")
    
    # Run evaluation natively in TF
    loss, accuracy, top3_acc = model.evaluate(test_ds, verbose=1)
    
    # Collect predictions and true labels for sklearn metrics
    y_true = []
    y_pred = []
    
    for images, labels in test_ds:
        preds = model.predict(images, verbose=0)
        y_true.extend(np.argmax(labels.numpy(), axis=1))
        y_pred.extend(np.argmax(preds, axis=1))
        
    y_true = np.array(y_true)
    y_pred = np.array(y_pred)
    
    # Calculate classification report
    report = classification_report(
        y_true, 
        y_pred, 
        labels=np.arange(len(class_names)), 
        target_names=class_names, 
        output_dict=True,
        zero_division=0
    )
    
    metrics = {
        "test_loss": float(loss),
        "test_accuracy": float(accuracy),
        "test_top3_accuracy": float(top3_acc),
        "weighted_precision": report["weighted avg"]["precision"],
        "weighted_recall": report["weighted avg"]["recall"],
        "weighted_f1_score": report["weighted avg"]["f1-score"],
        "macro_precision": report["macro avg"]["precision"],
        "macro_recall": report["macro avg"]["recall"],
        "macro_f1_score": report["macro avg"]["f1-score"],
        "per_class_metrics": {
            cls: {
                "precision": report[cls]["precision"],
                "recall": report[cls]["recall"],
                "f1_score": report[cls]["f1-score"],
                "support": report[cls]["support"]
            } for cls in class_names
        }
    }
    
    # Generate Confusion Matrix
    cm = confusion_matrix(y_true, y_pred, labels=np.arange(len(class_names)))
    cm_df = pd.DataFrame(cm, index=class_names, columns=class_names)
    
    # Save files
    os.makedirs(config.EXPORT_DIR, exist_ok=True)
    
    metrics_path = os.path.join(config.EXPORT_DIR, config.METRICS_FILE)
    with open(metrics_path, 'w') as f:
        json.dump(metrics, f, indent=4)
        
    cm_path = os.path.join(config.EXPORT_DIR, config.CONFUSION_MATRIX_FILE)
    cm_df.to_csv(cm_path)
    
    report_path = os.path.join(config.EXPORT_DIR, 'classification_report.json')
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=4)
    
    logger.info(f"Evaluation complete. Metrics saved to {metrics_path}")
    
    return metrics, cm_df
