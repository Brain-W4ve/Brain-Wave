from flask import Flask
from flask_cors import CORS
from src.db import engine
from .models import Base
import os 


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # Base.metadata.create_all(engine)
    # app.config["DB_ENGINE"] = engine

    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from .routes.file import file_bp
    app.register_blueprint(file_bp)

    from .routes.process import process_bp
    app.register_blueprint(process_bp)

    return app