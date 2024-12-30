from datetime import datetime

from flask import Flask, render_template, request, session, send_file, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import pickle
import os
import csv
import io
from user import User, users  # Import the user model

app = Flask("sccproject")
app.secret_key = 'your_secret_key'  # Replace with a secure key

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Define the base directory
base_dir = os.path.dirname(os.path.abspath(__file__))

# Load the trained model
with open(os.path.join(base_dir, os.pardir, 'ML', 'best_model.pkl'), 'rb') as file:
    loaded_model = pickle.load(file)

# Load the vectorizer
with open(os.path.join(base_dir, os.pardir, 'ML', 'vectorizer.pkl'), 'rb') as file:
    vectorizer = pickle.load(file)

# Function to classify SMS messages
def classify_sms(sms_text):
    sms_vector = vectorizer.transform([sms_text])
    prediction = loaded_model.predict(sms_vector)
    return "spam" if prediction[0] == 1 else "ham"

@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.id == user_id:
            return user
    return None

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        error = login_logic(request)
        if error is not None:
            return render_template('login.html', error=error)
        else:
            return redirect(url_for("hello_world"))

    elif request.method == "GET":
        return render_template("login.html", error=None)

def login_logic(login_request):
    username = login_request.form.get("username")
    password = login_request.form.get("password")
    user = users.get(username)
    if user and user.password == password:
        login_user(user)
        session.permanent = False  # Session will expire when the browser is closed
        return None
    else:
        return "Invalid username or password"

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/", methods=["GET", "POST"])
@login_required
def hello_world():

    user_id = str(current_user.id)
    username = current_user.username
    if f'sms_log_{user_id}' not in session:
        session[f'sms_log_{user_id}'] = []

    if request.method == "POST":
        sms_text = request.form.get("sms_text")
        classification = classify_sms(sms_text)
        session[f'sms_log_{user_id}'].insert(0, (sms_text, classification))
        session.modified = True
        return redirect(url_for("hello_world"))  # Redirect after POST


    sms_log = session[f'sms_log_{user_id}']
    total_sms = len(sms_log)
    spam_count = sum(1 for _, classification in sms_log if classification == 'spam')
    spam_percentage = (spam_count / total_sms * 100) if total_sms > 0 else 0
    spam_percentage = f"{spam_percentage:.2f}"  # Format to two decimal places

    return render_template('index.html', person1="Aouni", person2="Peter", sms_log=sms_log, total_sms=total_sms, spam_count=spam_count, spam_percentage=spam_percentage, username=username)

@app.route("/export")
@login_required
def export_log():
    user_id = str(current_user.id)
    if f'sms_log_{user_id}' not in session or not session[f'sms_log_{user_id}']:
        return "No data to export", 400

    # Create a CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['SMS', 'Classification'])
    writer.writerows(session[f'sms_log_{user_id}'])

    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='sms_log.csv'
    )

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in users:
            return "User already exists", 400
        user_id = str(len(users) + 1)
        users[username] = User(user_id, username, password)
        return redirect(url_for("login"))
    return render_template("signup.html")

@app.route("/delete_history")
@login_required
def delete_history():
    user_id = str(current_user.id)
    session[f'sms_log_{user_id}'] = []
    session.modified = True
    return redirect(url_for("hello_world"))

@app.route("/api/classification", methods=["POST"])
def classify_sms_api():
    start_time = datetime.now()
    response = {
        "classification": classify_sms(request.json.get("sms_text")),
        "response_time_in_ms": (datetime.now() - start_time).microseconds
    }
    return jsonify(response)


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)

@app.route("/site-map")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if ("GET" in rule.methods or "POST" in rule.methods) and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    # links is now a list of url, endpoint tuples
    return render_template("all_links.html", links=links)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')