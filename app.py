import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime
from functools import wraps
import requests
from dotenv import load_dotenv

from database import engine, Base
from models import User
from crud import get_content, save_content, find_user_by_username, create_user, list_projects
from prompts import build_home_prompt
from flask_bcrypt import Bcrypt
from pydantic import ValidationError
from schemas import AIRequest

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_key")
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Create DB tables
Base.metadata.create_all(bind=engine)

bcrypt = Bcrypt(app)

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_URL = "https://api.openai.com/v1/chat/completions"

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user" not in session:
            flash("Please log in to access that page.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated

@app.context_processor
def inject_year():
    return {"current_year": datetime.now().year}

@app.route("/")
def home():
    default = "Welcome to my AI-managed portfolio! I’m passionate about technology, innovation, and building impactful solutions."
    home_intro = get_content("home") or default
    return render_template("index.html", title="Home", home_intro=home_intro)

@app.route("/about")
def about():
    about_text = get_content("about") or "I am a Computer Science postgraduate specializing in AI and software development."
    return render_template("about.html", title="About", about_content=about_text)

@app.route("/projects")
def projects():
    projects_list = list_projects()
    return render_template("projects.html", title="Projects", projects=projects_list)

@app.route("/contact")
def contact():
    contact_text = get_content("contact") or "Feel free to reach out through the contact form or my social links."
    return render_template("contact.html", title="Contact", contact_text=contact_text)

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", title="Dashboard")

@app.route("/ai_rewrite", methods=["GET", "POST"])
@login_required
def ai_rewrite():
    if request.method == "POST":
        try:
            # validate input with pydantic
            body = AIRequest(**request.form)
        except ValidationError:
            flash("Invalid input, please check your form fields.", "danger")
            return redirect(url_for("ai_rewrite"))

        prompt = build_home_prompt(body.section, body.job_role, body.keywords, body.project_info)

        if not OPENAI_API_KEY:
            flash("AI key not configured. Please set OPENAI_API_KEY.", "danger")
            return redirect(url_for("dashboard"))

        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 400
        }

        resp = requests.post(OPENAI_URL, headers=headers, json=data, timeout=30)
        if resp.status_code != 200:
            flash(f"AI service error: {resp.status_code}", "danger")
            return redirect(url_for("dashboard"))

        ai_text = resp.json()["choices"][0]["message"]["content"].strip()
        save_content(body.section, ai_text)
        flash("AI copy generated and saved.", "success")
        return render_template("ai_result.html", section=body.section, rewritten_text=ai_text)

    return render_template("ai_rewrite.html", title="AI Copywriter")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = find_user_by_username(username)
        if user and bcrypt.check_password_hash(user.password_hash, password):
            session["user"] = user.username
            flash("Logged in successfully", "success")
            return redirect(url_for("dashboard"))
        flash("Invalid credentials", "danger")
    return render_template("login.html", title="Login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if find_user_by_username(username):
            flash("Username already exists", "warning")
            return redirect(url_for("register"))
        pw_hash = bcrypt.generate_password_hash(password).decode()
        create_user(username, pw_hash)
        flash("Account created — please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out", "info")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
