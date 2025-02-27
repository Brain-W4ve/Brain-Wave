from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
from werkzeug.security import check_password_hash, generate_password_hash
from models.users import User  # ✅ Apunta a users.py correctamente
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import timedelta
import traceback  # Agrega esto para imprimir el error completo


app = Flask(__name__)
CORS(app,supports_credentials=True)  # 🔹 Habilita CORS solo para el frontend
app.config["JWT_SECRET_KEY"] = "supersecretkey"
jwt = JWTManager(app)

DATABASE_URL = "mysql+pymysql://root:@localhost:3306/brainwave"

# 🔹 Configurar la conexión a la base de datos
engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# 🔹 RUTA: LOGIN (Ahora consulta la base de datos)
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "Formato JSON inválido"}), 400

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"message": "Email y contraseña son requeridos"}), 400

        with SessionLocal() as session:
            user = session.query(User).filter_by(email=email).first()

            if not user:
                return jsonify({"message": "Usuario no encontrado"}), 404

            if not check_password_hash(user.password, password):
                return jsonify({"message": "Contraseña incorrecta"}), 401

            access_token = create_access_token(identity=email, expires_delta=timedelta(hours=1))
            return jsonify({"access_token": access_token}), 200

    except Exception as e:
        print("❌ ERROR EN LOGIN:")
        traceback.print_exc()  # Imprime el error completo en la terminal
        return jsonify({"message": "Error interno del servidor"}), 500


# 🔹 RUTA: REGISTRO (Se mantiene igual)
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    name = data.get("name", "Usuario")  # 🔹 Valor por defecto si no se envía

    if not email or not password:
        return jsonify({"error": "Email y contraseña son obligatorios"}), 400

    hashed_password = generate_password_hash(password)

    with SessionLocal() as session:
        if session.query(User).filter_by(email=email).first():
            return jsonify({"error": "El usuario ya existe"}), 400
        
        new_user = User(email=email, name=name, password=hashed_password)
        session.add(new_user)
        session.commit()

    return jsonify({"message": "Usuario registrado exitosamente"}), 201

if __name__ == "__main__":
    app.run(debug=True)
