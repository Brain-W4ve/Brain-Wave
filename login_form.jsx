import { useState } from "react";
import { useNavigate } from "react-router-dom";

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
        credentials: "include", // Permitir cookies/sesiones si es necesario
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        localStorage.setItem("token", data.access_token);
        navigate("/about"); // Redirige al dashboard tras login exitoso
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
    <div className="min-h-screen bg-gradient-to-br from-blue-500 to-blue-600 flex items-center justify-center p-4">
      <div className="bg-white w-full max-w-md rounded-3xl shadow-2xl p-8 space-y-8 transition-all hover:shadow-3xl">
        
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-bold text-blue-600 mb-2">
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-blue-400">
              BrainWave
            </span>
          </h1>
          <p className="text-gray-600 text-lg font-medium">Conecta con tus ideas</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-4">
            <input
              type="email"
              placeholder="Correo electrónico"
              className="w-full p-4 text-lg border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:ring-4 focus:ring-blue-100 placeholder-gray-400 transition-all"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            
            <input
              type="password"
              placeholder="Contraseña"
              className="w-full p-4 text-lg border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:ring-4 focus:ring-blue-100 placeholder-gray-400 transition-all"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {error && <p className="text-red-500 text-sm font-medium">{error}</p>}

          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white p-4 rounded-xl font-bold text-lg transition-all duration-300 transform hover:-translate-y-1 shadow-lg hover:shadow-xl"
            disabled={loading}
          >
            {loading ? "Cargando..." : "Continuar"}
          </button>
        </form>
      </div>
    </div>
  );
};

export default LoginForm;
