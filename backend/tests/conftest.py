# tests/conftest.py
import pytest
from flask import Flask
from src.routes.auth import auth_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "testsecret"
    app.register_blueprint(auth_bp, url_prefix="/auth")
    return app

@pytest.fixture
def client(app):
    return app.test_client()


def pytest_configure(config):
    config.addinivalue_line("markers", "unit: mark test as unit")
    config.addinivalue_line("markers", "integration: mark test as integration")