import { Routes, Route } from "react-router-dom"; 
import LoginPage from "./components/LoginPage.jsx";
import AboutUs from "./components/AboutUs.jsx";
import Dashboard from "./components/Dashboard.jsx";
import Register from "./components/RegisterForm.jsx"
import Menu from "./components/Menu.jsx";
import Visualizer from "./components/Visualizer.jsx";
import FileInformation from "./components/FileInformation.jsx";

export default function App() {
  return (
    <Routes> {}
      <Route path="/" element={<LoginPage />} />
      <Route path="/register" element={<Register />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/about" element={<AboutUs />} />
      <Route path="/menu" element={<Menu />} />
      <Route path="/visualizer" element={<Visualizer />} />
      <Route path="/file/:fileId" element={<FileInformation />} />
    </Routes>
  );
}
