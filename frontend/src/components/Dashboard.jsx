import { useEffect, useState } from "react";
import { useNavigate, Link} from "react-router-dom";
import rest_client from "../utils/rest_client";


function Dashboard(){
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchFiles = async () => {
      try {
        const response = await rest_client.request(
          "GET",
          "/files",
        );
        
        const data = await response.data;
        if (data.status === "success" && Array.isArray(data.files)){
          setFiles(data.files);
        } else {
          setFiles([]);
        }
      } catch (error) {
        console.error("Error fetching files: ", error);
        setFiles([]);
      } finally {
        setLoading(false);
      }
    };
    fetchFiles();
  }, []);

  const handleDownload = async (fileId) => {
    try {
      const response = await rest_client.request(
        "GET", 
        `/download/${fileId}`, 
    );
      const contentDisposition = response.headers?.["content-disposition"];
      let filename = "downloaded_file";
  
      if (contentDisposition) {
        const match = contentDisposition.match(/filename\*?=(?:UTF-8'')?["']?([^"';\n]+)["']?/);
        if (match && match[1]) {
          filename = decodeURIComponent(match[1]);
        }
      }
  
      const blob = new Blob([response.data], { type: response.data.type });
  
      const link = document.createElement("a");
      link.href = window.URL.createObjectURL(blob);
      link.setAttribute("download", filename);
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error("Error downloading file: ", error);
      alert("Hubo un problema al descargar el archivo");
    }
  };

  const handleProcess = async (fileId) => {
    const response = await rest_client.request(
      "POST",
      `/process/${fileId}`,
      {model: "demo"}
    );

    console.log(response);

    const data = await response.data;

    if (response.status === "success"){
      const blob = await response.blob();
      const text = await blob.text();
      const data = JSON.parse(text);
      navigate("/visualizer", {state: {data}})
    } else {
      alert(`Error al procesar el archivo: ${fileId}`);
    }
  };

  // const handleAddFileRedirect = () => {};
  const handleMenuRedirect = () => {
    navigate("/menu");
  }

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
                  <td>
                    <Link to={`/file/${file.id}`} className="text-decoration-none text-primary">
                      {file.filename}
                    </Link>
                  </td>
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

export default Dashboard;