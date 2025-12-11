from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from utils.db import db
from datetime import datetime
import os, json, PyPDF2, docx, re, traceback
import google.generativeai as genai
from bson import ObjectId
from flask_mail import Message
import dotenv

dotenv.load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

applicants = Blueprint("applicants", __name__)

UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
ALLOWED_EXTENSIONS = {"pdf", "docx"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_text(file_path):
    ext = file_path.rsplit(".", 1)[1].lower()
    text = ""
    try:
        if ext == "pdf":
            with open(file_path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + " "
        elif ext == "docx":
            doc = docx.Document(file_path)
            for para in doc.paragraphs:
                text += para.text + " "
        return text.strip()
    except Exception as e:
        print("[ERROR][extract_text]", e)
        return ""

def send_email(mail, recipient, subject, body):
    try:
        msg = Message(subject, sender=current_app.config["MAIL_USERNAME"], recipients=[recipient])
        msg.body = body
        mail.send(msg)
    except Exception as e:
        print("[ERROR][send_email]", e)

@applicants.route("/upload-resume/<job_id>", methods=["POST"])
def upload_resume(job_id):
    try:
        if "resume" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["resume"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        if not allowed_file(file.filename):
            return jsonify({"error": f"File type not allowed. Allowed: {ALLOWED_EXTENSIONS}"}), 400

        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        resume_text = extract_text(file_path)
        if not resume_text.strip():
            return jsonify({"fit_score": 0, "summary": "Parsing failed (no text found)"}), 200

        job = db.jobs.find_one({"_id": ObjectId(job_id)})
        if not job:
            return jsonify({"error": "Job not found"}), 404
        job_desc = job.get("description", "")
        job_title = job.get("title", "the position")
        created_by = job.get("created_by")  # HR/admin email

        # Fetch company name from HR/admin
        company_name = "Our Company"
        if created_by:
            hr_doc = db.users.find_one({"email": created_by})
            if hr_doc and hr_doc.get("company_name"):
                company_name = hr_doc["company_name"]

        analysis_result = {
            "fit_score": 0,
            "summary": "Parsing failed",
            "education": [],
            "skills": [],
            "experience": [],
            "projects": [],
            "weak_areas": [],
            "recommendations": [],
            "candidate_name": "",
            "candidate_email": ""
        }

        # ----------- Gemini Resume Analysis -----------
        try:
            prompt = f"""
You are an AI HR assistant. Analyze this resume against the job description.
Return ONLY a valid JSON like this:
{{
  "fit_score": <float 0-1>,
  "summary": "<short professional summary>",
  "education": ["<degree/institution>"],
  "skills": ["<skill1>", "<skill2>"],
  "experience": ["<role1>", "<role2>"],
  "projects": ["<project1>", "<project2>"],
  "weak_areas": ["<weak1>", "<weak2>"],
  "recommendations": ["<rec1>", "<rec2>"],
  "candidate_name": "<full name if available>",
  "candidate_email": "<email if available>"
}}
Job Description:
{job_desc}
Resume Text:
{resume_text}
"""
            model = genai.GenerativeModel("models/gemini-2.5-pro")
            response = model.generate_content(prompt)
            raw_text = response.text.strip()
            match = re.search(r"\{.*\}", raw_text, re.DOTALL)
            if match:
                result = json.loads(match.group(0))
                for key in analysis_result.keys():
                    if key in result:
                        analysis_result[key] = result[key]
        except Exception as e:
            print("[ERROR][Gemini AI parsing]", e)
            traceback.print_exc()

        applicant = {
            "job_id": job_id,
            "filename": filename,
            "resume_text": resume_text,
            "fit_score": analysis_result["fit_score"],
            "skills_summary": analysis_result["summary"],
            "education": analysis_result.get("education", []),
            "skills": analysis_result.get("skills", []),
            "experience": analysis_result.get("experience", []),
            "projects": analysis_result.get("projects", []),
            "weak_areas": analysis_result.get("weak_areas", []),
            "recommendations": analysis_result.get("recommendations", []),
            "candidate_name": analysis_result.get("candidate_name", ""),
            "candidate_email": analysis_result.get("candidate_email", ""),
            "uploaded_at": datetime.utcnow(),
        }
        applicant_id = db.applicants.insert_one(applicant).inserted_id

        # ----------- Send Email based on Fit Score -----------
        mail = current_app.extensions.get("mail")
        candidate_email = analysis_result.get("candidate_email")
        if not candidate_email:
            email_match = re.search(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", resume_text)
            candidate_email = email_match.group(0) if email_match else None

        if candidate_email:
            candidate_name = analysis_result.get("candidate_name", "Candidate")
            if analysis_result["fit_score"] < 0.85:
                # Rejection email sent automatically
                email_msg = f"""
Generate ONLY a professional, polite, and encouraging rejection email for {candidate_name} 
who applied for the {job_title} position at {company_name}.
Mention that they scored {analysis_result['fit_score']*100:.2f}% in the initial screening.
Do NOT include any extra commentary or mention AI generation.
Return ONLY the email text.
"""
                try:
                    model = genai.GenerativeModel("models/gemini-2.5-pro")
                    email_response = model.generate_content(email_msg)
                    polite_reply = email_response.text.strip()
                    polite_reply = re.sub(r"^(Of course.*?email\.?)\s*", "", polite_reply, flags=re.IGNORECASE)
                    email_subject = f"Application Update for {job_title} at {company_name}"
                    send_email(mail, candidate_email, email_subject, polite_reply)
                except Exception as e:
                    print("[ERROR][send rejection email]", e)
            else:
                # Score >= 85% → do not send invitation automatically
                # HR/admin must schedule date/time and send invitation manually
                print(f"[INFO] Candidate {candidate_name} scored {analysis_result['fit_score']*100:.2f}%. Awaiting HR scheduling.")

        return jsonify({
            "message": "Resume analyzed successfully",
            "fit_score": round(analysis_result["fit_score"] * 100, 2),
            "summary": analysis_result["summary"],
            "education": analysis_result["education"],
            "skills": analysis_result["skills"],
            "experience": analysis_result["experience"],
            "projects": analysis_result["projects"],
            "weak_areas": analysis_result["weak_areas"],
            "recommendations": analysis_result["recommendations"],
            "candidate_name": analysis_result.get("candidate_name", ""),
            "candidate_email": analysis_result.get("candidate_email", ""),
            "applicant_id": str(applicant_id)
        }), 201

    except Exception as e:
        print("[ERROR][upload_resume]", e)
        traceback.print_exc()
        return jsonify({"error": "Failed to upload/analyze resume", "details": str(e)}), 500
