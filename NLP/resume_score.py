import re


class ResumeScore:

    def calculate(self, text, skills):

        score = 0

        feedback = []

        # Resume Length

        words = len(text.split())

        if words >= 400:

            score += 20

        elif words >= 250:

            score += 15

        else:

            feedback.append("Resume content is too short.")

        # Skills

        if len(skills) >= 10:

            score += 30

        elif len(skills) >= 5:

            score += 20

        else:

            score += 10
            feedback.append("Add more technical skills.")

        # Email

        if re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text):

            score += 10

        else:

            feedback.append("Email not found.")

        # Phone

        if re.search(r"\d{10}", text):

            score += 10

        else:

            feedback.append("Phone number missing.")

        # Education

        education = [

            "b.tech",
            "bachelor",
            "master",
            "m.tech",
            "b.e",
            "degree"

        ]

        if any(word in text.lower() for word in education):

            score += 15

        else:

            feedback.append("Education section missing.")

        # Projects

        if "project" in text.lower():

            score += 15

        else:

            feedback.append("Add project experience.")

        return {

            "resume_score": score,
            "feedback": feedback

        }