import { useState } from "react";
import { useNavigate } from "react-router-dom";
// import "bootstrap/dist/css/bootstrap.min.css";

const LoginForm = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    navigate("/dashboard");
  };

  return (
    <div className="min-vh-100 d-flex align-items-center justify-content-center bg-gradient">
      <div className="card p-4 shadow-lg" style={{ maxWidth: "400px", borderRadius: "20px" }}>
        <div className="text-center mb-4">
          <h1 className="display-5 fw-bold text-primary">BrainWave</h1>
          <p className="text-muted">Conecta con tus ideas</p>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="email" className="form-label">
              Correo electrónico
            </label>
            <input
              type="email"
              id="email"
              className="form-control"
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
              className="form-control"
              placeholder="Ingresa tu contraseña"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button
            type="submit"
            className="btn btn-primary w-100 py-2 fw-bold"
          >
            Continuar
          </button>
        </form>
        <div className="text-center mt-3">
          <p>¿No tienes una cuenta? <button className="btn btn-link p-0" onClick={() => navigate("/register")} >Regístrate</button></p>
        </div>
      </div>
    </div>
  );
};

export default LoginForm;
