import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { ToastContainer, toast, Slide } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import "../app.css";

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  // 🌈 Custom glass toast style
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

  const handleLogin = async () => {
    if (!email || !password) {
      toast.warn("⚠️ Please fill in all fields!", {
        position: "top-center",
        style: toastStyle,
        transition: Slide,
      });
      return;
    }

    setLoading(true);
    try {
      const res = await axios.post("http://127.0.0.1:5000/api/login", {
        email,
        password,
      });

      toast.success("✅ Login successful!", {
        position: "top-center",
        style: toastStyle,
        transition: Slide,
      });

      localStorage.setItem("email", res.data.email);
      localStorage.setItem("company_name", res.data.company_name);

      setTimeout(() => navigate("/postjob"), 1000);
    } catch (err) {
      console.error(err.response?.data || err);
      toast.error(err.response?.data?.error || "❌ Login failed!", {
        position: "top-center",
        style: toastStyle,
        transition: Slide,
      });
    } finally {
      setLoading(false);
    }
  };

  const handleForgotPassword = async () => {
    if (!email) {
      toast.info("✉️ Please enter your registered email first!", {
        position: "top-center",
        style: toastStyle,
        transition: Slide,
      });
      return;
    }

    setLoading(true);
    try {
      const res = await axios.post("http://127.0.0.1:5000/api/forgot-password", {
        email,
      });
      toast.success(res.data.message, {
        position: "top-center",
        style: toastStyle,
        transition: Slide,
      });
    } catch (err) {
      console.error(err.response?.data || err);
      toast.error(err.response?.data?.error || "❌ Password recovery failed!", {
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
        <h1 className="auth-title">Login</h1>

        <div className="auth-form">
          <input
            type="email"
            placeholder="Enter Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <input
            type="password"
            placeholder="Enter Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button
            onClick={handleLogin}
            className="auth-btn"
            disabled={loading}
          >
            {loading ? "Logging in..." : "Login"}
          </button>

          <button
            onClick={handleForgotPassword}
            className="auth-btn"
            style={{
              marginTop: "10px",
              background: "linear-gradient(90deg, #1e3a8a, #2563eb)",
            }}
            disabled={loading}
          >
            {loading ? "Sending..." : "Forgot Password?"}
          </button>
        </div>

        <p className="auth-footer">
          Don’t have an account? <a href="/signup">Signup</a>
        </p>
      </div>
    </div>
  );
}
