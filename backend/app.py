from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import uuid
from concurrent.futures import ThreadPoolExecutor

from analyzer import analyze_log_file
from analysis import create_summary, attacks_per_hour


app = Flask(__name__)
CORS(app)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


LOG_FILE = os.path.join(
    BASE_DIR,
    "logs",
    "sample.log"
)


DEMO_LOG_FILE = os.path.join(
    BASE_DIR,
    "logs",
    "demo.log"
)


UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "logs",
    "uploads"
)


os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# Background job executor
executor = ThreadPoolExecutor(max_workers=2)

# Stores job status and results
jobs = {}


def process_log_job(job_id, file_path):
    try:
        jobs[job_id]["status"] = "processing"

        results = analyze_log_file(file_path)

        summary = create_summary(results)
        summary["attacks_per_hour"] = attacks_per_hour(results)

        jobs[job_id]["status"] = "completed"
        jobs[job_id]["result"] = summary

    except Exception as error:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(error)


@app.route("/")
def home():
    return "LogLens Backend is Running!"


@app.route("/api/analysis")
def get_analysis():
    results = analyze_log_file(LOG_FILE)

    summary = create_summary(results)
    summary["attacks_per_hour"] = attacks_per_hour(results)

    return jsonify(summary)


@app.route("/api/demo-analysis")
def get_demo_analysis():
    results = analyze_log_file(DEMO_LOG_FILE)

    summary = create_summary(results)
    summary["attacks_per_hour"] = attacks_per_hour(results)

    return jsonify(summary)


@app.route("/api/upload", methods=["POST"])
def upload_log():

    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    filename = secure_filename(file.filename)

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(file_path)

    # Create unique job ID
    job_id = str(uuid.uuid4())

    jobs[job_id] = {
        "status": "queued",
        "result": None,
        "error": None
    }

    # Start background processing
    executor.submit(
        process_log_job,
        job_id,
        file_path
    )

    return jsonify({
        "job_id": job_id,
        "status": "queued"
    }), 202


@app.route("/api/job/<job_id>")
def get_job_status(job_id):

    job = jobs.get(job_id)

    if job is None:
        return jsonify({
            "error": "Job not found"
        }), 404

    response = {
        "job_id": job_id,
        "status": job["status"]
    }

    if job["status"] == "completed":
        response["result"] = job["result"]

    if job["status"] == "failed":
        response["error"] = job["error"]

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)