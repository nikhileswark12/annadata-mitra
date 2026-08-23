import logging
import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

def generate_synthetic_data(num_samples=2200):
    np.random.seed(42)
    crops = [
        'rice', 'maize', 'chickpea', 'kidneybeans', 'pigeonpeas',
        'mothbeans', 'mungbean', 'blackgram', 'lentil', 'pomegranate',
        'banana', 'mango', 'grapes', 'watermelon', 'muskmelon', 'apple',
        'orange', 'papaya', 'coconut', 'cotton', 'jute', 'coffee'
    ]
    
    data = []
    for _ in range(num_samples):
        crop = np.random.choice(crops)
        # Generating plausible random values
        n = np.random.uniform(0, 140)
        p = np.random.uniform(5, 145)
        k = np.random.uniform(5, 205)
        temperature = np.random.uniform(8, 43)
        humidity = np.random.uniform(14, 100)
        ph = np.random.uniform(3.5, 9.9)
        rainfall = np.random.uniform(20, 298)
        
        data.append([n, p, k, temperature, humidity, ph, rainfall, crop])
        
    df = pd.DataFrame(data, columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall', 'label'])
    return df

def train_model():
    logging.info("Generating synthetic dataset...")
    df = generate_synthetic_data()
    
    # Save dataset
    dataset_dir = os.path.join(os.path.dirname(__file__), '../datasets')
    os.makedirs(dataset_dir, exist_ok=True)
    df.to_csv(os.path.join(dataset_dir, 'synthetic_crop_data.csv'), index=False)
    
    X = df.drop('label', axis=1)
    y = df['label']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    logging.info("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)
    
    y_pred = model.predict(X_test_scaled)
    acc = accuracy_score(y_test, y_pred)
    logging.info(f"Model Accuracy (Synthetic Data): {acc * 100:.2f}%")
    
    # Save model and scaler
    model_dir = os.path.join(os.path.dirname(__file__), '../models')
    os.makedirs(model_dir, exist_ok=True)
    
    model_path = os.path.join(model_dir, 'crop_model.pkl')
    scaler_path = os.path.join(model_dir, 'crop_scaler.pkl')
    
    joblib.dump(model, model_path)
    joblib.dump(scaler, scaler_path)
    logging.info(f"Model saved to {model_path}")
    logging.info(f"Scaler saved to {scaler_path}")

if __name__ == '__main__':
    train_model()
