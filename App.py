from flask import Flask, request, jsonify
from flask_cors import CORS
from log_collector import get_failed_build_log
from ai_explainer import explain_failure
from email_sender import send_failure_email
import requests as req
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)


# ── Route 1: Test Jenkins connection ──────────────────────────────────────────
@app.route('/connect', methods=['POST'])
def connect():
    data  = request.json
    url   = data.get('url', '').rstrip('/')
    user  = data.get('user')
    token = data.get('token')

    if not all([url, user, token]):
        return jsonify({'error': 'Missing url, user, or token'}), 400

    try:
        res = req.get(f"{url}/api/json", auth=(user, token), timeout=5)

        if res.status_code == 401:
            return jsonify({'error': 'Wrong username or API token'}), 401
        if res.status_code == 403:
            return jsonify({'error': 'Access denied. Check your Jenkins permissions'}), 403
        if res.status_code == 404:
            return jsonify({'error': 'Jenkins URL not found. Check the URL'}), 404
        if res.status_code != 200:
            return jsonify({'error': f'Jenkins returned status {res.status_code}'}), 400

        info = res.json()
        return jsonify({
            'status': 'connected',
            'jenkins_version': res.headers.get('X-Jenkins', 'unknown'),
            'node_name': info.get('nodeName', 'master')
        })

    except req.exceptions.ConnectionError:
        return jsonify({'error': 'Cannot reach Jenkins. Make sure it is running and the URL is correct'}), 503
    except req.exceptions.Timeout:
        return jsonify({'error': 'Jenkins connection timed out'}), 504
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── Route 2: Fetch all pipelines ──────────────────────────────────────────────
@app.route('/pipelines', methods=['POST'])
def pipelines():
    data  = request.json
    url   = data.get('url', '').rstrip('/')
    user  = data.get('user')
    token = data.get('token')

    try:
        res = req.get(
            f"{url}/api/json?tree=jobs[name,url,lastBuild[number,result,timestamp,duration]]",
            auth=(user, token),
            timeout=10
        )

        if res.status_code != 200:
            return jsonify({'error': f'Could not fetch pipelines: {res.status_code}'}), 400

        jobs = res.json().get('jobs', [])
        return jsonify({'jobs': jobs, 'total': len(jobs)})

    except req.exceptions.ConnectionError:
        return jsonify({'error': 'Lost connection to Jenkins'}), 503
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── Route 3: Analyze a specific failed pipeline ───────────────────────────────
@app.route('/analyze', methods=['POST'])
def analyze():
    data  = request.json
    url   = data.get('url', '').rstrip('/')
    user  = data.get('user')
    token = data.get('token')
    job   = data.get('job')

    if not all([url, user, token, job]):
        return jsonify({'error': 'Missing required fields'}), 400

    build_number, log_text = get_failed_build_log(job, url, user, token)

    if not log_text:
        return jsonify({'error': f'No failed build log found for: {job}'}), 404

    explanation = explain_failure(job, build_number, log_text)

    # Also send email notification
    send_failure_email(job, build_number, explanation)

    return jsonify({
        'job':          job,
        'build_number': build_number,
        'explanation':  explanation,
        'log':          log_text
    })


# ── Route 4: Health check ─────────────────────────────────────────────────────
@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'message': 'Jenkins AI Explainer backend is running'})


# ── Route 5: Webhook — Jenkins calls this automatically on failure ────────────
@app.route('/webhook', methods=['POST'])
def webhook():
    data  = request.json or {}

    job   = data.get('job')
    url   = data.get('url')   or os.getenv("JENKINS_URL")
    user  = data.get('user')  or os.getenv("JENKINS_USER")
    token = data.get('token') or os.getenv("JENKINS_TOKEN")

    if not job:
        return jsonify({'error': 'Missing job name'}), 400

    if not all([url, user, token]):
        return jsonify({'error': 'Missing Jenkins credentials. Check your .env file'}), 400

    print(f"Webhook triggered for job: {job}")

    build_number, log_text = get_failed_build_log(job, url, user, token)

    if not log_text:
        return jsonify({'error': f'No failed log found for: {job}'}), 404

    explanation = explain_failure(job, build_number, log_text)
    send_failure_email(job, build_number, explanation)

    print(f"Auto-analysis done for: {job} build #{build_number}")

    return jsonify({
        'status':       'success',
        'job':          job,
        'build_number': build_number,
        'message':      'Analysis complete and email sent'
    })


if __name__ == '__main__':
    print("=" * 50)
    print("  Jenkins AI Explainer - Backend")
    print("  Running at http://localhost:5000")
    print("  Webhook at http://localhost:5000/webhook")
    print("  Open jenkins_dashboard.html in your browser")
    print("=" * 50)
    app.run(port=5000, debug=True)