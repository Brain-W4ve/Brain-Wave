import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import rest_client from "../utils/rest_client";

const LoginForm = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await rest_client.request({
        method: "POST",
        url: "/login",
        data: { email, password },
      });

      if (response.auth_token) {
        localStorage.setItem("token", response.auth_token);
        navigate("/dashboard");
      } else {
        alert("Token no recibido.");
      }
    } catch (error) {
      console.error("Error en autenticación:", error);
      alert(error.response?.data?.message || "Error en inicio de sesión");
    }
  };

  return (
    <div className="min-vh-100 d-flex align-items-center justify-content-center bg-light">
      <div
        className="card p-4 shadow-lg border-0"
        style={{
          maxWidth: "400px",
          borderRadius: "15px",
          backgroundColor: "#f0f9ff",
        }}
      >
        <div className="text-center mb-4">
          <h1 className="display-6 fw-bold text-primary">BrainWave</h1>
          <p className="text-muted">Conectando mentes, transformando ideas</p>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="email" className="form-label">
              Correo electrónico
            </label>
            <input
              type="email"
              id="email"
              className="form-control rounded-pill border-0 shadow-sm"
              placeholder="Ingresa tu correo electrónico"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="mb-3">
            <label htmlFor="password" className="form-label">
              Contraseña
            </label>
            <input
              type="password"
              id="password"
              className="form-control rounded-pill border-0 shadow-sm"
              placeholder="Ingresa tu contraseña"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button
            type="submit"
            className="btn btn-primary w-100 py-2 fw-bold rounded-pill shadow-sm"
          >
            Iniciar sesión
          </button>
          <div className="text-center mt-3">
            <button
              className="btn btn-link text-primary fw-bold"
              type="button"
              onClick={() => navigate("/register")}
            >
              ¿No tienes cuenta? Regístrate
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default LoginForm;
