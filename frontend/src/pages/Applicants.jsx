import { useState } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import "../app.css";
import InterviewPanel from "./interviewpanel"; 

export default function Applicants() {
  const { jobId } = useParams();
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a resume first!");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append("resume", file);

    try {
      const res = await axios.post(
        `http://127.0.0.1:5000/api/upload-resume/${jobId}`,
        formData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
      console.log("[INFO] Upload response:", res.data);
      setResult(res.data);
    } catch (err) {
      console.error("[ERROR][Upload]", err.response?.data || err);
      alert(err.response?.data?.error || "Upload failed! Check console for details.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="applicants-container">
      <div className="applicants-card">
        <h1 className="applicants-title">📄 Upload & Analyze Resume</h1>

        <div className="applicants-form">
          <input
            type="file"
            accept=".pdf,.docx"
            onChange={(e) => setFile(e.target.files[0])}
            className="file-input"
          />
          <button
            onClick={handleUpload}
            disabled={loading}
            className={`upload-btn ${loading ? "disabled" : ""}`}
          >
            {loading ? "Uploading..." : "Upload & Analyze"}
          </button>
        </div>

        {result && (
          <>
            <div className="result-card">
              <h2>Analysis Result</h2>
              <div className="result-box">
                <p><strong>Fit Score:</strong> {result.fit_score}</p>
                <p><strong>Skills Summary:</strong> {result.summary}</p>
              </div>
            </div>

            {/* ✅ Show InterviewPanel only if fit_score > 85 */}
            <InterviewPanel
              candidate={{
                name: result.candidate_name,
                email: result.candidate_email,
                fitScore: result.fit_score,
              }}
              companyName={result.company_name || "Our Company"} // Pass actual company name
            />
          </>
        )}
      </div>

      <p className="file-info">
        Supported formats: <strong>PDF</strong>, <strong>DOCX</strong>
      </p>

      {loading && (
        <div className="glass-overlay">
          <div className="loader"></div>
          <p className="loading-text">Analyzing Resume with AI...</p>
        </div>
      )}
    </div>
  );
}
