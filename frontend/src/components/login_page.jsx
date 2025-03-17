import { useNavigate } from "react-router-dom";
import LoginForm from "./login_form.jsx";
import RegisterForm from "./register_form.jsx";

export default function LoginPage() {
  const navigate = useNavigate();

  return (
    <div>
      <LoginForm />
      <div>
        <button onClick={() => navigate("/register")}>Ir a Registro</button>
      </div>
    </div>
  );
}
