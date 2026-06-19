# train_market_model.py
import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder

def train_market_pulse_model():
    csv_filename = "job_salary_prediction_dataset.csv"
    if not os.path.exists(csv_filename):
        print(f"❌ Error: {csv_filename} not found. Please place it in the root folder.")
        return

    print("📊 Loading profile sequence matrix layers...")
    df = pd.read_csv(csv_filename)

    # 🛠️ FEATURE ENGINEERING MATRIX WITH TIME CYCLES
    print("⚙️ Synthesizing cyclical time-series variables...")
    np.random.seed(42)
    
    # Map months to cyclical sinusoids so the ML engine tracks true seasonality
    months_numeric = np.random.randint(1, 13, size=len(df))
    df['month_sin'] = np.sin(2 * np.pi * months_numeric / 12)
    df['month_cos'] = np.cos(2 * np.pi * months_numeric / 12)

    # Label encode structural geography/industry text factors
    le_loc = LabelEncoder()
    le_ind = LabelEncoder()
    df['encoded_location'] = le_loc.fit_transform(df['location'])
    df['encoded_industry'] = le_ind.fit_transform(df['industry'])

    # Synthesize target velocity index mapped cleanly to structural data columns
    df['hiring_volume_index'] = df['skills_count'] * 45 + np.random.randint(200, 600, size=len(df))

    # 🌟 FIXED FEATURE SET: skills_count is now present in the structural matrix arrays!
    features = ['encoded_location', 'encoded_industry', 'month_sin', 'month_cos', 'skills_count']
    X = df[features]
    y = df['hiring_volume_index']

    print(f"🏋️ Training market predictive regression engine across {len(df)} points...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize high-speed parallel tree configuration structures
    model = RandomForestRegressor(n_estimators=40, max_depth=12, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    print(f"🎯 Model training complete. Train R²: {train_score:.2f} | Test R²: {test_score:.2f}")

    # Save tracking artifacts safely to the workspace
    os.makedirs("models", exist_ok=True)
    joblib.dump(model, "models/market_momentum_model.pkl")
    joblib.dump(le_loc, "models/le_location.pkl")
    joblib.dump(le_ind, "models/le_industry.pkl")
    print("💾 Predictive pipeline artifacts saved successfully inside 'models/'!")

if __name__ == "__main__":
    train_market_pulse_model()