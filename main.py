from log_collector import get_failed_build_log
from ai_explainer import explain_failure
from email_sender import send_failure_email
import os
from dotenv import load_dotenv
 
load_dotenv()
 
# ── Configure these if running without the dashboard ──
JENKINS_URL   = os.getenv("JENKINS_URL", "http://localhost:8080")
JENKINS_USER  = os.getenv("JENKINS_USER", "admin")
JENKINS_TOKEN = os.getenv("JENKINS_TOKEN", "")
JOB_NAME      = "your-jenkins-job-name"   # change this to your job name
 
 
def run():
    print("=" * 50)
    print("  Jenkins AI Failure Explainer")
    print("=" * 50)
 
    # Step 1: fetch the failed build log
    build_number, log_text = get_failed_build_log(
        JOB_NAME, JENKINS_URL, JENKINS_USER, JENKINS_TOKEN
    )
 
    if not log_text:
        print("No failed build log found. Exiting.")
        return
 
    # Step 2: send to Claude
    explanation = explain_failure(JOB_NAME, build_number, log_text)
 
    print("\n--- AI EXPLANATION ---")
    print(explanation)
    print("----------------------\n")
 
    # Step 3: send email
    send_failure_email(JOB_NAME, build_number, explanation)
 
    print("Done!")
 
 
if __name__ == "__main__":
    run()
 
