from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def explain_failure(job_name, build_number, log_text):
    print("Sending log to Groq for analysis...")

    prompt = f"""
You are a DevOps expert. A Jenkins CI/CD pipeline has failed.
Analyze the build log below and respond in this EXACT format:

JOB NAME: {job_name}
BUILD NUMBER: #{build_number}

CAUSE:
(1-2 sentences explaining what went wrong and why, in simple language)

FIX:
(1-3 clear numbered steps the developer should take to fix it)

FAILED STEP:
(the exact step name or command that failed)

Rules:
- Keep language simple, avoid deep jargon
- Be direct and specific
- If you cannot determine the cause, say so clearly

--- BUILD LOG START ---
{log_text}
--- BUILD LOG END ---
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024
    )

    explanation = response.choices[0].message.content
    print("Groq analysis complete.")
    return explanation