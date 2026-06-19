# verify_predictions.py
import joblib
import numpy as np
import os

def test_model_intelligence():
    print("=========================================================")
    # Visual check to ensure the model can dynamically jump between classes
    print("🧪 CAREERCOMPASS INTERACTIVE INFRASTRUCTURE TEST SUITE")
    print("=========================================================\n")
    
    model_path = "models/salary_model.pkl"
    vectorizer_path = "models/tfidf_vectorizer.pkl"
    
    if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
        print("❌ ERROR: Model files missing! Run train_salary_model.py first.")
        return
        
    # Load serialized artifacts
    artifact = joblib.load(model_path)
    salary_classifier = artifact["model"]
    label_mapping = artifact["mapping"]
    tfidf_vectorizer = joblib.load(vectorizer_path)

    # Define 3 highly distinct mock test profiles
    test_cases = {
        "1. Entry-Level Student Profile": {
            "text": "student fresher entry level html css basic documentation microsoft word intern",
            "num": [2, 1, 0, 1, 0] # low skills, low edu tier, 0 exp, 1 project, 0 certs
        },
        "2. Mid-Level Web Developer": {
            "text": "software web developer java javascript spring boot SQL git backend developer",
            "num": [6, 1, 3, 3, 1] # mid skills, mid edu tier, 3 exp, 3 projects, 1 cert
        },
        "3. Premium Cloud Solutions Architect": {
            "text": "senior solutions architect aws cloud kubernetes docker devops manager python microservices",
            "num": [10, 2, 8, 5, 4] # high skills, high edu tier, 8 exp, 5 projects, 4 certs
        }
    }

    print("🔄 Running real-time mock evaluation loops...\n")
    
    for profile_name, data in test_cases.items():
        # Clean array structuring to mimic live backend pipelines
        numerical_matrix = np.array([data["num"]])
        skills_vectorized = tfidf_vectorizer.transform([data["text"]]).toarray()
        X_input = np.hstack((numerical_matrix, skills_vectorized))
        
        # Predict class
        predicted_class_code = salary_classifier.predict(X_input)[0]
        predicted_range_string = label_mapping[predicted_class_code]
        
        print(f"📋 Profile: {profile_name}")
        print(f"   ↳ Key Words: \"{data['text'][:60]}...\"")
        print(f"   💰 Predicted Bracket: {predicted_range_string}")
        print("-" * 57)

if __name__ == "__main__":
    test_model_intelligence()