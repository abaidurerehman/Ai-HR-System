import os
import time
from flask import Blueprint, request, jsonify, current_app
from flask_mail import Message
import google.generativeai as genai

ai = Blueprint("ai", __name__)

# ---------------- Gemini Setup ----------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Validate API key on startup
if not GEMINI_API_KEY:
    print("[ERROR] GEMINI_API_KEY not found in environment variables!")
    print("[ERROR] Make sure .env file exists and contains GEMINI_API_KEY")
elif GEMINI_API_KEY.strip() == "":
    print("[ERROR] GEMINI_API_KEY is empty!")
else:
    print(f"[INFO] Gemini API key loaded successfully (first 10 chars): {GEMINI_API_KEY[:10]}...")
    genai.configure(api_key=GEMINI_API_KEY)

# ---------------- Helper Function for Safe Email ----------------
def send_email_safely(mail, msg, retries=3, delay=2):
    for attempt in range(1, retries + 1):
        try:
            mail.send(msg)
            return True
        except Exception as e:
            print(f"[WARN] Email send attempt {attempt} failed: {e}")
            if attempt < retries:
                time.sleep(delay)
            else:
                raise e

# ---------------- Job Description Generation ----------------
@ai.route("/generate-jd", methods=["POST"])
def generate_jd():
    data = request.get_json()
    title = data.get("title")
    skills = data.get("skills")
    experience = data.get("experience")

    if not title or not skills or not experience:
        return jsonify({"error": "Missing title, skills, or experience"}), 400

    prompt_text = (
        f"Generate a professional plain-text job description for {title}. "
        f"Include Job Summary, Responsibilities, and Requirements. "
        f"Required skills: {skills}. Expected experience: {experience}. "
        f"Return plain text only."
    )

    try:
        # Check if API key is configured
        if not GEMINI_API_KEY:
            return jsonify({"error": "Gemini API key not configured"}), 500
        
        print(f"[DEBUG] Using API key: {GEMINI_API_KEY[:15]}...")
        print(f"[DEBUG] Generating JD for: {title}")
        
        # ✅ Using Gemini 2.0 Flash (latest and fastest model)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(
            prompt_text,
            generation_config=genai.GenerationConfig(
                temperature=0.7,
                max_output_tokens=800
            )
        )
        jd_text = response.text
        print(f"[SUCCESS] Generated JD (length: {len(jd_text)} chars)")
        return jsonify({"description": jd_text})
    except Exception as e:
        import traceback
        print("[ERROR][generate_jd]", e)
        print(traceback.format_exc())
        return jsonify({"error": f"JD generation failed: {str(e)}"}), 500

# ---------------- Send Interview / Rejection Email ----------------
@ai.route("/send-response", methods=["POST"])
def send_response():
    data = request.json
    candidate_email = data.get("email")
    fit_score = data.get("fit_score")
    candidate_name = data.get("name")
    interview_date = data.get("interview_date")
    interview_time = data.get("interview_time")

    if not candidate_email or fit_score is None:
        return jsonify({"error": "Missing email or fit score"}), 400

    try:
        mail = current_app.extensions.get('mail')

        if float(fit_score) > 85:
            subject = "🎉 Interview Invitation - AI HR System"
            body = f"""
Dear {candidate_name},

Congratulations! Your profile has been shortlisted with a Fit Score of {fit_score}.

We'd like to invite you for an interview on:
📅 Date: {interview_date}
🕒 Time: {interview_time}

Please confirm your availability by replying to this email.

Best regards,
HR Team
"""
        else:
            subject = "Your Application Update - AI HR System"
            body = f"""
Dear {candidate_name},

Thank you for applying. Your profile scored {fit_score} in our screening. 
We appreciate your interest and encourage you to apply for future opportunities.

Best regards,
HR Team
"""

        msg = Message(subject, sender=current_app.config["MAIL_USERNAME"], recipients=[candidate_email])
        msg.body = body
        send_email_safely(mail, msg)
        return jsonify({"message": "Email sent successfully ✅"}), 200

    except Exception as e:
        print("[ERROR][send_response]", e)
        return jsonify({"error": f"Email sending failed: {e}"}), 500