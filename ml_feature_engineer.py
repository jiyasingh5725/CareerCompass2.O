# ml_feature_engineer.py
import re

class MLFeatureEngineer:
    def __init__(self):
        # Broad list of keywords to detect certifications
        self.cert_keywords = ["certified", "certification", "aws certified", "coursera", "udemy", "pmp", "scrum", "cisco"]
        
    def extract_features(self, resume_text, skills_list):
        text_lower = resume_text.lower()
        
        # 1. Skill Count
        skill_count = len(skills_list)
        
        # 2. Education Tier Encoding
        education_tier = 0  # Default (None/High School)
        if any(word in text_lower for word in ["b.tech", "bachelor", "b.e", "undergraduate", "bsc"]):
            education_tier = 1  # Bachelor's
        if any(word in text_lower for word in ["m.tech", "master", "m.e", "msc", "mba"]):
            education_tier = 2  # Master's / Higher
            
        # 3. Experience Vector (Look for patterns like "2 years", "3+ years", "exp: 5 yrs")
        exp_years = 0
        exp_patterns = [
            r"(\d+)\s*(?:year|yr)s?\s*(?:of\s*)?(?:experience|exp)",
            r"(?:experience|exp)\s*[:|-]?\s*(\d+)\s*(?:year|yr)s?"
        ]
        for pattern in exp_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                # Take the highest found experience mentioned to prevent mistaking dates
                exp_years = max(exp_years, max(int(m) for m in matches if int(m) < 40))
                break

        # 4. Projects Counted
        # Split text into lines or blocks and count occurrences of project sections/bullet points
        project_count = text_lower.count("project")
        # Normalize: if "project" is mentioned a lot, map it to a reasonable count of distinct projects (capped at 5)
        project_count = min(max(1, project_count // 2), 5) if "project" in text_lower else 0

        # 5. Certifications Count
        cert_count = 0
        for keyword in self.cert_keywords:
            if keyword in text_lower:
                cert_count += text_lower.count(keyword)
        cert_count = min(cert_count, 5) # Cap at 5 for stability
        
        return {
            "skills_count": skill_count,
            "education_tier": education_tier,
            "experience_years": exp_years,
            "projects_count": project_count,
            "certifications_count": cert_count,
            "skills_string": " ".join(skills_list) # Keep for vocabulary mapping
        }