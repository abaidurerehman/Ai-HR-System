from flask import Flask, jsonify
from flask_cors import CORS
from flask_mail import Mail
from routes.ai import ai
from routes.applicants import applicants
from routes.jobs import jobs
from routes.auth import auth
from dotenv import load_dotenv
import os
import google.generativeai as genai

# ---------------- Load Environment FIRST ----------------
load_dotenv()

# ---------------- Flask App Setup ----------------
app = Flask(__name__)
CORS(app)

# ---------------- Flask-Mail Config ----------------
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")

mail = Mail(app)
app.extensions["mail"] = mail  # accessible via current_app.extensions['mail']

# ---------------- Gemini Setup ----------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

print("\n" + "="*50)
print("🚀 AI HR System - Startup Configuration")
print("="*50)

# Check GEMINI_API_KEY
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    print(f"✅ Gemini API Key: Loaded (starts with: {GEMINI_API_KEY[:15]}...)")
else:
    print("❌ GEMINI_API_KEY: NOT FOUND")
    print("   Please check your .env file")

# Check Mail Configuration
if app.config["MAIL_USERNAME"]:
    print(f"✅ Mail Username: {app.config['MAIL_USERNAME']}")
else:
    print("❌ MAIL_USERNAME: NOT FOUND")

if app.config["MAIL_PASSWORD"]:
    print(f"✅ Mail Password: Loaded (length: {len(app.config['MAIL_PASSWORD'])} chars)")
else:
    print("❌ MAIL_PASSWORD: NOT FOUND")

print("="*50 + "\n")

# ---------------- Register Blueprints ----------------
app.register_blueprint(jobs, url_prefix="/api")
app.register_blueprint(applicants, url_prefix="/api")
app.register_blueprint(ai, url_prefix="/api")
app.register_blueprint(auth, url_prefix="/api")

print("📋 Registered Routes:")
print("-" * 50)
for rule in app.url_map.iter_rules():
    if rule.endpoint != 'static':
        print(f"  {rule.methods} {rule.rule} -> {rule.endpoint}")
print("-" * 50 + "\n")

# ---------------- Health Route ----------------
@app.route("/")
def home():
    return jsonify({
        "message": "AI HR System backend is running",
        "status": "healthy",
        "gemini_configured": bool(GEMINI_API_KEY),
        "mail_configured": bool(app.config["MAIL_USERNAME"] and app.config["MAIL_PASSWORD"])
    }), 200

@app.route("/api/health")
def health_check():
    """Detailed health check endpoint"""
    return jsonify({
        "status": "running",
        "gemini_api": "configured" if GEMINI_API_KEY else "missing",
        "mail_service": "configured" if app.config["MAIL_USERNAME"] else "missing",
        "routes": {
            "jobs": "registered",
            "applicants": "registered",
            "ai": "registered",
            "auth": "registered"
        }
    }), 200


if __name__ == "__main__":
    print("🌐 Starting Flask server on http://localhost:5000")
    print("📍 API endpoints available at /api/*")
    print("\n")
    app.run(host="0.0.0.0", port=5000, debug=True)