import os
import threading
import uuid
from dataclasses import dataclass, field
from typing import Optional

from flask import Flask, jsonify, render_template, request, send_file

app = Flask(__name__)

ACCESS_PASSWORD = os.environ.get("ACCESS_PASSWORD", "")

# ==============================
# JOB STORE
# ==============================

@dataclass
class Job:
    id: str
    status: str  # "pending" | "running" | "done" | "error"
    log: list = field(default_factory=list)
    output_path: Optional[str] = None
    error: Optional[str] = None

jobs: dict = {}
jobs_lock = threading.Lock()

# Limit to 1 concurrent scrape job — Chrome uses ~200-400 MB; free tier has 512 MB
_scrape_semaphore = threading.Semaphore(1)

# ==============================
# BACKGROUND WORKER
# ==============================

def _run_job(job_id: str, url: str):
    def log(msg):
        with jobs_lock:
            jobs[job_id].log.append(msg)

    log("Waiting for available slot...")
    with _scrape_semaphore:
        with jobs_lock:
            jobs[job_id].status = "running"

        try:
            from scraper import run_scrape
            output_path = run_scrape(url, progress_callback=log)
            with jobs_lock:
                jobs[job_id].status = "done"
                jobs[job_id].output_path = output_path
        except Exception as e:
            with jobs_lock:
                jobs[job_id].status = "error"
                jobs[job_id].error = str(e)

# ==============================
# AUTH
# ==============================

def _check_password():
    if not ACCESS_PASSWORD:
        return True  # no password set — open access
    pw = request.form.get("password") or request.args.get("password") or request.headers.get("X-Password", "")
    return pw == ACCESS_PASSWORD

# ==============================
# ROUTES
# ==============================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start():
    if not _check_password():
        return jsonify({"error": "Unauthorized"}), 401
    url = request.form.get("url", "").strip()
    if not url:
        return jsonify({"error": "URL is required"}), 400
    if not url.startswith(("http://", "https://")):
        return jsonify({"error": "URL must start with http:// or https://"}), 400

    job_id = str(uuid.uuid4())
    with jobs_lock:
        jobs[job_id] = Job(id=job_id, status="pending")

    t = threading.Thread(target=_run_job, args=(job_id, url), daemon=True)
    t.start()

    return jsonify({"job_id": job_id}), 202


@app.route("/status/<job_id>")
def status(job_id):
    if not _check_password():
        return jsonify({"error": "Unauthorized"}), 401
    with jobs_lock:
        job = jobs.get(job_id)

    if not job:
        return jsonify({"error": "Job not found"}), 404

    if job.status == "done":
        return jsonify({
            "status": "done",
            "log": job.log,
            "download_url": f"/download/{job_id}",
        })
    elif job.status == "error":
        return jsonify({
            "status": "error",
            "log": job.log,
            "error": job.error,
        })
    else:
        return jsonify({
            "status": job.status,
            "log": job.log,
        })


@app.route("/download/<job_id>")
def download(job_id):
    if not _check_password():
        return jsonify({"error": "Unauthorized"}), 401
    with jobs_lock:
        job = jobs.get(job_id)

    if not job:
        return jsonify({"error": "Job not found"}), 404
    if job.status != "done" or not job.output_path:
        return jsonify({"error": "File not ready"}), 400
    if not os.path.exists(job.output_path):
        return jsonify({"error": "File no longer available"}), 410

    filename = os.path.basename(job.output_path)
    return send_file(job.output_path, as_attachment=True, download_name=filename)


if __name__ == "__main__":
    app.run(debug=True)
