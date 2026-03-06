from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Replace with your actual Groq API Key [cite: 130]
GROQ_API_KEY = "your_gsk_key_here"
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def call_groq(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    body = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    try:
        response = requests.post(GROQ_URL, json=body, headers=headers)
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"API Error: {str(e)}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate_campaign", methods=["POST"])
def generate_campaign():
    product = request.form.get("product")
    audience = request.form.get("audience")
    platform = request.form.get("platform")
    prompt = f"Generate a detailed marketing campaign for {product} targeting {audience} on {platform}."
    return jsonify({"result": call_groq(prompt)})

@app.route("/generate_pitch", methods=["POST"])
def generate_pitch():
    product = request.form.get("product")
    customer = request.form.get("customer")
    prompt = f"Create a 30-second sales pitch and value prop for {product} targeting {customer}."
    return jsonify({"result": call_groq(prompt)})

@app.route("/lead_score", methods=["POST"])
def lead_score():
    name = request.form.get("name")
    budget = request.form.get("budget")
    need = request.form.get("need")
    urgency = request.form.get("urgency")
    prompt = f"Score this lead (0-100) for {name}. Budget: {budget}, Need: {need}, Urgency: {urgency}. Provide reasoning."
    return jsonify({"result": call_groq(prompt)})

if __name__ == "__main__":
    app.run(debug=True)