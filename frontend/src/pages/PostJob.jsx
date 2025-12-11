import { useState, useEffect } from "react";
import axios from "axios";
import { FiCopy } from "react-icons/fi";
import "../app.css";

export default function PostJob() {
  const [form, setForm] = useState({
    title: "",
    skills: "",
    experience: "",
    description: "",
  });
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [hrEmail, setHrEmail] = useState("");

  // Fetch logged-in HR/admin email from localStorage
  useEffect(() => {
    const email = localStorage.getItem("email");
    if (email) setHrEmail(email);
  }, []);

  const jobTitles = ["Frontend Developer", "Backend Developer", "Data Scientist", "AI Engineer", "Full Stack Developer"];
  const skillsList = ["Python", "JavaScript", "React", "Node.js", "Machine Learning", "SQL", "AWS"];
  const experienceLevels = ["0-1 years", "1-3 years", "2-5 years", "5+ years"];

  const handleGenerate = async () => {
    if (!form.title || !form.skills || !form.experience) {
      alert("Please fill title, skills, and experience first!");
      return;
    }

    setLoading(true);
    try {
      const res = await axios.post("http://127.0.0.1:5000/api/generate-jd", {
        title: form.title,
        skills: form.skills,
        experience: form.experience,
      });

      const jd = res.data.description;
      setForm({ ...form, description: jd });
      setCopied(false);
    } catch (err) {
      console.error(err.response?.data || err);
      alert(`Error generating description: ${err.response?.data?.error || "Unknown error"}`);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!form.title || !form.skills || !form.experience || !form.description) {
      alert("Please fill all fields and generate description first!");
      return;
    }

    if (!hrEmail) {
      alert("HR/Admin email not found. Please login again.");
      return;
    }

    setLoading(true);
    try {
      const res = await axios.post("http://127.0.0.1:5000/api/jobs", {
        ...form,
        hr_email: hrEmail,  // automatically sent to backend
      });

      const jobId = res.data.job_id;
      alert(`Job created successfully for ${res.data.company_name}!`);
      window.location.href = `/applicants/${jobId}`;
      setForm({ title: "", skills: "", experience: "", description: "" });
      setCopied(false);
    } catch (err) {
      console.error(err.response?.data || err);
      alert(`Error saving job: ${err.response?.data?.error || "Unknown error"}`);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = () => {
    if (!form.description) return;
    navigator.clipboard.writeText(form.description);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="container">
      <div className="form-box">
        <h1>🧠 AI Job Description Generator</h1>
        <form onSubmit={handleSubmit}>
          <input
            list="titles"
            type="text"
            placeholder="Job Title"
            value={form.title}
            onChange={(e) => setForm({ ...form, title: e.target.value })}
          />
          <datalist id="titles">{jobTitles.map((t, i) => <option key={i} value={t} />)}</datalist>

          <input
            list="skills"
            type="text"
            placeholder="Skills (comma-separated)"
            value={form.skills}
            onChange={(e) => setForm({ ...form, skills: e.target.value })}
          />
          <datalist id="skills">{skillsList.map((s, i) => <option key={i} value={s} />)}</datalist>

          <input
            list="experienceLevels"
            type="text"
            placeholder="Experience Level"
            value={form.experience}
            onChange={(e) => setForm({ ...form, experience: e.target.value })}
          />
          <datalist id="experienceLevels">{experienceLevels.map((exp, i) => <option key={i} value={exp} />)}</datalist>

          <div className="flex justify-between items-center mt-4">
            <button type="button" onClick={handleGenerate} disabled={loading} className="generate-btn">
              {loading ? "Generating..." : "✨ Generate Description"}
            </button>
            <button type="submit" className="save-btn">Save Job</button>
          </div>
        </form>
      </div>

      <div className="description-box">
        <h2>Job Description Preview</h2>
        <div
          className="description-content"
          style={{
            position: "relative",
            maxHeight: "300px",
            overflowY: "auto",
            padding: "1rem",
            border: "1px solid #ddd",
            borderRadius: "8px",
            background: "#fafafa",
            fontFamily: "Arial, sans-serif",
            fontSize: "0.95rem",
            lineHeight: "1.5",
            whiteSpace: "pre-wrap"
          }}
        >
          {form.description ? (
            <>
              <p>{form.description}</p>
              <button
                onClick={handleCopy}
                title="Copy to clipboard"
                style={{
                  position: "absolute",
                  top: "10px",
                  right: "10px",
                  background: "#4CAF50",
                  border: "none",
                  borderRadius: "50%",
                  padding: "8px",
                  cursor: "pointer",
                  color: "white",
                  boxShadow: "0 2px 5px rgba(0,0,0,0.2)",
                  transition: "transform 0.2s",
                  zIndex: 10
                }}
                onMouseOver={(e) => (e.currentTarget.style.transform = "scale(1.1)")}
                onMouseOut={(e) => (e.currentTarget.style.transform = "scale(1)")}
              >
                <FiCopy size={18} />
              </button>
              {copied && (
                <span style={{ position: "absolute", top: "12px", right: "50px", color: "green", fontWeight: "bold" }}>
                  Copied!
                </span>
              )}
            </>
          ) : (
            <p className="description-placeholder">Your generated job description will appear here...</p>
          )}
        </div>
      </div>
    </div>
  );
}
