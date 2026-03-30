from flask import Flask, render_template, request
import spacy
import re

app = Flask(__name__)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Skills list (you can add more)
SKILLS = [
    "python", "java", "c", "c++", "html", "css", "javascript",
    "machine learning", "ai", "sql", "flask", "django"
]

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form['resume']
    doc = nlp(text)

    # -----------------------------
    # ✅ Extract Emails
    # -----------------------------
    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}", text)

    # -----------------------------
    # ✅ Extract Names (FIXED)
    # -----------------------------
    names = []

    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name = ent.text.strip()

            # Remove unwanted words
            unwanted = ["email", "gmail", "phone", "contact"]
            words = name.split()

            clean_name = []
            for w in words:
                if w.lower() not in unwanted:
                    clean_name.append(w)

            name = " ".join(clean_name)

            if len(name.split()) >= 2:
                names.append(name)

    names = list(set(names))

    # -----------------------------
    # ✅ Extract Skills
    # -----------------------------
    found_skills = []
    text_lower = text.lower()

    for skill in SKILLS:
        if skill in text_lower:
            found_skills.append(skill.upper())
    found_skills = list(set(found_skills))

    return render_template(
        "index.html",
        names=names,
        emails=emails,
        skills=found_skills
    )
if __name__ == '__main__':

    app.run(debug=True)