import { useState } from "react";
import SciChart from "./SciChart"; // Your SciChartComponent

export default function Menu() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [channelsData, setChannelsData] = useState(null);
  const [isLoading, setIsLoading] = useState(false); // Loading state

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert("Por favor, selecciona un archivo primero.");
      return;
    }

    setIsLoading(true); // Start loading
    setChannelsData(null); // Reset the previous data

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      // Step 1: Upload the file
      const uploadResponse = await fetch("http://localhost:5000/upload", {
        method: "POST",
        body: formData,
      });

      if (!uploadResponse.ok) {
        throw new Error("Error al subir el archivo.");
      }

      const uploadResult = await uploadResponse.json();
      const fileId = uploadResult.fileId;

      // Step 2: Fetch channels data
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
      setIsLoading(false); // Stop loading
    }
  };

  return (
    <div>
      <h2>Menú</h2>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={isLoading}>
        {isLoading ? "Subiendo..." : "Subir Archivo"}
      </button>
      {selectedFile && <p>Archivo seleccionado: {selectedFile.name}</p>}

      {isLoading && <p>Cargando datos...</p>}

      {channelsData && (
        <div>
          <h3>Datos de Canales Visualizados:</h3>
          <SciChart data={channelsData} />
        </div>
      )}
    </div>
  );
}
