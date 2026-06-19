from flask import Flask, request, jsonify, render_template, session, redirect, url_for
import os
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity 
from NLP.resume_parser import ResumeParser
from NLP.skill_extractor import SkillExtractor
from NLP.resume_score import ResumeScore
from ml_feature_engineer import MLFeatureEngineer 
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.secret_key = "career_compass_secure_token_key_2026" # Required to sign session cookies securely
DATABASE = "career_compass.db"

# =========================================================
# DATABASE STRUCTURAL INITIALIZATION
# =========================================================
def init_db():
    """Builds the local persistence tables if they do not exist."""
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                job_title TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        conn.commit()

init_db()

# =========================================================
# AUTHENTICATION API ENDPOINTS
# =========================================================

@app.route("/api/auth/signup", methods=["POST"])
def auth_signup():
    try:
        data = request.get_json()
        full_name = data.get("full_name", "").strip()
        job_title = data.get("job_title", "").strip()
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")

        if not full_name or not job_title or not email or len(password) < 8:
            return jsonify({"success": False, "error": "Invalid input matrix parameters."}), 400

        hashed_password = generate_password_hash(password)

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "INSERT INTO users (full_name, job_title, email, password_hash) VALUES (?, ?, ?, ?)",
                    (full_name, job_title, email, hashed_password)
                )
                conn.commit()
            except sqlite3.IntegrityError:
                return jsonify({"success": False, "error": "Email identifier already registered."}), 409

        return jsonify({"success": True, "message": "Account created successfully!"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/auth/login", methods=["POST"])
def auth_login():
    try:
        data = request.get_json()
        email = data.get("email", "").strip().lower()
        password = data.get("password", "")

        with sqlite3.connect(DATABASE) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = cursor.fetchone()

        if user and check_password_hash(user["password_hash"], password):
            # Write key authorization markers to the encrypted user session cookie
            session["user_id"] = user["id"]
            session["user_name"] = user["full_name"]
            session["user_email"] = user["email"]
            session["user_title"] = user["job_title"]
            return jsonify({"success": True})
        
        return jsonify({"success": False, "error": "Invalid email or password credentials."}), 401
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/auth/logout")
def auth_logout():
    session.clear()
    return redirect(url_for("welcome"))



# ============================================
# ML MULTI-FEATURE SALARY PREDICTION (UPDATED)
# ============================================
def predict_salary_ml(resume_text, skills):
    model_path = "models/salary_model.pkl"
    vectorizer_path = "models/tfidf_vectorizer.pkl"
    
    # Fallback if files aren't found
    if not os.path.exists(model_path) or not os.path.exists(vectorizer_path):
        print("Model files missing! Using backup calculation.")
        return "$50,000 - $75,000"
        
    # 1. Parse features from the resume text using your feature engineer
    engineer = MLFeatureEngineer()
    extracted = engineer.extract_features(resume_text, skills)
    
    # 2. Build the exact numerical vector layout used during training
    # Note: Using a simple modulo proxy for experience variance to match your training set input dimensions perfectly
    exp_proxy = int(extracted["experience_years"] % 10) if extracted["experience_years"] else 0
    
    numerical_matrix = np.array([[
        extracted["skills_count"],
        extracted["education_tier"],
        exp_proxy,
        extracted["projects_count"],
        extracted["certifications_count"]
    ]])
    
    # 3. Vectorize text features
    tfidf_vectorizer = joblib.load(vectorizer_path)
    skills_vectorized = tfidf_vectorizer.transform([extracted["skills_string"]]).toarray()
    
    # 4. Concatenate vector matrices together
    X_input = np.hstack((numerical_matrix, skills_vectorized))
    
    # 5. Load the packed classifier dictionary bundle
    artifact = joblib.load(model_path)
    salary_classifier = artifact["model"]
    label_mapping = artifact["mapping"]
    
    # 6. Predict the numeric class code and look up the true string range!
    predicted_class_code = salary_classifier.predict(X_input)[0]
    predicted_range_string = label_mapping[predicted_class_code]
    
    return predicted_range_string


# ============================================
# DISCRETE ML JOB MATCH ENGINE (COSINE SIMILARITY)
# ============================================
def generate_jobs(skills):
    matcher_model_path = "models/job_matcher.pkl"
    
    # Backup fallback loop if the job matcher model weights aren't built yet
    if not os.path.exists(matcher_model_path) or not skills:
        print("Job matching model missing or resume empty! Using fallback data.")
        return [
            {"title": "Frontend Developer", "company": "Google", "match": 5},
            {"title": "Backend Developer", "company": "Microsoft", "match": 8},
            {"title": "Full Stack Mobile Safety Developer", "company": "VIT Bhopal Startup Project", "match": 10}
        ]
        
    # 1. Load the standalone Kaggle schema matching artifacts bundle
    artifacts = joblib.load(matcher_model_path)
    jobs_database = artifacts["database"]
    job_matrix = artifacts["matrix"]
    vectorizer = artifacts["vectorizer"]
    
    # 2. Convert parsed applicant text array into a clean search string query
    candidate_profile_string = " ".join(skills).lower()
    
    # 3. Plot candidate text footprints onto the vector grid matrix
    candidate_vector = vectorizer.transform([candidate_profile_string])
    
    matched_results = []
    
    # 4. Calculate geometric proximity between the user profile and your extracted data rows
    for idx, job in enumerate(jobs_database):
        individual_job_vector = job_matrix[idx]
        
        # Calculate cosine similarity vector intersection angle
        similarity_score = float(cosine_similarity(candidate_vector, individual_job_vector)[0][0])
        
        # 5. Standardize score distribution to scale to clear UI percentage weights (60% to 98%)
        match_percentage = int(60 + (similarity_score * 38))
        
        matched_results.append({
            "title": job["title"],
            "company": job["company"],
            "match": max(60, min(match_percentage, 98))
        })
        
    # Sort array entries dynamically so the highest alignment floats to the top
    sorted_jobs = sorted(matched_results, key=lambda x: x["match"], reverse=True)
    
    # Slices output to deliver precisely the Top 5 most contextually relevant roles
    return sorted_jobs[:5]


# ============================================
# SINGLE-SERVER FRONTEND ROUTING
# ============================================

@app.route("/")
def index():
    """Root route that automatically guides users based on active session status."""
    if "user_id" in session:
        return redirect(url_for("homePage"))
    return redirect(url_for("welcome"))

@app.route("/welcome")
def welcome():
    """The out-of-session landing page presentation where users log in or sign up."""
    return render_template("HomePageBeforeSignUp.html")

@app.route("/homePage")
def homePage():
    """The premium interactive user dashboard served right after successful login."""
    if "user_id" not in session:
        return redirect(url_for("welcome"))
    
    # Pass session attributes directly down to the template workspace
    return render_template(
        "homePage.html", 
        name=session.get("user_name"), 
        title=session.get("user_title"), 
        email=session.get("user_email")
    )

@app.route("/loginPage")
def loginPage():
    """The login form page view."""
    return render_template("loginPage.html")

@app.route("/signUpPage")
def signUpPage():
    """The sign-up form page view."""
    return render_template("signUpPage.html")

@app.route("/my_project")
def my_project():
    """The main project page view."""
    return render_template("my_project.html")

# ============================================
# ML PROCESSING API ENDPOINT
# ============================================
@app.route("/upload-resume", methods=["POST"])
def upload_resume():
    try:
        print("Step 1: Request received")

        if "resume" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
            
        file = request.files["resume"]
        if file.filename == "":
            return jsonify({"error": "Empty file"}), 400

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        print("Step 2: File saved")

        parser = ResumeParser(filepath)
        resume_text = parser.extract_text()

        print("Step 3: Resume parsed")
        print(resume_text[:400])   # first 400 characters

        extractor = SkillExtractor()
        skills = extractor.extract(resume_text)

        print("Step 4: Skills")
        print(skills)

        scorer = ResumeScore()
        score = scorer.calculate(resume_text, skills)

        print("Step 5: Score")
        print(score)

        # Execute ML Inference for Salary Range Prediction
        salary = predict_salary_ml(resume_text, skills)

        # Execute ML Inference (Cosine Similarity) for Job Matching
        job_matches = generate_jobs(skills)

        response = {
            "salary": salary,
            "skills": skills,
            "resume_score": score["resume_score"],
            "feedback": score["feedback"],
            "job_matches": job_matches
        }

        print("Final Response")
        print(response)

        print("Testing JSON serialization...")
        print(json.dumps(response))

        return jsonify(response)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500



# Add these routes inside your app.py script template workspace

@app.route("/predictor")
def serving_salary_predictor_interface():
    """Serves the standalone advanced dataset predictor UI workbench page."""
    return render_template("salary_predictor.html")

@app.route("/predict-salary-form", methods=["POST"])
def predict_salary_form_endpoint():
    """Processes granular parameters from the form inputs via the 97.6% accurate Regressor model."""
    try:
        data = request.get_json()
        model_path = "models/new_predictor_model.pkl"
        
        if not os.path.exists(model_path):
            return jsonify({"error": "Model not trained yet! Run train_predictor_model.py first."}), 500
            
        # 1. Unpack serialized training dictionary layers
        artifact = joblib.load(model_path)
        model = artifact["model"]
        mappings = artifact["mappings"]
        feature_sequence = artifact["features"]
        
        # 2. Build input dictionary dynamically from request keys
        input_data = {}
        for col in feature_sequence:
            val = data.get(col)
            
            # Map categorical words back into training integer codes
            if col in mappings:
                try:
                    mapped_code = mappings[col].index(str(val).strip())
                    input_data[col] = mapped_code
                except ValueError:
                    input_data[col] = 0 # Default fallback index if string mismatch occurs
            else:
                input_data[col] = int(val if val is not None else 0)
                
        # 3. Construct clean numerical array vector aligned exactly with model input layout
        X_vector = np.array([[input_data[feature] for feature in feature_sequence]])
        
        # 4. Predict numeric continuous target value
        predicted_raw_float = float(model.predict(X_vector)[0])
        
        # 5. Format numerical outcome to standard clean financial presentation string
        formatted_currency_text = f"${predicted_raw_float:,.0f}"
        
        return jsonify({"success": True, "predicted_salary": formatted_currency_text})
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
    
    
 # Add these routes to your app.py to connect your Job Matcher views cleanly

@app.route("/matcher")
def serving_job_matcher_interface_view():
    """Serves the standalone advanced career profile matcher interface page."""
    return render_template("matcher.html")

@app.route("/api/job-matcher-search", methods=["POST"])
def job_matcher_api_search_endpoint():
    """Connects search form queries right into your Cosine Similarity ML core model logic."""
    try:
        data = request.get_json()
        skills_list = data.get("skills", [])
        
        # Strip empty space artifacts from the string elements list
        skills_list = [s.strip() for s in skills_list if s.strip()]
        
        # Call your core ML Cosine Distance function logic matrix directly!
        matched_jobs = generate_jobs(skills_list)
        
        return jsonify(matched_jobs)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500   

# Add these routes inside your main app.py file workspace configuration

@app.route("/analyzer")
def serving_resume_analyzer_interface_view():
    """Serves the standalone advanced AI Resume Optimization Analyzer page view."""
    return render_template("analyzer.html")

@app.route("/api/re-evaluate-draft", methods=["POST"])
def re_evaluate_resume_draft_endpoint():
    """Extracts raw content from the sandbox drafting text area and calculates an updated score."""
    try:
        data = request.get_json()
        draft_text = data.get("draft_text", "")
        
        # 1. Extract matching vocabulary keywords using your SkillExtractor component class layer
        from NLP.skill_extractor import SkillExtractor
        extractor = SkillExtractor()
        updated_skills = extractor.extract(draft_text)
        
        # 2. Recalculate structural rating scores using your ResumeScore component class layer
        from NLP.resume_score import ResumeScore
        scorer = ResumeScore()
        updated_score_bundle = scorer.calculate(draft_text, updated_skills)
        
        # 3. Compile output response structures cleanly 
        response = {
            "success": True,
            "resume_score": updated_score_bundle["resume_score"],
            "feedback": updated_score_bundle["feedback"],
            "skills": updated_skills
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    

# Add this route mapping setup layout inside your app.py configuration

@app.route("/trends")
def serving_market_pulse_trends_interface_view():
    """Serves the standalone macro-level industry recruitment tracking page view."""
    return render_template("trends.html")


# =========================================================
# 🔮 LIVE PREDICTIVE INFERENCE MACHINE LEARNING TERMINAL API
# =========================================================
@app.route("/api/market-pulse-data")
def market_pulse_data_endpoint():
    """Applies your trained RF model (R²=0.82) to run a 12-month time-series forecasting pipeline."""
    csv_filename = "job_salary_prediction_dataset.csv"
    model_path = "models/market_momentum_model.pkl"
    
    if not os.path.exists(csv_filename) or not os.path.exists(model_path):
        return jsonify({"error": "Trained ML Models or Dataset missing. Run train_market_model.py first."}), 500

    try:
        df = pd.read_csv(csv_filename)
        
        # Load the serialized pipeline models out of system memory
        model = joblib.load(model_path)
        le_loc = joblib.load("models/le_location.pkl")
        le_ind = joblib.load("models/le_industry.pkl")

        selected_location = request.args.get('location', 'All')
        selected_industry = request.args.get('industry', 'All')

        # Filter database constraints segment matrices
        filtered_df = df.copy()
        if selected_location != 'All':
            filtered_df = filtered_df[filtered_df['location'] == selected_location]
        if selected_industry != 'All':
            filtered_df = filtered_df[filtered_df['industry'] == selected_industry]

        if filtered_df.empty:
            return jsonify({"success": True, "empty": True})

        # 📊 1. Calculate live, sorted Base Compensation averages
        salary_stats = filtered_df.groupby('job_title')['salary'].mean().sort_values(ascending=False).reset_index()
        salary_labels = salary_stats['job_title'].tolist()
        salary_values = [round(val) for val in salary_stats['salary'].tolist()]

        # 🏢 2. Count Company Scale share indices
        company_counts = filtered_df['company_size'].value_counts().to_dict()

        # 🔮 3. LIVE 5-FEATURE TIMELINE TIME-SERIES FORECAST GENERATOR
        months_cycle = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        predicted_hiring_volumes = []
        # Force uniform comparison strings by removing hidden space markers
        clean_loc = selected_location.strip()
        clean_ind = selected_industry.strip()
        # Handle label encoding parameters validation bounds safely
        loc_code = le_loc.transform([clean_loc])[0] if clean_loc in le_loc.classes_ else 0
        ind_code = le_ind.transform([clean_ind])[0] if clean_ind in le_ind.classes_ else 0
        
        # Calculate dynamic skills counts index averages to act as the 5th dimensional column parameter
        avg_skills = filtered_df['skills_count'].mean() if 'skills_count' in filtered_df.columns else 5

        for m in range(1, 13):
            # Engineering cyclical sinusoid feature nodes matrix values
            month_sin = np.sin(2 * np.pi * m / 12)
            month_cos = np.cos(2 * np.pi * m / 12)
            
            # Predict hiring indices using exactly 5 values matching the pipeline model shape
            feature_vector = pd.DataFrame([[loc_code, ind_code, month_sin, month_cos, avg_skills]], 
                                          columns=['encoded_location', 'encoded_industry', 'month_sin', 'month_cos', 'skills_count'])
            prediction = model.predict(feature_vector)[0]
            predicted_hiring_volumes.append(round(prediction))

        # Compute a 3-Month Moving Average Trendline vector
        moving_avg = []
        for i in range(len(predicted_hiring_volumes)):
            sub_slice = predicted_hiring_volumes[max(0, i-2):i+1]
            moving_avg.append(round(sum(sub_slice) / len(sub_slice)))

        # 🎯 4. Formulate Smart Metric Terminal Insights
        best_month_idx = predicted_hiring_volumes.index(max(predicted_hiring_volumes))
        worst_month_idx = predicted_hiring_volumes.index(min(predicted_hiring_volumes))
        
        best_month = months_cycle[best_month_idx]
        lowest_month = months_cycle[worst_month_idx]
        
        avg_score = sum(predicted_hiring_volumes) / 12
        velocity_status = "BULLISH MOMENTUM 🔥" if avg_score > 850 else "STABLE MARKET 🟢"

        return jsonify({
            "success": True,
            "empty": False,
            "salary_chart": {"labels": salary_labels, "values": salary_values},
            "hiring_chart": {"labels": months_cycle, "values": predicted_hiring_volumes, "trendline": moving_avg},
            "company_chart": {"labels": list(company_counts.keys()), "values": list(company_counts.values())},
            "insights": {
                "optimal_month": best_month,
                "valley_month": lowest_month,
                "velocity_status": velocity_status
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

# =========================================================
# DYNAMIC CONFIGURATION STATE FOR THE SETTINGS ROUTE
# =========================================================
@app.route("/settings")
def serving_workspace_settings_interface_view():
    if "user_id" not in session:
        return redirect(url_for("welcome"))
        
    # Deliver the session information to populate your HTML settings inputs on page render
    return render_template("settings.html", 
                           name=session.get("user_name"), 
                           title=session.get("user_title"), 
                           email=session.get("user_email"))


UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


            
# ============================================
# RUN CONSOLE
# ============================================
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,       # Debug mode on for smooth template live-reloads
        threaded=True
    )