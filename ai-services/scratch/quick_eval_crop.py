import os, json, time, joblib, pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, confusion_matrix
from sklearn.preprocessing import StandardScaler

def run_crop():
    base_dir = "f:/Annadata Mitra/annadata-mitra/ai-services"
    test_df = pd.read_csv(os.path.join(base_dir, "datasets/crop/splits/test.csv"))
    X_test, y_test = test_df.drop('label', axis=1), test_df['label']
    
    train_df = pd.read_csv(os.path.join(base_dir, "datasets/crop/splits/train.csv"))
    scaler = StandardScaler()
    scaler.fit(train_df.drop('label', axis=1))
    X_test_scaled = scaler.transform(X_test)
    
    crop_model_path = os.path.join(base_dir, "models/crop/baseline/crop_model_baseline.pkl")
    frozen_rf = joblib.load(crop_model_path)
    
    for estimator in frozen_rf.estimators_:
        if not hasattr(estimator, 'monotonic_cst'):
            estimator.monotonic_cst = None
            
    t0 = time.time()
    crop_preds = frozen_rf.predict(X_test_scaled)
    crop_inf_time = time.time() - t0
    
    crop_results = {
        "Accuracy": float(accuracy_score(y_test, crop_preds)),
        "Precision_Macro": float(precision_score(y_test, crop_preds, average="macro")),
        "Recall_Macro": float(recall_score(y_test, crop_preds, average="macro")),
        "Macro_F1": float(f1_score(y_test, crop_preds, average="macro")),
        "Weighted_F1": float(f1_score(y_test, crop_preds, average="weighted")),
        "Confusion_Matrix": confusion_matrix(y_test, crop_preds).tolist(),
        "Inference_Time_sec": float(crop_inf_time),
        "Test_Samples": len(y_test)
    }
    with open(os.path.join(base_dir, "experiments/crop_results_temp.json"), "w") as f:
        json.dump(crop_results, f)
    print("Crop Eval Done!")

if __name__ == '__main__':
    run_crop()
