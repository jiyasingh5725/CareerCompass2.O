# train_predictor_model.py
import os
import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error

def train_advanced_predictor_engine():
    print("=========================================================")
    print("🚀 TRAINING HIGH-PRECISION CORE PREDICTOR REGRESSOR")
    print("=========================================================\n")
    
    csv_filename = "job_salary_prediction_dataset.csv"
    if not os.path.exists(csv_filename):
        print(f"❌ ERROR: '{csv_filename}' not found in current workspace directory.")
        return

    print("[1/3] Loading dataset and performing categorical mapping...")
    df = pd.read_csv(csv_filename)
    
    cat_cols = ['job_title', 'education_level', 'industry', 'company_size', 'location', 'remote_work']
    mappings = {}
    df_encoded = df.copy()

    # Convert string object categories into clean, reproducible codes
    for col in cat_cols:
        df_encoded[col] = df_encoded[col].astype(str).str.strip()
        df_encoded[col] = df_encoded[col].astype('category')
        mappings[col] = list(df_encoded[col].cat.categories)
        df_encoded[col] = df_encoded[col].cat.codes

    # Ensure precise matching feature layout sequence
    X = df_encoded.drop(columns=['salary'])
    y = df_encoded['salary']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

    print("[2/3] Fitting Gradient Boosting Regressor (250,000 matrix elements)...")
    model = GradientBoostingRegressor(
        n_estimators=100, 
        max_depth=6, 
        random_state=42
    )
    model.fit(X_train, y_train)

    print("\n=========================================================")
    print("📊 REGRESSION ENGINE VALIDATION METRICS REPORT")
    print("=========================================================")
    preds = model.predict(X_test)
    print(f"• Model Coefficient of Determination (R² Score): {r2_score(y_test, preds):.2%}")
    print(f"• Mean Absolute Error (MAE Deviation Grid)      : ${mean_absolute_error(y_test, preds):,.2f}")
    print("=========================================================\n")

    # Serialize complete bundle with lookups inside
    artifact = {
        "model": model,
        "mappings": mappings,
        "features": list(X.columns)
    }

    os.makedirs("models", exist_ok=True)
    joblib.dump(artifact, "models/new_predictor_model.pkl")
    print("✓ Success: New high-precision predictor artifact saved to 'models/new_predictor_model.pkl'")

if __name__ == "__main__":
    train_advanced_predictor_engine()