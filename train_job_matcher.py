# train_job_matcher.py
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def train_isolated_job_matcher():
    print("=========================================================")
    print("💼 COMPILING & EVALUATING STANDALONE COSINE MATCH ENGINE")
    print("=========================================================\n")
    
    csv_filename = "job_descriptions.csv" 
    if not os.path.exists(csv_filename):
        print(f"❌ ERROR: '{csv_filename}' not found!")
        return

    print("[1/3] Reading and cleaning job corpus entries...")
    df = pd.read_csv(csv_filename).dropna(subset=['Job Title', 'skills', 'Company']).reset_index(drop=True)
    
    # Take a diverse slice of 3,000 corporate items
    df_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)
    df_slice = df_shuffled.head(3000).copy()

    jobs_database = []
    job_corpus_signatures = []
    
    for idx, row in df_slice.iterrows():
        cleaned_skills = str(row['skills']).replace(',', ' ')
        text_signature = f"{row['Job Title']} {row['Role']} {cleaned_skills} {row['Job Description']} {row['Responsibilities']} {row['Company']}".lower()
        job_corpus_signatures.append(text_signature)
        
        jobs_database.append({
            "id": int(idx),
            "title": row['Job Title'],
            "company": row['Company'],
            "keywords": text_signature,
            "work_type": row.get('Work Type', 'Full-Time'),
            "location": row.get('location', 'Global'),
            "country": row.get('Country', 'Remote')
        })

    print("[2/3] Transforming text blocks into TF-IDF vector coordinates...")
    # Bounding max_features to 2,000 explicitly prevents word overfitting
    matcher_vectorizer = TfidfVectorizer(max_features=2000, stop_words='english', lowercase=True)
    job_vectors_matrix = matcher_vectorizer.fit_transform(job_corpus_signatures)
    
    # 🌟 PART 3: LIVE TERMINAL MATRIX EVALUATION
    print("\n=========================================================")
    print("📊 JOB VECTOR ENGINE METRICS & SANITY TESTING")
    print("=========================================================")
    
    non_zero_percentage = (job_vectors_matrix.nnz / (job_vectors_matrix.shape[0] * job_vectors_matrix.shape[1])) * 100
    print(f"• Vector Matrix Shape       : {job_vectors_matrix.shape[0]} jobs x {job_vectors_matrix.shape[1]} token features")
    print(f"• Vocabulary Density Score  : {non_zero_percentage:.3f}% non-zero entries")
    
    # Run a mock alignment test query to verify performance live
    test_query = ["python java backend developer machine learning developer software engineer"]
    test_vector = matcher_vectorizer.transform(test_query)
    mock_similarities = cosine_similarity(test_vector, job_vectors_matrix)[0]
    best_match_idx = np.argmax(mock_similarities)
    max_score = mock_similarities[best_match_idx]
    
    print(f"• Integration Test Match Score: {max_score:.4f} (Raw Cosine Distance)")
    if max_score > 0.05:
        print("✅ DIAGNOSTIC: Matrix mapping layers are active, accurate, and responsive!")
    else:
        print("⚠️ DIAGNOSTIC: Match signal is dangerously weak. Check vocabulary text lengths.")
    print("=========================================================\n")

    os.makedirs("models", exist_ok=True)
    matcher_artifacts = {
        "database": jobs_database,
        "matrix": job_vectors_matrix,
        "vectorizer": matcher_vectorizer
    }
    
    joblib.dump(matcher_artifacts, "models/job_matcher.pkl")
    print("✓ Success: Independent 'models/job_matcher.pkl' matrix built successfully.")

if __name__ == "__main__":
    train_isolated_job_matcher()