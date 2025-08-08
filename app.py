from flask import Flask, render_template, request, jsonify
import csv
import os
from datetime import datetime

app = Flask(__name__)

FEEDBACK_FILE = "feedback.csv"

# Create feedback file if it doesn't exist
if not os.path.exists(FEEDBACK_FILE):
    with open(FEEDBACK_FILE, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(["timestamp", "case_number", "rating", "comments"])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search", methods=["POST"])
def search():
    case_number = request.form.get("case_number", "").strip().upper()
    if not case_number or len(case_number) < 3:
        return jsonify({"error": "Please enter a valid case number."}), 400

    # Mock response – shows fake but realistic data
    return jsonify({
        "case_number": case_number,
        "case_title": f"Raju Kumar vs State of Karnataka",
        "status": "Hearing Concluded",
        "court_name": "High Court of Karnataka",
        "petitioner": "Raju Kumar",
        "respondent": "State of Karnataka",
        "filing_date": "2022-03-15",
        "last_listed": "2024-05-10",
        "next_listed": "2024-06-05",
        "acts": "IPC Section 420, 342",
        "source": "eCourts India (Public Data)"
    })

@app.route("/submit_feedback", methods=["POST"])
def submit_feedback():
    try:
        data = request.json
        with open(FEEDBACK_FILE, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([
                datetime.now().isoformat(),
                data.get("case", ""),
                data.get("rating", ""),
                data.get("comments", "")
            ])
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
