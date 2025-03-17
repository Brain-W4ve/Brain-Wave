import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode"; // ✅ Importar correctamente
import "bootstrap/dist/css/bootstrap.min.css";

const Dashboard = () => {
  const [userName, setUserName] = useState("");
  const [files, setFiles] = useState([]);
  const navigate = useNavigate();

  // 🔹 Cargar el nombre del usuario desde el token
  useEffect(() => {
    const token = localStorage.getItem("token");
  
    if (token) {
      try {
        const decodedToken = jwtDecode(token); 
        console.log("Token decodificado:", decodedToken); // 🔹 Verifica que ahora incluye "sub.name"
  
        if (decodedToken.sub && decodedToken.sub.name) {
          setUserName(decodedToken.sub.name); // ✅ Extraer el nombre correctamente
        }
      } catch (error) {
        console.error("Error al decodificar el token:", error);
      }
    }
  }, []);

  return (
    <div className="container mt-5">
      <div className="card shadow-lg p-4">
        <h2 className="text-center text-primary">¡Hola, {userName}!</h2>
        <p className="text-center text-muted">Bienvenido a tu Dashboard</p>

        <div className="text-center mt-3">
          <button
            className="btn btn-outline-primary w-50"
            onClick={() => navigate("/menu")}
          >
            Ir al Menú
          </button>
        </div>

        <h4 className="mt-4">Tus archivos subidos:</h4>
        {files.length === 0 ? (
          <p className="text-muted">Aún no has subido ningún archivo.</p>
        ) : (
          <ul className="list-group">
            {files.map((file, index) => (
              <li key={index} className="list-group-item">
                {file}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default Dashboard;
