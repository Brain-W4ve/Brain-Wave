from flask import Flask, jsonify
from unittest.mock import patch, MagicMock
import pytest

from src.utils.auth_utils import token_required

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "supersecret"

    @app.route("/protected")
    @token_required
    def protected(user_id):
        return jsonify(message="Access granted", user_id=user_id)

    return app

def test_token_required_success(app):
    client = app.test_client()

    # valid token
    from src.utils.auth_utils import encode_auth_token
    token = encode_auth_token(42, app.config["SECRET_KEY"])

    with patch("src.utils.auth_utils.decode_auth_token") as mock_decode:
        mock_decode.return_value = 42
        response = client.get("/protected", headers={"Authorization": f"Bearer {token}"})
        assert response.status_code == 200
        assert response.json["message"] == "Access granted"
        assert response.json["user_id"] == 42


def test_token_required_missing(app):
    client = app.test_client()
    response = client.get("/protected")
    assert response.status_code == 401
    assert response.json["message"] == "Provide a valid auth token"


def test_token_required_invalid_token(app):
    client = app.test_client()

    with patch("src.utils.auth_utils.decode_auth_token") as mock_decode:
        mock_decode.return_value = "Invalid token. Please log in again."
        response = client.get("/protected", headers={"Authorization": "Bearer faketoken"})
        assert response.status_code == 401
        assert "Invalid token" in response.json["message"]
