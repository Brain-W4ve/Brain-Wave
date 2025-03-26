import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

export default function Dashboard() {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchFiles = async () => {
      try {
        const token = localStorage.getItem("token");
        const response = await fetch("http://localhost:5000/files", {
          headers: { Authorization: `Bearer ${token}` },
        });
        const data = await response.json();
        if (data.status === "success" && Array.isArray(data.files)) {
          setFiles(data.files);
        } else {
          setFiles([]);
        }
      } catch (error) {
        console.error("Error fetching files:", error);
        setFiles([]);
      } finally {
        setLoading(false);
      }
    };
    fetchFiles();
  }, []);

  const handleDownload = async (fileId) => {
    try {
      const token = localStorage.getItem("token");
      const response = await fetch(`http://localhost:5000/download/${fileId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      const data = await response.json();
      if (data.status === "success") {
        window.location.href = data.download_url;
      } else {
        alert("Error al descargar el archivo");
      }
    } catch (error) {
      console.error("Error downloading file:", error);
      alert("Hubo un problema al descargar el archivo");
    }
  };

  const handleProcess = (fileId) => {
    window.location.href = `/scichart/${fileId}`;
  };

  const handleMenuRedirect = () => {
    navigate("/menu");
  };

  return (
    <div className="container mt-5">
      <div className="card shadow-sm p-4" style={{ backgroundColor: "#f8f9fa", color: "#333" }}>
        <h2 className="mb-4 text-center" style={{ color: "#007bff" }}>Dashboard</h2>
        {loading ? (
          <div className="text-center">
            <div className="spinner-border text-primary" role="status">
              <span className="visually-hidden">Cargando...</span>
            </div>
          </div>
        ) : files.length > 0 ? (
          <table className="table table-striped">
            <thead className="table-light">
              <tr>
                <th>Nombre del Archivo</th>
                <th className="text-center">Acciones</th>
              </tr>
            </thead>
            <tbody>
              {files.map((file) => (
                <tr key={file.id}>
                  <td>{file.filename}</td>
                  <td className="text-center">
                    <button
                      className="btn btn-outline-primary btn-sm me-2"
                      onClick={() => handleDownload(file.id)}
                    >
                      Descargar
                    </button>
                    <button
                      className="btn btn-outline-secondary btn-sm"
                      onClick={() => handleProcess(file.id)}
                    >
                      Procesar
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p className="text-center text-muted">No hay archivos disponibles.</p>
        )}
        <div className="text-center mt-4">
          <button className="btn btn-outline-dark" onClick={handleMenuRedirect}>Volver al Menú</button>
        </div>
      </div>
    </div>
  );
}
