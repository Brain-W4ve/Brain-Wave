import { useState } from "react";
import { useNavigate } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";

const LoginForm = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem("token", data.access_token);
        navigate("/dashboard");
      } else {
        setError(data.message || "Error en el inicio de sesión");
      }
    } catch (error) {
      console.error("Error en el login:", error);
      setError("No se pudo conectar con el servidor. Intenta nuevamente.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="d-flex vh-100 bg-primary justify-content-center align-items-center">
      <div className="card shadow-lg p-4" style={{ width: "22rem" }}>
        <div className="card-body text-center">
          <h1 className="text-primary fw-bold">BrainWave</h1>
          <p className="text-muted">Conecta con tus ideas</p>

          <form onSubmit={handleSubmit} className="mt-3">
            <div className="mb-3">
              <input
                type="email"
                className="form-control form-control-lg"
                placeholder="Correo electrónico"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="mb-3">
              <input
                type="password"
                className="form-control form-control-lg"
                placeholder="Contraseña"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>

            {error && <div className="alert alert-danger py-2">{error}</div>}

            <button
              type="submit"
              className="btn btn-primary btn-lg w-100"
              disabled={loading}
            >
              {loading ? "Cargando..." : "Continuar"}
            </button>
          </form>
          <div className="mt-3">
            <p className="text-muted">¿No tienes cuenta?</p>
            <button
              className="btn btn-outline-primary w-100"
              onClick={() => navigate("/register")}
            >
              Regístrate
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginForm;
