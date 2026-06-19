from NLP.resume_parser import ResumeParser
from NLP.skill_extractor import SkillExtractor
from NLP.resume_score import ResumeScore

resume = ResumeParser("uploads/Jiya Singh resume.pdf")

text = resume.extract_text()

print("\n===== Resume Text =====\n")
print(text[:1000])

extractor = SkillExtractor()

skills = extractor.extract(text)

print("\n===== Skills =====\n")
print(skills)

score = ResumeScore()

result = score.calculate(text, skills)

print("\n===== Resume Score =====\n")
print(result)