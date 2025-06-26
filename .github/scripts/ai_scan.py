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

# Collect files
file_types = ["**/*.js", "**/*.py", "**/*.php", "**/*.cs", "**/*.html"]
report_entries = []

print("📦 Scanning source files for vulnerabilities...\n")

for pattern in file_types:
    for file in glob.glob(pattern, recursive=True):
        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            code = f.read()
            print(f"\n🔍 Analyzing {file}...")
            result = analyze_code(code[:3000])  # Truncate large files
            print(result)
            report_entries.append((file, result))

# Generate HTML report
html = f"""<!DOCTYPE html>
<html>
<head>
    <title>AI Security Report</title>
    <style>
        body {{ font-family: Arial; padding: 20px; background: #f9f9f9; }}
        h1 {{ color: #c0392b; }}
        .file-report {{ margin-bottom: 30px; padding: 15px; background: #fff; border-radius: 8px; box-shadow: 0 0 5px rgba(0,0,0,0.1); }}
        pre {{ background: #f4f4f4; padding: 10px; overflow-x: auto; }}
    </style>
</head>
<body>
<h1>🔐 AI Security Scan Report</h1>
<p>Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
"""

for filename, result in report_entries:
    html += f"""
    <div class="file-report">
        <h2>📁 {filename}</h2>
        <pre>{result}</pre>
    </div>
    """

html += "</body></html>"

# Save HTML report
os.makedirs("output", exist_ok=True)
with open("output/ai-security-report.html", "w", encoding="utf-8") as report_file:
    report_file.write(html)

print("\n✅ HTML report generated at output/ai-security-report.html")
