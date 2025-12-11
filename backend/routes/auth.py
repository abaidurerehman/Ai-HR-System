from flask import Blueprint, request, jsonify
from utils.db import users_collection
from email.mime.text import MIMEText
import smtplib, os
from dotenv import load_dotenv

load_dotenv()
auth = Blueprint("auth", __name__)

def send_email(to_email, subject, body):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        return True
    except Exception as e:
        print("❌ Email sending error:", e)
        return False

@auth.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    company_name = data.get("company_name")

    if not email or not password or not company_name:
        return jsonify({"error": "All fields are required"}), 400

    existing_user = users_collection.find_one({"email": email, "company_name": company_name, "password": password})
    if existing_user:
        return jsonify({"error": "This user already exists with same details!"}), 400

    users_collection.insert_one({"email": email, "password": password, "company_name": company_name})
    return jsonify({"message": "Signup successful!"}), 201

@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = users_collection.find_one({"email": email, "password": password})
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    return jsonify({"message": "Login successful!", "email": user["email"], "company_name": user.get("company_name", "")}), 200

@auth.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"error": "Email is required"}), 400

    user = users_collection.find_one({"email": email})
    if not user:
        return jsonify({"error": "No account found with this email"}), 404

    password = user.get("password", "")
    subject = "Your Password Recovery - AI HR System"
    body = f"Dear User,\n\nYour registered password is: {password}\n\nPlease keep it safe."

    if send_email(email, subject, body):
        return jsonify({"message": "Password has been sent to your registered email."}), 200
    else:
        return jsonify({"error": "Failed to send email. Please try again later."}), 500
