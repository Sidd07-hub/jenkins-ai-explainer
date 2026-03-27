import requests
import os
from dotenv import load_dotenv
 
load_dotenv()
 
 
def get_failed_build_log(job_name, jenkins_url=None, jenkins_user=None, jenkins_token=None):
    url   = jenkins_url  or os.getenv("JENKINS_URL")
    user  = jenkins_user or os.getenv("JENKINS_USER")
    token = jenkins_token or os.getenv("JENKINS_TOKEN")
 
    auth = (user, token)
 
    # Step 1: get last failed build info
    job_url = f"{url}/job/{job_name}/lastFailedBuild/api/json"
 
    try:
        response = requests.get(job_url, auth=auth, timeout=10)
    except requests.exceptions.ConnectionError:
        print("Cannot reach Jenkins. Is it running?")
        return None, None
 
    if response.status_code == 404:
        print(f"No failed build found for job: {job_name}")
        return None, None
 
    if response.status_code == 401:
        print("Unauthorized. Check your Jenkins username and API token.")
        return None, None
 
    if response.status_code != 200:
        print(f"Error connecting to Jenkins: {response.status_code}")
        return None, None
 
    build_data   = response.json()
    build_number = build_data.get("number")
 
    # Step 2: fetch the console log
    log_url      = f"{url}/job/{job_name}/{build_number}/consoleText"
    log_response = requests.get(log_url, auth=auth, timeout=10)
 
    if log_response.status_code != 200:
        print(f"Could not fetch log: {log_response.status_code}")
        return None, None
 
    # Return last 100 lines to save Claude tokens
    full_log      = log_response.text
    last_100_lines = "\n".join(full_log.splitlines()[-100:])
 
    print(f"Fetched build #{build_number} log for job: {job_name}")
    return build_number, last_100_lines