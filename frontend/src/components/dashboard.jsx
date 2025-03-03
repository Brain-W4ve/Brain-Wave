import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";

const Dashboard = () => {
  const [userName, setUserName] = useState("Usuario");
  const [files, setFiles] = useState([]);
  const navigate = useNavigate();

  // Cargar el nombre del usuario desde localStorage
  useEffect(() => {
    const storedUserName = localStorage.getItem("userName");
    if (storedUserName) {
      setUserName(storedUserName);
    }
  }, []);

  // Cargar archivos desde el backend
  useEffect(() => {
    const fetchFiles = async () => {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch("http://127.0.0.1:5000/files", {
          method: "GET",
          headers: {
            Authorization: `Bearer ${token}`,
          },
          credentials: "include",
        });

        if (response.ok) {
          const data = await response.json();
          setFiles(data.files || []);
        } else {
          console.error("Error al obtener archivos");
        }
      } catch (error) {
        console.error("Error de conexión:", error);
      }
    };

    fetchFiles();
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
