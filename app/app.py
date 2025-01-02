from datetime import datetime
from flask import Flask, render_template, request, send_file, redirect, url_for, session, jsonify
import pickle
import os
import csv
import io

app = Flask("sccproject")
app.secret_key = 'your_secret_key'

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

@app.route("/", methods=["GET", "POST"])
def hello_world():
    if 'sms_log' not in session:
        session['sms_log'] = []

    if request.method == "POST":
        sms_text = request.form.get("sms_text")
        classification = classify_sms(sms_text)
        session['sms_log'].insert(0, (sms_text, classification))
        session.modified = True        
        return redirect(url_for("hello_world"))  # Redirect after POST

    sms_log = session['sms_log']
    total_sms = len(sms_log)
    spam_count = sum(1 for _, classification in sms_log if classification == 'spam')
    spam_percentage = (spam_count / total_sms * 100) if total_sms > 0 else 0
    spam_percentage = f"{spam_percentage:.2f}"  # Format to two decimal places

    return render_template('index.html', person1="Aouni", person2="Peter", sms_log=sms_log, total_sms=total_sms, spam_count=spam_count, spam_percentage=spam_percentage)

@app.route("/export")
def export_log():
    if 'sms_log' not in session or not session['sms_log']:
        return "No data to export", 400

    # Create a CSV in memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['SMS', 'Classification'])
    writer.writerows(session['sms_log'])

    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='sms_log.csv'
    )

@app.route("/delete_history")
def delete_history():
    session['sms_log'] = []
    session.modified = True
    return redirect(url_for("hello_world"))

@app.route("/api/classification", methods=["POST"])
def classify_sms_api():
    start_time = datetime.now()
    response = {
        "classification": classify_sms(request.json.get("sms_text")),
        "calculation_time_in_ms": (datetime.now() - start_time).microseconds/1000
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
    app.run(debug=True, host='0.0.0.0') # port can be changed here, if default port 5000 is used -> port=5001