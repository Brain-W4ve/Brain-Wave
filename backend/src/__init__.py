from flask import Flask
from flask_cors import CORS
from sqlalchemy import create_engine
from .models import Base
import os 


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["DATABASE_URL"] = os.getenv("DATABASE_URL", "sqlite:///data.db")

    engine = create_engine(app.config["DATABASE_URL"])
    Base.metadata.create_all(engine)
    app.config["DB_ENGINE"] = engine


    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp)


    return app