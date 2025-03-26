import { useState } from "react";
import { useNavigate } from "react-router-dom";

const RegisterForm = () => {
  const [formData, setFormData] = useState({ username: "", email: "", password: "" });
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:5000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await response.json();
      if (response.ok) {
        setMessage("Registro exitoso.");
        navigate("/");

      } else {
        setMessage(data.message || "Error en el registro");
      }
    } catch (error) {
      setMessage("Error al conectar con el servidor");
    }
  };

  return (
    <div className="d-flex align-items-center justify-content-center min-vh-100 bg-light">
      <div className="card shadow-lg rounded-4 p-4" style={{ width: '100%', maxWidth: '400px' }}>
        <h2 className="text-center text-primary mb-4">Registro</h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <input
              type="text"
              name="username"
              placeholder="Nombre de usuario"
              value={formData.username}
              onChange={handleChange}
              required
              className="form-control"
            />
          </div>
          <div className="mb-3">
            <input
              type="email"
              name="email"
              placeholder="Correo electrónico"
              value={formData.email}
              onChange={handleChange}
              required
              className="form-control"
            />
          </div>
          <div className="mb-3">
            <input
              type="password"
              name="password"
              placeholder="Contraseña"
              value={formData.password}
              onChange={handleChange}
              required
              className="form-control"
            />
          </div>
          <button
            type="submit"
            className="btn btn-primary w-100 py-2"
          >
            Registrarse
          </button>
        </form>
        {message && <p className="mt-3 text-center text-muted">{message}</p>}
      </div>
    </div>
  );
};

export default RegisterForm;
