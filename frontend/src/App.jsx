import { Routes, Route } from "react-router-dom"; 
import LoginPage from "./components/LoginPage.jsx";
import AboutUs from "./components/AboutUs.jsx";
import Dashboard from "./components/dashboard.jsx"
import Register from "./components/RegisterForm.jsx"

export default function App() {
  return (
    <Routes> {}
      <Route path="/" element={<LoginPage />} />
      <Route path="/register" element={<Register />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/about" element={<AboutUs />} />
    </Routes>
  );
}
