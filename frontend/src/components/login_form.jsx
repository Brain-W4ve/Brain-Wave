import { useState } from "react";
import { useNavigate } from "react-router-dom";

const LoginForm = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = (e) => {
    e.preventDefault();
    navigate("/about");
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
              type="text"
              placeholder="Correo electrónico"
              className="w-full p-4 text-lg border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:ring-4 focus:ring-blue-100 placeholder-gray-400 transition-all"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            
            <input
              type="text"
              placeholder="Contraseña"
              className="w-full p-4 text-lg border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:ring-4 focus:ring-blue-100 placeholder-gray-400 transition-all"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white p-4 rounded-xl font-bold text-lg transition-all duration-300 transform hover:-translate-y-1 shadow-lg hover:shadow-xl"
          >
            Continuar
          </button>
        </form>
      </div>
    </div>
  );
};

export default LoginForm;
