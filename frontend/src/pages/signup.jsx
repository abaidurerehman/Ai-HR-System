import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { ToastContainer, toast, Slide } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "../app.css";

export default function Signup() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [companyName, setCompanyName] = useState("");
  const [loading, setLoading] = useState(false);

  // 🌈 Custom glass toast style (matches Login.jsx)
  const toastStyle = {
    background: "rgba(15, 23, 42, 0.85)",
    backdropFilter: "blur(12px)",
    border: "1px solid rgba(255, 255, 255, 0.15)",
    color: "#f1f5f9",
    borderRadius: "16px",
    fontSize: "0.95rem",
    textAlign: "center",
    boxShadow: "0 4px 30px rgba(0,0,0,0.3)",
  };

  const handleSignup = async () => {
    if (!email || !password || !companyName) {
      toast.warn("⚠️ All fields are required!", {
        position: "top-center",
        style: toastStyle,
        transition: Slide,
      });
      return;
    }

    setLoading(true);
    try {
      const res = await axios.post("http://127.0.0.1:5000/api/signup", {
        email,
        password,
        company_name: companyName,
      });

      toast.success("✅ Signup successful! Redirecting to login...", {
        position: "top-center",
        style: toastStyle,
        transition: Slide,
      });

      setTimeout(() => navigate("/login"), 1500);
    } catch (err) {
      console.error(err.response?.data || err);
      toast.error(err.response?.data?.error || "❌ Signup failed!", {
        position: "top-center",
        style: toastStyle,
        transition: Slide,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      {/* 🌌 Toast Notification Container */}
      <ToastContainer
        limit={3}
        autoClose={3500}
        hideProgressBar
        newestOnTop
        closeOnClick
        pauseOnHover={false}
        draggable
      />

      <div className="auth-card">
        <h1 className="auth-title">Create Account</h1>

        <div className="auth-form">
          <input
            type="text"
            placeholder="Company Name"
            value={companyName}
            onChange={(e) => setCompanyName(e.target.value)}
          />
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button
            onClick={handleSignup}
            className="auth-btn"
            disabled={loading}
          >
            {loading ? "Signing up..." : "Signup"}
          </button>
        </div>

        <p className="auth-footer">
          Already have an account? <a href="/login">Login</a>
        </p>
      </div>
    </div>
  );
}
