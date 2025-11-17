import os
prompt = build_home_prompt(body.section, body.job_role, body.keywords, body.project_info)


if not OPENAI_API_KEY:
flash("No OPENAI_API_KEY set. Please configure it in environment.", "danger")
return redirect(url_for("dashboard"))


headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}
data = {
"model": "gpt-3.5-turbo",
"messages": [{"role": "user", "content": prompt}],
"max_tokens": 300
}


r = requests.post(OPENAI_URL, headers=headers, json=data)
if r.status_code != 200:
flash("AI service error: " + r.text[:200], "danger")
return redirect(url_for("dashboard"))


ai_text = r.json()["choices"][0]["message"]["content"].strip()
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
