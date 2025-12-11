import React, { useState, useEffect } from "react";
import "../app.css";

function InterviewPanel({ candidate, companyName = "Our Company" }) {
  const [email, setEmail] = useState(candidate?.email || "");
  const [name, setName] = useState(candidate?.name || "");
  const [fitScore, setFitScore] = useState(candidate?.fitScore || 0);
  const [interviewDate, setInterviewDate] = useState("");
  const [interviewTime, setInterviewTime] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);
  const [emailPreview, setEmailPreview] = useState("");

  useEffect(() => {
    if (fitScore <= 85) {
      setMessage(
        "❌ Candidate scored below threshold. Rejection email has been sent automatically."
      );
      setEmailPreview("");
    } else {
      setMessage("");
      setEmailPreview("");
    }
  }, [fitScore, name, interviewDate, interviewTime]);

  const generateInterviewMessage = () => {
    return `Dear ${name},

Congratulations! Your profile has been shortlisted with a Fit Score of ${fitScore}.

We'd like to invite you for an interview on:
📅 Date: ${interviewDate}
🕒 Time: ${interviewTime}

Best regards,
${companyName}`;
  };

  const sendResponse = async () => {
    if (!email || !name || !fitScore) {
      setMessage("⚠️ Please fill all required fields (Name, Email, Fit Score).");
      return;
    }

    if (fitScore > 85 && (!interviewDate || !interviewTime)) {
      setMessage(
        "⚠️ Please select interview date and time for high-fit candidates."
      );
      return;
    }

    setLoading(true);
    setMessage("⏳ Sending interview invite...");

    const emailBody = {
      email,
      name,
      fit_score: Number(fitScore),
      type: "interview",
      interview_date: interviewDate,
      interview_time: interviewTime,
      message: generateInterviewMessage(),
    };

    try {
      const response = await fetch("http://localhost:5000/api/send-response", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(emailBody),
      });

      const result = await response.json();

      if (response.ok) {
        setMessage(`✅ ${result.message}`);
      } else {
        setMessage(`❌ ${result.error || "Something went wrong"}`);
      }
    } catch (err) {
      setMessage("❌ Error connecting to backend. Check server or API URL.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="applicants-container">
      <div className="background-animation"></div>

      {loading && (
        <div className="glass-overlay">
          <div className="loader"></div>
          <div className="loading-text">Sending Response...</div>
        </div>
      )}

      <div className="applicants-card">
        <h2 className="applicants-title">Candidate Response Panel ⚙️</h2>

        <input
          type="text"
          placeholder="Candidate Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="file-input"
          disabled={fitScore <= 85}
        />
        <input
          type="email"
          placeholder="Candidate Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="file-input"
          disabled={fitScore <= 85}
        />
        <input
          type="number"
          placeholder="Fit Score"
          value={fitScore}
          className="file-input"
          disabled
        />

        {fitScore > 85 && (
          <>
            <input
              type="date"
              value={interviewDate}
              onChange={(e) => setInterviewDate(e.target.value)}
              className="file-input"
            />
            <input
              type="time"
              value={interviewTime}
              onChange={(e) => setInterviewTime(e.target.value)}
              className="file-input"
            />
          </>
        )}

        {/* ✅ Only show email preview for interview invitations */}
        {fitScore > 85 && emailPreview && (
          <div
            className="result-card"
            style={{
              background: "rgba(15, 23, 42, 0.85)",
              color: "#f1f5f9",
              maxHeight: "200px",
              overflowY: "auto",
              whiteSpace: "pre-line",
            }}
          >
            <strong>Email Preview:</strong>
            <div style={{ marginTop: "0.5rem" }}>{emailPreview}</div>
          </div>
        )}

        {/* ✅ Show button only for high-fit candidates */}
        {fitScore > 85 ? (
          <button
            onClick={sendResponse}
            disabled={loading || fitScore <= 0}
            className="upload-btn"
            style={{ marginTop: "1rem" }}
          >
            {loading ? "Sending..." : "Send Interview Invite"}
          </button>
        ) : (
          <div
            className="result-card"
            style={{
              background: "rgba(220, 38, 38, 0.85)",
              color: "#fff",
              marginTop: "1rem",
            }}
          >
            ❌ Rejection email has already been sent automatically.
          </div>
        )}

        {message && fitScore > 85 && (
          <div
            className="result-card"
            style={{
              background:
                message.startsWith("✅")
                  ? "rgba(22, 163, 74, 0.8)"
                  : message.startsWith("❌")
                  ? "rgba(220, 38, 38, 0.85)"
                  : "rgba(234, 179, 8, 0.85)",
              color: "#fff",
            }}
          >
            {message}
          </div>
        )}
      </div>
    </div>
  );
}

export default InterviewPanel;
