from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY") 
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def call_groq(prompt):
    """Utility function to communicate with Groq API"""
    if not GROQ_API_KEY:
        return "Error: GROQ_API_KEY not found in .env file."

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    body = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": "You are a professional marketing and sales assistant. Provide structured, actionable advice."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    
    try:
        response = requests.post(GROQ_URL, json=body, headers=headers)
        response.raise_for_status() # Check for HTTP errors (401, 404, 500, etc.)
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")
        return f"Connection Error: Could not reach Groq API."
    except Exception as e:
        print(f"General Error: {e}")
        return f"System Error: {str(e)}"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate_campaign", methods=["POST"])
def generate_campaign():
    product = request.form.get("product")
    audience = request.form.get("audience")
    platform = request.form.get("platform")
    
    prompt = (f"Generate a professional marketing strategy for {product}.\n"
              f"Target Audience: {audience}\n"
              f"Platform: {platform}\n\n"
              "Please provide: Campaign objectives, 5 content ideas, 3 ad copy variations, and CTAs.")
    
    result = call_groq(prompt)
    return jsonify({"result": result})

@app.route("/generate_pitch", methods=["POST"])
def generate_pitch():
    product = request.form.get("product")
    customer = request.form.get("customer")
    
    prompt = (f"Create a high-converting sales pitch for {product}.\n"
              f"Customer Persona: {customer}\n\n"
              "Include: 30-second elevator pitch, value proposition, and differentiators.")
    
    result = call_groq(prompt)
    return jsonify({"result": result})

@app.route("/lead_score", methods=["POST"])
def lead_score():
    name = request.form.get("name")
    budget = request.form.get("budget")
    need = request.form.get("need")
    urgency = request.form.get("urgency")
    
    prompt = (f"Analyze this lead: {name}\n"
              f"Budget: {budget}\n"
              f"Need: {need}\n"
              f"Urgency: {urgency}\n\n"
              "Provide a score (0-100), reasoning, and conversion probability.")
    
    result = call_groq(prompt)
    return jsonify({"result": result})

if __name__ == "__main__":
    # Check if API key exists on startup
    if not GROQ_API_KEY:
        print("WARNING: GROQ_API_KEY is missing! Check your .env file.")
    app.run(debug=True)
