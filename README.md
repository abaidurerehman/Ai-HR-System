# AI Recruitment Assistant  
### AI-Powered Job Description Generator, Job Posting System & Resume Fit Score Analyzer

This project is a complete AI-powered recruitment system built with:

- Frontend: React  
- Backend: Flask  
- Database: MongoDB  
- AI Model: Google Gemini API  
- Resume Parsing: PDF/DOCX extraction  
- Fit Score: AI matching model  

The system allows you to:

- Generate job descriptions using AI  
- Create and save job posts  
- Upload resumes for a selected job  
- Analyze resumes & calculate fit score  
- Store applicants in MongoDB  
- View job listings & applicant details  

---

## Features

### 1. AI Job Description Generator
Enter title + skills + experience, and AI generates a professional JD.

### 2. Post Job
Save job posts into MongoDB.

### 3. Resume Upload
Upload PDF or DOCX resumes for any job.

### 4. AI Fit Score Analysis
AI evaluates resume vs job description and returns:
- Fit Score (0–1)
- Skills Summary
- Missing Skills

### 5. Applicants List
View all applicants with their fit scores.

---

## Project Structure

```

project/
│── backend/
│   ├── app.py
│   ├── jobs.py
│   ├── ai.py
│   ├── applicants.py
│   ├── utils/
│   │   └── db.py
│   ├── uploads/
│   ├── requirements.txt
│
│── frontend/
│   ├── src/
│   │   ├── PostJob.jsx
│   │   ├── Applicants.jsx
│   │   ├── JobList.jsx
│   │   ├── app.css
│
│── README.md

```

---

## Backend Setup (Flask)

### 1. Create virtual environment

```

cd backend
python -m venv venv

```

Activate:

Windows:
```

venv/Scripts/activate

```

Linux/Mac:
```

source venv/bin/activate

```

### 2. Install dependencies

```

pip install -r requirements.txt

```

### 3. Add environment variables

Create a `.env` file:

```

GEMINI_API_KEY=YOUR_API_KEY
MONGO_URI=mongodb://localhost:27017/ai_recruitment

```

### 4. Run backend

```

python app.py

```

Backend runs at:
```

[http://127.0.0.1:5000](http://127.0.0.1:5000)

```

---

## Frontend Setup (React)

### 1. Install dependencies

```

cd frontend
npm install

```

### 2. Run React app

```

npm start

```

Frontend runs at:
```

[http://localhost:3000](http://localhost:3000)

```

---

## API Endpoints

### POST /api/generate-jd  
Generate job description using AI.

### POST /api/jobs  
Save job post.

### GET /api/jobs  
List all jobs.

### POST /api/upload-resume/<job_id>  
Upload resume & calculate fit score.

---

## Resume Extraction

Supports:
- PDF  
- DOCX  

Tools Used:
- PyPDF2  
- python-docx  
- Google Gemini AI  

---

## Fit Score Calculation

AI returns a score and summary, for example:

```

{
"score": 0.82,
"summary": "Strong skills in Python, ML, NLP"
}

```

---

## CORS + Error Handling

All routes include:
- CORS enabled
- JSON validation
- Error logging
- MongoDB ObjectId validation

---

## Future Improvements

- Candidate Matching Dashboard  
- Job Recommendation System  
- AI Interview Question Generator  
- Skill Gap Analysis  

---

## Author

Abaidur-E-Rehman  
AI Engineer & Machine Learning Developer
