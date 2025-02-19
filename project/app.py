from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
DATA_FILE = "profiles.json"

# Load user profiles
def load_profiles():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return []

# Save user profiles
def save_profiles(users):
    with open(DATA_FILE, "w") as file:
        json.dump(users, file, indent=4)

@app.route("/")
def index():
    users = load_profiles()
    return render_template("index.html", users=users)

@app.route("/add", methods=["GET", "POST"])
def add_profile():
    if request.method == "POST":
        users = load_profiles()
        new_user = {"name": request.form["name"], "email": request.form["email"]}
        users.append(new_user)
        save_profiles(users)
        return redirect(url_for("index"))
    return render_template("edit.html", action="Add", user=None)

@app.route("/edit/<int:user_id>", methods=["GET", "POST"])
def edit_profile(user_id):
    users = load_profiles()
    if request.method == "POST":
        users[user_id]["name"] = request.form["name"]
        users[user_id]["email"] = request.form["email"]
        save_profiles(users)
        return redirect(url_for("index"))
    return render_template("edit.html", action="Edit", user=users[user_id])

@app.route("/delete/<int:user_id>")
def delete_profile(user_id):
    users = load_profiles()
    users.pop(user_id)
    save_profiles(users)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
