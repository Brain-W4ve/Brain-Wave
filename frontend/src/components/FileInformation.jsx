import { useState, useEffect } from "react";
import React from "react";
import rest_client from "../utils/rest_client";
import { useParams } from "react-router-dom";

function FileInformation(){
    const { fileId } = useParams();
    const [fileData, setFileData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() =>{
        const fetchFileData = async () => {
            try {
                const response = await rest_client.request(
                    "GET",
                    `/file/${fileId}`
                );

                const data = await response.data;
                setFileData(data.file);
            } catch (error){
                setError(error.message);
            } finally {
                setLoading(false);
            }
        };

        fetchFileData();
    }, [fileId]);

    if (loading){
        return <div>Loading...</div>
    }

    if (error){
        return <div>Error: {error}</div>
    }

    return (
        <div className="container mt-5">
            <div className="card shadow-sm p-4" style={{ backgroundColor: "#f8f9fa", color: "#333" }}>
                <h2 className="mb-4 text-center" style={{ color: "#007bff" }}>File Information</h2>
                {fileData ? (
                <div>
                    <p><strong>Filename:</strong> {fileData.filename}</p>
                    <p><strong>Content Type:</strong> {fileData.content_type}</p>
                    <p><strong>Uploaded At:</strong> {new Date(fileData.uploaded_at).toLocaleString()}</p>
                    <p>
                    <strong>Download URL:</strong>{" "}
                    <a
                        href={fileData.download_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="btn btn-outline-primary btn-sm"
                    >
                        Download File
                    </a>
                    </p>
                </div>
                ) : (
                <p className="text-muted">No file data available.</p>
                )}
            </div>
        </div>
    )
}

export default FileInformation;