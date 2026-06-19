# CareerCompass2.O
# 🧭 CareerCompass: AI Career Engine v2.0

CareerCompass is an interactive, full-stack predictive career analytics dashboard designed to empower professionals by discovering their market value and aligning their skills with tailored industry opportunities. Leveraging machine learning pipelines, the engine parses resumes, estimates market compensation arrays, and maps job profiles with precision algorithms.

---

## ⚡ Key Intelligence Features

* **Multi-Feature Salary Prediction Engine**: Extracted resume markers (experience years, skill count, education tier, projects, and certifications) feed an advanced machine learning regressor to forecast hyper-localized compensation bounds.
* **Algorithmic Job Matcher (Cosine Proximity Engine)**: Utilizes a vectorized TF-IDF pipeline to compute geometric distance metrics between user skill vectors and live database schematics.
* **Dynamic Notification Hub**: An integrated system messaging dropdown that handles workspace state parameters, live macro trends, and pipeline sync notifications smoothly without overlapping UI elements.
* **Interactive System Settings Sandbox**: A clean workspace terminal splitting form contexts seamlessly between profile adjustments, active core models, and system log configurations.

---

## 🏗️ Technical Stack & Architecture

### Backend Core
* **Framework**: Python Flask (High-concurrency threaded runtime)
* **Database**: SQLite3 (Local context persistence layers for secure user management)
* **Security**: Cryptographic password hashing protection (`werkzeug.security`)

### Machine Learning Stack
* **NLP Layers**: Custom RegEx token matchers and string parsing classes (`ResumeParser`, `SkillExtractor`, `ResumeScore`).
* **Vectorizers**: Scikit-Learn `TfidfVectorizer` mapping word tokens to geometric coordinates.
* **Predictive Frameworks**: Pre-trained Random Forest Ensemble architectures serialized using `joblib`.

### Frontend Layer
* **Styles**: Tailwind CSS (Glassmorphism layer grids & fluid radial blur layouts)
* **Animations**: AOS (Animate On Scroll) Framework library integrations
* **Icons**: Dynamic vector graphics served seamlessly through Lucide Icons

---

## 📂 System Directory Structure

```text
├── app.py                      # Main backend server & machine learning terminal routing
├── NLP/
│   ├── resume_parser.py        # Text extraction tool handling varied file types
│   ├── skill_extractor.py      # Keyword filter matching dictionary definitions
│   └── resume_score.py         # Structural audit algorithms for rating resume weight
├── models/
│   ├── salary_model.pkl        # Serialized multi-feature regression weights
│   ├── tfidf_vectorizer.pkl    # Serialized text vectorization layers
│   ├── job_matcher.pkl         # Bundled cosine similarity reference indices
│   ├── market_momentum_model.pkl # Time-series forecasting pipeline weights
│   ├── le_location.pkl         # Label encoder mapping geographical constraints
│   └── le_industry.pkl         # Label encoder mapping macro industry sectors
├── templates/
│   ├── HomePageBeforeSignUp.html # Public-facing orientation page view
│   ├── loginPage.html          # Authentication terminal for user login
│   ├── signUpPage.html         # User onboarding registration workspace
│   ├── homePage.html           # Main active user overview analytics dashboard
│   ├── settings.html           # System parameters & verification views
│   └── my_project.html         # Project profile fallback presentation layout
├── static/                     # Global client layout CSS stylesheets and assets
└── career_compass.db           # Generated user database (SQLite)
```

# 🚀 Step-by-Step Installation & Deployment

## 1. Clone & Set Up the Workspace Environment

Ensure **Python 3.9+** is installed and configured in your system environment. Clone your project repository, initialize the workspace, and create a virtual environment.

### Initialize the Local Workspace

```bash
# Navigate to the project directory
cd career_compass_v2

# Create a virtual environment
python -m venv venv

# Activate the virtual environment

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

---

## 2. Install Project Core Dependencies

Install the required packages for the Flask application, data processing, and machine learning.

```bash
pip install flask numpy pandas scikit-learn joblib werkzeug
```

---

## 3. Verify System Model Artifact Layouts

Before running the application, ensure the required datasets and trained models are available.

- ✅ `job_salary_prediction_dataset.csv` exists in the project root.
- ✅ The `models/` directory contains the trained model files:
  - `salary_model.pkl`
  - `job_matcher.pkl`
  - *(and any additional model artifacts used by the application)*

Project structure should look similar to:

```text
career_compass_v2/
│
├── app.py
├── career_compass.db
├── job_salary_prediction_dataset.csv
├── models/
│   ├── salary_model.pkl
│   ├── job_matcher.pkl
│   └── ...
├── templates/
├── static/
└── venv/
```

---

## 4. Execute the Application Instance

Start the Flask development server.

```bash
python app.py
```

The application will automatically:

- Initialize the database schema inside **`career_compass.db`**
- Load the trained machine learning models
- Start the Flask development server at:

```text
http://127.0.0.1:5000/
```

---

# 🔒 Authentication API Schema Notes

### **POST** `/api/auth/signup`

Registers a new user.

**Payload**

```json
{
  "full_name": "John Doe",
  "job_title": "Software Engineer",
  "email": "john@example.com",
  "password": "your_password"
}
```

**Features**

- Secure password hashing with salt
- User validation
- Database insertion

---

### **POST** `/api/auth/login`

Authenticates an existing user.

**Payload**

```json
{
  "email": "john@example.com",
  "password": "your_password"
}
```

**Features**

- Password hash verification
- Secure session creation
- Stores:

- `user_id`
- `user_name`
- `user_title`
- `user_email`

---

### **GET** `/api/auth/logout`

Logs out the authenticated user.

**Features**

- Clears the active session
- Redirects to the welcome page

---

# 📝 License

This project is distributed under the **Precision Platform License**.

---

<div align="center">

### CareerCompass Engine v2.0

**2026 Platform Build**

</div>
