import { useNavigate } from "react-router-dom";

export default function AboutUs() {
  const navigate = useNavigate();

  return (
    <div className="container mt-5">
      <div className="card shadow-lg p-4">
        <h2 className="text-center mb-3">Sobre Nosotros</h2>
        <p className="text-muted text-center">
          Bienvenido a nuestra aplicación. Aquí puedes aprender más sobre nuestro proyecto.
        </p>
        <div className="d-flex justify-content-center">
          <button className="btn btn-primary" onClick={() => navigate("/menu")}>
            Ir al Menú
          </button>
        </div>
      </div>
    </div>
  );
}
