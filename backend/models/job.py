from bson import ObjectId

def job_serializer(job):
    return {
        "id": str(job["_id"]),
        "title": job["title"],
        "description": job["description"],
        "skills": job["skills"],
        "created_at": job["created_at"]
    }
