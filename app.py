# import os
# import json
# from flask import Flask, request, render_template, jsonify
# import requests
# from dotenv import load_dotenv

# load_dotenv()

# app = Flask(__name__)

# API_KEY = os.getenv("OPENROUTER_API_KEY")  # For OpenRouter.ai
# API_URL = "https://openrouter.ai/api/v1/chat/completions"

# HEADERS = {
#     "Authorization": f"Bearer {API_KEY}",
#     "Content-Type": "application/json"
# }

# def evaluate_with_llm(idea):
#     prompt = f"""
# You are an innovation evaluation AI. Evaluate this idea based on:
# - Feasibility (30%)
# - Impact (30%)
# - Originality (25%)
# - SDG Alignment (15%)

# Return a valid JSON:
# {{
#   "Feasibility": {{"score": 0-10, "justification": "..."}},
#   "Impact": {{"score": 0-10, "justification": "..."}},
#   "Originality": {{"score": 0-10, "justification": "..."}},
#   "SDG Alignment": {{"score": 0-10, "justification": "..."}},
#   "Total": 0-10,
#   "Verdict": "...",
#   "Suggestions": "..."
# }}

# Idea:
# Title: {idea['title']}
# Problem: {idea['problem_statement']}
# Solution: {idea['solution_overview']}
# Market: {idea['target_market']}
# Feasibility: {idea['feasibility']}
# Innovation Summary: {idea['innovation_summary']}
# SDG Linkage: {idea['sdg_linkage']}
#     """

#     payload = {
#         "model": "openai/gpt-3.5-turbo",
#         "messages": [
#             {"role": "system", "content": "You are a smart, fair, and supportive evaluator of innovative ideas."},
#             {"role": "user", "content": prompt}
#         ],
#         "temperature": 0.4
#     }

#     try:
#         res = requests.post(API_URL, headers=HEADERS, json=payload)
#         content = res.json()["choices"][0]["message"]["content"]
#         return json.loads(content)
#     except Exception as e:
#         return {"error": "Failed to evaluate idea", "details": str(e)}

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/evaluate', methods=['POST'])
# def evaluate():
#     data = request.get_json()
#     result = evaluate_with_llm(data)
#     return jsonify(result)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))


import os
import json
from flask import Flask, request, render_template, jsonify
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def evaluate_with_llm(idea):
    prompt = f"""
You are an innovation evaluation AI. Evaluate this idea based on:
- Feasibility (30%)
- Impact (30%)
- Originality (25%)
- SDG Alignment (15%)

Return a valid JSON:
{{
  "Feasibility": {{"score": 0-10, "justification": "..."}},
  "Impact": {{"score": 0-10, "justification": "..."}},
  "Originality": {{"score": 0-10, "justification": "..."}},
  "SDG Alignment": {{"score": 0-10, "justification": "..."}},
  "Total": 0-10,
  "Verdict": "...",
  "Suggestions": "..."
}}

Idea:
Title: {idea['title']}
Problem: {idea['problem_statement']}
Solution: {idea['solution_overview']}
Market: {idea['target_market']}
Feasibility: {idea['feasibility']}
Innovation Summary: {idea['innovation_summary']}
SDG Linkage: {idea['sdg_linkage']}
    """

    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a smart, fair, and supportive evaluator of innovative ideas."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4
    }

    try:
        res = requests.post(API_URL, headers=HEADERS, json=payload)
        res.raise_for_status()
        raw_content = res.json()["choices"][0]["message"]["content"].strip()
        print("Raw LLM response:\n", raw_content)  # for debugging

        try:
            return json.loads(raw_content)
        except json.JSONDecodeError as je:
            return {
                "error": "Invalid JSON returned from model",
                "details": str(je),
                "raw": raw_content
            }

    except Exception as e:
        return {"error": "Failed to evaluate idea", "details": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400
    result = evaluate_with_llm(data)
    return jsonify(result)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
