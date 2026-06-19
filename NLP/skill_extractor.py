import re


class SkillExtractor:

    def __init__(self):

        self.skills = [

            "python",
            "java",
            "c",
            "c++",
            "javascript",
            "react",
            "node",
            "express",
            "html",
            "css",
            "bootstrap",
            "tailwind",
            "mysql",
            "sql",
            "mongodb",
            "flask",
            "django",
            "git",
            "github",
            "docker",
            "kubernetes",
            "aws",
            "azure",
            "machine learning",
            "deep learning",
            "tensorflow",
            "pytorch",
            "opencv",
            "nlp",
            "pandas",
            "numpy",
            "power bi",
            "excel",
            "data analysis"

        ]


    def extract(self, resume_text):

        resume_text = resume_text.lower()

        found_skills = []

        for skill in self.skills:

            pattern = r"\b" + re.escape(skill) + r"\b"

            if re.search(pattern, resume_text):

                found_skills.append(skill.title())

        return sorted(list(set(found_skills)))