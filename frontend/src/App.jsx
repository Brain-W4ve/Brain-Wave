import { Routes, Route } from "react-router-dom"; 
import LoginPage from "./components/login_page.jsx";
import AboutUs from "./components/about_us.jsx";
import Menu from "./components/menu.jsx";
import Register from "./components/register_form.jsx"
import Dashboard from "./components/dashboard.jsx"
import "bootstrap/dist/css/bootstrap.min.css";


export default function App() {
  return (
    <Routes> {}
      <Route path="/" element={<LoginPage />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/about" element={<AboutUs />} />
      <Route path="/menu" element={<Menu />} />   
      <Route path="/register" element={<Register/>}/>
    </Routes>
  );
}