import { useNavigate } from "react-router-dom";

export default function AboutUs() {
  const navigate = useNavigate();

  return (
    <div>
      <h2>Sobre Nosotros</h2>
      <p>Bienvenido a nuestra aplicación. Aquí puedes aprender más sobre nuestro proyecto.</p>
      <button onClick={() => navigate("/menu")}>
        Ir al Menú
      </button>
    </div>
  );
}
