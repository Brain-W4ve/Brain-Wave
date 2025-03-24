import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";

const Dashboard = () => {
  const [files, setFiles] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchFiles = async () => {
      try {
        const token = localStorage.getItem("auth_token");
        const response = await fetch("http://localhost:5000/files", {
          headers: { Authorization: `Bearer ${token}` },
        });
        if (!response.ok) throw new Error("Error fetching files");
        const data = await response.json();
        setFiles(data.files);
      } catch (error) {
        console.error("Error fetching files:", error);
      }
    };

    fetchFiles();
  }, []);

  const handleDownload = async (fileName) => {
    try {
      const token = localStorage.getItem("auth_token");
      const response = await fetch(`http://localhost:5000/files/${fileName}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      if (!response.ok) throw new Error("Error downloading file");
      
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", fileName);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error("Error downloading file:", error);
    }
  };

  return (
    <div className="container mt-5">
      <h2 className="mb-4 text-center">Mis Archivos</h2>
      <ul className="list-group mb-3">
        {files.map((file) => (
          <li key={file} className="list-group-item d-flex justify-content-between align-items-center">
            {file}
            <button className="btn btn-primary btn-sm" onClick={() => handleDownload(file)}>Descargar</button>
          </li>
        ))}
      </ul>
      <div className="text-center">
        <button className="btn btn-secondary" onClick={() => navigate("/menu")}>Ir al Menú</button>
      </div>
    </div>
  );
};

export default Dashboard;
