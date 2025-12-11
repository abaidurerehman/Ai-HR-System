import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Signup from "./pages/signup";
import Login from "./pages/login";
import PostJob from "./pages/PostJob";
import Applicants from "./pages/Applicants";

function App() {
  return (
    <Router>
      <Routes>
        {/* Default route redirects to signup */}
        <Route path="/" element={<Navigate to="/signup" />} />

        {/* Auth Routes */}
        <Route path="/signup" element={<Signup />} />
        <Route path="/login" element={<Login />} />

        {/* Main App Routes */}
        <Route path="/postjob" element={<PostJob />} />
        <Route path="/applicants/:jobId" element={<Applicants />} />
      </Routes>
    </Router>
  );
}

export default App;
