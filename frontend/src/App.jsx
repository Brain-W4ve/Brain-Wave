import { Routes, Route } from "react-router-dom"; 
import LoginPage from "./components/LoginPage.jsx";
import AboutUs from "./components/AboutUs.jsx";
import Menu from "./components/Menu.jsx";

export default function App() {
  return (
    <Routes> {}
      <Route path="/" element={<LoginPage />} />
      <Route path="/about" element={<AboutUs />} />
      <Route path="/menu" element={<Menu />} />   
    </Routes>
  );
}