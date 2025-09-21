from flask import Flask, request, render_template, redirect, url_for, flash
from agent import run_query
from db import get_all_reports, get_report_by_id, save_report, init_db, DB_PATH
import json
import sqlite3

app = Flask(__name__)
app.secret_key = "your-secret-key"  # Needed for flashing messages

# Jinja filter to parse JSON strings
@app.template_filter('from_json')
def from_json(s):
    try:
        return json.loads(s)
    except Exception:
        return {}

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        query = request.form.get("query")
        if not query:
            flash("Please enter a query!")
            return redirect(url_for("home"))
        return redirect(url_for("search", query=query))
    return render_template("home.html")

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        query = request.form.get("query")
        if not query:
            flash("Query missing!")
            return redirect(url_for("home"))
        return redirect(url_for("search", query=query))

    query = request.args.get("query")
    if not query:
        flash("Query missing!")
        return redirect(url_for("home"))

    try:
        report_id = run_query(query)  # returns saved report id
        return redirect(url_for("view_report", report_id=report_id))
    except Exception as e:
        flash(f"Error running query: {e}")
        return redirect(url_for("home"))

@app.route("/history")
def history():
    reports = get_all_reports()
    return render_template("history.html", reports=reports)

@app.route("/report/<int:report_id>")
def view_report(report_id):
    report = get_report_by_id(report_id)
    if not report:
        flash("Report not found")
        return redirect(url_for("history"))

    # Parse JSON for display
    summary_json = json.loads(report["summary"])
    sources_json = json.loads(report["sources"])

    return render_template(
        "report.html",
        report=report,
        summary=summary_json,
        sources=sources_json
    )

@app.route("/history/clear", methods=["POST"])
def clear_history():
    """Clear all saved reports from the database."""
    conn = sqlite3.connect(DB_PATH)  # use the same DB_PATH as db.py
    c = conn.cursor()
    c.execute('DELETE FROM reports')  # remove all reports
    conn.commit()
    conn.close()
    flash("History cleared successfully!")
    return redirect(url_for("history"))

if __name__ == "__main__":
    app.run(port=5050, debug=True)
