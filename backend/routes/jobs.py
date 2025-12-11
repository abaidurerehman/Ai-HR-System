from flask import Blueprint, request, jsonify
from utils.db import db
from datetime import datetime
from flask_cors import cross_origin

jobs = Blueprint("jobs", __name__)

@jobs.route("/jobs", methods=["POST"])
@cross_origin()
def create_job():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON payload provided"}), 400

        required_fields = ["title", "skills", "description", "hr_email"]
        missing_fields = [field for field in required_fields if not data.get(field)]
        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        hr_email = data["hr_email"]

        # Fetch HR/admin from users collection
        hr_doc = db.users.find_one({"email": hr_email})
        if not hr_doc:
            return jsonify({"error": "HR/Admin not found"}), 404

        job_doc = {
            "title": data["title"],
            "skills": data["skills"],
            "description": data["description"],
            "experience": data.get("experience", ""),
            "created_by": hr_email,                  # link HR/admin
            "company_name": hr_doc.get("company_name", "Our Company"),  # fetch company name
            "created_at": datetime.utcnow()
        }

        result = db.jobs.insert_one(job_doc)
        return jsonify({
            "message": "Job created successfully",
            "job_id": str(result.inserted_id),
            "company_name": job_doc["company_name"]
        }), 201

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Failed to create job: {str(e)}"}), 500


@jobs.route("/jobs", methods=["GET"])
@cross_origin()
def list_jobs():
    try:
        jobs_list = list(db.jobs.find().sort("created_at", -1))
        for job in jobs_list:
            job["_id"] = str(job["_id"])
        return jsonify(jobs_list), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Failed to fetch jobs: {str(e)}"}), 500
