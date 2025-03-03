import { useState } from "react";
import SciChart from "./SciChart"; // Your SciChartComponent
import "bootstrap/dist/css/bootstrap.min.css";

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
      alert("Archivo subido y datos obtenidos correctamente.");
    } catch (error) {
      console.error(error);
      alert("Ocurrió un error durante la subida o la obtención de datos.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container mt-5">
      <div className="card p-4 shadow-sm">
        <h2 className="mb-3">Menú</h2>
        <input type="file" className="form-control mb-3" onChange={handleFileChange} />
        <button className="btn btn-primary" onClick={handleUpload} disabled={isLoading}>
          {isLoading ? "Subiendo..." : "Subir Archivo"}
        </button>
        {selectedFile && <p className="mt-2">Archivo seleccionado: <strong>{selectedFile.name}</strong></p>}

        {isLoading && <div className="alert alert-info mt-3">Cargando datos...</div>}

        {channelsData && (
          <div className="mt-4">
            <h3>Datos de Canales Visualizados:</h3>
            <SciChart data={channelsData} />
          </div>
        )}
      </div>
    </div>
  );
}
