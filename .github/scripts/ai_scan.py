import os
import requests
import glob
from datetime import datetime

API_URL = "https://api-inference.huggingface.co/models/deepseek-ai/deepseek-coder-6.7b-instruct"
headers = {
    "Authorization": f"Bearer {os.getenv('HF_API_TOKEN')}",
    "Content-Type": "application/json"
}

def analyze_code(code):
    prompt = f"""Analyze this code for security vulnerabilities. Be specific with line numbers and CWE references.\n\n```code\n{code}\n```"""
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 500}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()
    return result[0]["generated_text"] if isinstance(result, list) else str(result)

# Prepare files
file_types = ["**/*.js", "**/*.py", "**/*.php", "**/*.cs", "**/*.html"]
markdown = f"# 🔐 AI Security Scan Summary\n\n🕒 Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

for pattern in file_types:
    for file in glob.glob(pattern, recursive=True):
        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            code = f.read()
            print(f"\n🔍 Analyzing {file}...")
            result = analyze_code(code[:3000])
            print(result)
            markdown += f"## 📄 `{file}`\n\n```\n{result.strip()}\n```\n\n---\n"

# Save Markdown summary
summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
if summary_file:
    with open(summary_file, "a", encoding="utf-8") as f:
        f.write(markdown)
