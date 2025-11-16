import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from transformers import pipeline
from datetime import datetime
from functools import wraps

from database import SessionLocal, engine, Base
from models import PageContent, User

Base.metadata.create_all(bind=engine)

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Change in production

app.config["TEMPLATES_AUTO_RELOAD"] = True

generator = pipeline("text-generation", model="gpt2")

def generate_text(prompt, max_length=180):
    result = generator(prompt, max_length=max_length, num_return_sequences=1)
    return result[0]["generated_text"].strip()

def save_content(section, text):
    db = SessionLocal()
    existing = db.query(PageContent).filter(PageContent.section == section).first()
    if existing:
        existing.content = text
    else:
        db.add(PageContent(section=section, content=text))
    db.commit()
    db.close()

def get_content(section, default_text):
    db = SessionLocal()
    entry = db.query(PageContent).filter(PageContent.section == section).first()
    db.close()
    return entry.content if entry else default_text

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            flash("Please log in to access the dashboard.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

@app.route("/")
def home():
    home_intro = get_content(
        "home",
        "Welcome to my AI-managed portfolio! I’m passionate about technology, innovation, and building impactful solutions."
    )
    return render_template("index.html", title="Home", home_intro=home_intro, current_year=datetime.now().year)

@app.route("/about")
def about():
    about_content = get_content(
        "about",
        "I am a Computer Science postgraduate specializing in AI and software development."
    )
    return render_template("about.html", title="About", about_content=about_content, current_year=datetime.now().year)

@app.route("/projects")
def projects():
    projects_content = get_content(
        "projects",
        "Here you can explore my portfolio projects and technical work."
        "Task Management App: A mobile app that allows users to create, edit, and organize tasks with features like deadlines and priority tags."
        "A Weather forecast App: An app that fetches weather data from a public API and displays current conditions and forecasts."
    )
    return render_template("projects.html", title="Projects", projects_content=projects_content, current_year=datetime.now().year)

@app.route("/contact")
def contact():
    contact_text = get_content(
        "contact",
        "Feel free to reach out through the contact form or my social links."
        "Email Address: example@outlook.com, LinkedIn: example, Phone number: +44 123 456 789"
    )
    return render_template("contact.html", title="Contact", contact_text=contact_text, current_year=datetime.now().year)

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", title="Dashboard", current_year=datetime.now().year)

@app.route("/ai_rewrite", methods=["GET", "POST"])
@login_required
def ai_rewrite():
    rewritten_text = None

    if request.method == "POST":
        section = request.form["section"]
        job_role = request.form["job_role"]
        keywords = request.form["keywords"]
        project_info = request.form["project_info"]

        prompt = (
            f"Rewrite the '{section}' section of a portfolio website for someone applying "
            f"as a {job_role}. Use these keywords: {keywords}. "
            f"Include project details if relevant: {project_info}. "
            f"Tone: professional, engaging, clear."
        )

        rewritten_text = generate_text(prompt, max_length=300)
        flash("New AI-generated text created!", "success")

        return render_template(
            "ai_result.html",
            section=section,
            rewritten_text=rewritten_text,
            current_year=datetime.now().year,
        )

    return render_template("ai_rewrite.html", title="AI Copywriter", current_year=datetime.now().year)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = SessionLocal()
        user = db.query(User).filter(User.username == username, User.password == password).first()
        db.close()

        if user:
            session["user"] = username
            flash("Logged in successfully!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password.", "danger")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
