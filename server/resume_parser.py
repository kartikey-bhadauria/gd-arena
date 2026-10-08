# Simple & robust keyword-based resume and JD parser
import re

SKILL_KEYWORDS = [
    "python", "java", "javascript", "typescript", "c++", "c#", "react", "node", "django",
    "flask", "fastapi", "sql", "postgres", "mongodb", "mysql", "redis", "aws", "docker",
    "kubernetes", "git", "linux", "html", "css", "tailwind", "pandas", "numpy", "pytorch",
    "tensorflow", "machine learning", "deep learning", "nlp", "computer vision", "rest api",
    "graphql", "microservices", "system design", "data structures", "algorithms"
]

def parse_resume_text(text):
    if not text:
        return {"skills": [], "education": [], "experience": [], "projects": [], "raw_length": 0}

    text_lower = text.lower()
    lines = [l.strip() for l in text.splitlines() if l.strip()]

    # Extract Skills
    found_skills = []
    for skill in SKILL_KEYWORDS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            found_skills.append(skill.title() if len(skill) > 3 else skill.upper())

    # Extract Education
    edu_keywords = ["b.tech", "btech", "b.e", "b.sc", "bca", "m.tech", "mca", "university", "college", "institute", "gpa", "cgpa", "bachelor", "master"]
    education = []
    for line in lines:
        if any(ek in line.lower() for ek in edu_keywords):
            if len(line) < 120:
                education.append(line)

    # Extract Experience
    exp_keywords = ["intern", "internship", "developer", "engineer", "analyst", "assistant", "lead", "trainee", "founder", "freelance"]
    experience = []
    for line in lines:
        if any(ek in line.lower() for ek in exp_keywords):
            if len(line) < 140:
                experience.append(line)

    # Extract Projects
    proj_keywords = ["project", "developed", "built", "designed", "implemented", "created", "clone", "full stack", "app", "model"]
    projects = []
    for line in lines:
        if any(pk in line.lower() for pk in proj_keywords):
            if len(line) < 150:
                projects.append(line)

    return {
        "skills": list(dict.fromkeys(found_skills)),
        "education": education[:4],
        "experience": experience[:5],
        "projects": projects[:5],
        "raw_length": len(text)
    }

def match_jd_skills(resume_skills, jd_text):
    if not jd_text:
        return {"score": 75, "matched": resume_skills[:4], "missing": ["System Design", "Cloud Infrastructure"]}
    jd_lower = jd_text.lower()
    matched = []
    missing = []
    for skill in SKILL_KEYWORDS:
        if re.search(r'\b' + re.escape(skill) + r'\b', jd_lower):
            display = skill.title() if len(skill) > 3 else skill.upper()
            if any(display.lower() == s.lower() for s in resume_skills):
                matched.append(display)
            else:
                missing.append(display)
    
    total = len(matched) + len(missing)
    score = int((len(matched) / total * 100)) if total > 0 else 70
    return {
        "score": max(20, min(98, score)),
        "matched": matched[:8],
        "missing": missing[:6]
    }
