import { Routes, Route } from "react-router-dom"; 
import LoginPage from "./src/components/login_page.jsx";
import AboutUs from "./src/components/about_us.jsx";
import Menu from "./src/components/menu.jsx";

export default function App() {
  return (
    <Routes> {}
      <Route path="/" element={<LoginPage />} />
      <Route path="/about" element={<AboutUs />} />
      <Route path="/menu" element={<Menu />} />   
    </Routes>
  );
}