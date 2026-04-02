from flask import Flask, render_template, request
import PyPDF2

app = Flask(__name__)

SKILLS = [
    "python", "java", "c", "html", "css",
    "flask", "sql", "ai", "data structures"
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["resume"]

    text = ""

    if file:
        pdf = PyPDF2.PdfReader(file)
        for page in pdf.pages:
            text += page.extract_text()

    text_lower = text.lower()

    found_skills = []
    for skill in SKILLS:
        if skill in text_lower:
            found_skills.append(skill)

    score = len(found_skills) / len(SKILLS) * 100 if SKILLS else 0
    score = round(score)

    if score > 70:
        role = "Backend Developer"
    elif score > 40:
        role = "Junior Developer"
    else:
        role = "Beginner"

    return render_template(
        "index.html",
        text=text,
        skills=found_skills,
        score=score,
        role=role
    )

if __name__ == "__main__":
    app.run(debug=True)