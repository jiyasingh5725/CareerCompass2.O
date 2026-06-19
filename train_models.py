# train_salary_model.py
import os
import re
import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def train_final_stable_classifier():
    print("=========================================================")
    print("🎯 TRAINING BALANCED STRATIFIED SALARY CLASSIFIER")
    print("=========================================================\n")
    
    csv_filename = "cleaned_job_descriptions.csv" 
    if not os.path.exists(csv_filename):
        print(f"❌ ERROR: '{csv_filename}' not found! Run clean_and_visualize.py first.")
        return

    print("[1/3] Loading data and applying clean class balancing...")
    df = pd.read_csv(csv_filename)

    # 1. Standardize string categories and generate numeric class targets cleanly
    df['salary_bucket'] = df['salary_bucket'].astype(str).str.strip()
    df['salary_label'] = df['salary_bucket'].astype('category').cat.codes
    label_mapping = dict(enumerate(df['salary_bucket'].astype('category').cat.categories))
    
    # 2. Find the sizing threshold based on your smallest tier category
    unique_classes = df['salary_label'].value_counts()
    min_class_size = unique_classes.min()
    sample_size_per_class = min(min_class_size, 3000) 
    
    # 🌟 FIXED: Loop manually and combine with pd.concat to completely isolate columns from index shifts
    balanced_chunks = []
    for label in unique_classes.index:
        class_subset = df[df['salary_label'] == label]
        sampled_chunk = class_subset.sample(n=sample_size_per_class, random_state=42)
        balanced_chunks.append(sampled_chunk)
        
    df_balanced = pd.concat(balanced_chunks, ignore_index=True)
    print(f"• Found {len(unique_classes)} distinct salary tier brackets.")
    print(f"• Total balanced rows selected: {len(df_balanced):,} ({sample_size_per_class} rows per class)")

    # Feature Engineering
    qual_tier_map = {"b.tech": 1, "bachelor": 1, "b.com": 1, "ba": 1, "b.sc": 1, "m.tech": 2, "master": 2, "mba": 2, "phd": 3}
    df_balanced['edu_tier'] = df_balanced['Qualifications'].str.lower().map(qual_tier_map).fillna(1)
    df_balanced['text_features'] = df_balanced['cleaned_title'].fillna("") + " " + df_balanced['cleaned_skills'].fillna("")
    df_balanced['skill_count'] = df_balanced['cleaned_skills'].apply(lambda x: len(str(x).split()))
    
    if 'salary_midpoint' in df_balanced.columns:
        df_balanced['exp_years'] = df_balanced['salary_midpoint'].apply(lambda x: int(x % 10) if not pd.isna(x) else 0)
    else:
        df_balanced['exp_years'] = 3

    np.random.seed(42)
    df_balanced['projects_count'] = np.random.randint(1, 6, size=len(df_balanced))
    df_balanced['certifications_count'] = np.random.randint(0, 5, size=len(df_balanced))

    print("[2/3] Vectorizing keywords via TF-IDF...")
    salary_tfidf = TfidfVectorizer(max_features=400, stop_words='english', lowercase=True)
    X_text = salary_tfidf.fit_transform(df_balanced['text_features']).toarray()
    
    X_num = df_balanced[['skill_count', 'edu_tier', 'exp_years', 'projects_count', 'certifications_count']].values
    X = np.hstack((X_num, X_text))
    
    # Extract targets confidently from a guaranteed stable column array
    y = df_balanced['salary_label'].values

    # Stratified split to keep distribution clean
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    print("[3/3] Training Generalizing Random Forest Classifier...")
    salary_model = RandomForestClassifier(
        n_estimators=150,
        max_depth=12,
        min_samples_leaf=4,
        class_weight="balanced", 
        random_state=42,
        n_jobs=-1
    )
    salary_model.fit(X_train, y_train)
    
    print("\n=========================================================")
    print("📊 UNBIASED CLASSIFIER PERFORMANCE REPORT")
    print("=========================================================")
    train_acc = accuracy_score(y_train, salary_model.predict(X_train))
    test_acc = accuracy_score(y_test, salary_model.predict(X_test))
    
    print(f"• Balanced Training Set Accuracy: {train_acc:.2%}")
    print(f"• Balanced Testing Set Accuracy : {test_acc:.2%}")
    print("=========================================================\n")

    model_artifact = {
        "model": salary_model,
        "mapping": label_mapping
    }

    os.makedirs("models", exist_ok=True)
    joblib.dump(model_artifact, "models/salary_model.pkl")
    joblib.dump(salary_tfidf, "models/tfidf_vectorizer.pkl")
    print("✓ Success: Non-biased balanced artifacts serialized to models folder.")

if __name__ == "__main__":
    train_final_stable_classifier()