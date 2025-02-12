import { useState } from "react";
import SciChart from "./SciChart"; // Your SciChartComponent

export default function Menu() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [channelsData, setChannelsData] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Por favor, selecciona un archivo primero.");
      return;
    }

    setIsLoading(true);
    setChannelsData(null);

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const uploadResponse = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });

      if (!uploadResponse.ok) {
        throw new Error("Error al subir el archivo.");
      }

      const uploadResult = await uploadResponse.json();
      const fileId = uploadResult.fileId;

      const channelsResponse = await fetch(`http://localhost:5000/files/${fileId}/channels`);
      if (!channelsResponse.ok) {
        throw new Error("Error al obtener datos de los canales.");
      }

      const channelsData = await channelsResponse.json();
      setChannelsData(channelsData);
    } catch (error) {
      console.error(error);
      alert("Ocurrió un error durante la subida o la obtención de datos.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mt-5">
      <div className="card">
        <div className="card-body">
          <h2 className="card-title text-center">Menú de Subida de Archivos</h2>
          <div className="form-group">
            <label htmlFor="fileInput">Selecciona un archivo:</label>
            <input type="file" id="fileInput" className="form-control" onChange={handleFileChange} />
          </div>
          <button
            className="btn btn-primary btn-block"
            onClick={handleUpload}
            disabled={isLoading}
          >
            {isLoading ? (
              <span>
                <span className="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                {" "}Subiendo...
              </span>
            ) : (
              "Subir Archivo"
            )}
          </button>
          {selectedFile && (
            <p className="mt-3 text-muted">Archivo seleccionado: {selectedFile.name}</p>
          )}
        </div>
      </div>

      {isLoading && (
        <div className="text-center mt-4">
          <div className="spinner-border text-primary" role="status">
            <span className="sr-only">Cargando...</span>
          </div>
          <p className="mt-2">Cargando datos...</p>
        </div>
      )}

      {channelsData && (
        <div className="mt-5">
          <h3>Datos de Canales Visualizados:</h3>
          <div className="card">
            <div className="card-body">
              <SciChart data={channelsData} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
