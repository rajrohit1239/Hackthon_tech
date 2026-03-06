from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)
GROQ_API_KEY = os.getenv("GROQ_API_KEY") 
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def call_groq(prompt):
    """Utility function to communicate with Groq API [cite: 133, 143]"""
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
    """Renders the main dashboard [cite: 161]"""
    return render_template("index.html")

@app.route("/generate_campaign", methods=["POST"])
def generate_campaign():
    """Handles Marketing Campaign Generation [cite: 164, 221]"""
    product = request.form.get("product")
    audience = request.form.get("audience")
    platform = request.form.get("platform")
    prompt = (f"Generate a comprehensive marketing strategy for {product}. "
              f"Target Audience: {audience}. Platform: {platform}. "
              "Include: campaign objectives, 5 targeted content ideas, "
              "3 variations of compelling ad copy, and specific call-to-action suggestions.")
    
    result = call_groq(prompt)
    return jsonify({"result": result})

@app.route("/generate_pitch", methods=["POST"])
def generate_pitch():
    """Handles Sales Pitch Generation [cite: 187, 236]"""
    product = request.form.get("product")
    customer = request.form.get("customer")
    prompt = (f"Create a personalized sales pitch for {product}. "
              f"Customer Persona: {customer}. "
              "Include: a 30-second elevator pitch, clear value proposition, "
              "key differentiators, and a strategic call-to-action.")
    
    result = call_groq(prompt)
    return jsonify({"result": result})

@app.route("/lead_score", methods=["POST"])
def lead_score():
    """Handles Lead Qualification and Scoring [cite: 197, 258]"""
    name = request.form.get("name")
    budget = request.form.get("budget")
    need = request.form.get("need")
    urgency = request.form.get("urgency")
    
    prompt = (f"Analyze and score this lead: {name}. "
              f"Budget: {budget}. Need: {need}. Urgency: {urgency}. "
              "Provide: A quantified score (0-100), detailed reasoning for the score, "
              "and probability of conversion assessment.")
    
    result = call_groq(prompt)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)
