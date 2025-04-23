import pytest
from unittest.mock import patch, MagicMock
from werkzeug.security import generate_password_hash

USER_DATA = {
    "email": "user@example.com",
    "password": "securepass"
}

def test_register_success(client):
    mock_user = MagicMock(id=1, email=USER_DATA["email"])
    mock_user.password = "hashedpass"

    with patch("src.routes.auth.validate_schema") as mock_validate, \
         patch("src.routes.auth.Session_Factory") as mock_session_factory, \
         patch("src.routes.auth.User") as MockUser, \
         patch("src.routes.auth.encode_auth_token") as mock_encode:

        mock_validate.return_value = (USER_DATA, None)
        mock_session = MagicMock()
        mock_session.query.return_value.filter_by.return_value.first.return_value = None
        mock_session_factory.return_value.__enter__.return_value = mock_session
        MockUser.return_value = mock_user
        mock_encode.return_value = "token"

        response = client.post("/auth/register", json=USER_DATA)
        data = response.get_json()

        assert response.status_code == 200
        assert data["message"] == "Successfully registered"
        assert data["auth_token"] == "token"


def test_register_user_exists(client):
    with patch("src.routes.auth.validate_schema") as mock_validate, \
         patch("src.routes.auth.Session_Factory") as mock_session_factory:

        mock_validate.return_value = (USER_DATA, None)
        mock_session = MagicMock()
        mock_session.query.return_value.filter_by.return_value.first.return_value = True
        mock_session_factory.return_value.__enter__.return_value = mock_session

        response = client.post("/auth/register", json=USER_DATA)
        assert response.status_code == 400
        assert response.get_json()["message"] == "User already exists"


def test_login_success(client):
    mock_user = MagicMock(id=1, email=USER_DATA["email"])
    mock_user.password = generate_password_hash(USER_DATA["password"])

    with patch("src.routes.auth.validate_schema") as mock_validate, \
         patch("src.routes.auth.Session_Factory") as mock_session_factory, \
         patch("src.routes.auth.encode_auth_token") as mock_encode:

        mock_validate.return_value = (USER_DATA, None)
        mock_session = MagicMock()
        mock_session.query.return_value.filter_by.return_value.first.return_value = mock_user
        mock_session_factory.return_value.__enter__.return_value = mock_session
        mock_encode.return_value = "token"

        response = client.post("/auth/login", json=USER_DATA)
        data = response.get_json()

        assert response.status_code == 200
        assert data["auth_token"] == "token"


def test_login_invalid_credentials(client):
    with patch("src.routes.auth.validate_schema") as mock_validate, \
         patch("src.routes.auth.Session_Factory") as mock_session_factory:

        mock_validate.return_value = (USER_DATA, None)
        mock_session = MagicMock()
        mock_session.query.return_value.filter_by.return_value.first.return_value = None
        mock_session_factory.return_value.__enter__.return_value = mock_session

        response = client.post("/auth/login", json=USER_DATA)
        assert response.status_code == 401
        assert response.get_json()["message"] == "Invalid credentials"


def test_logout_success(client):
    valid_token = "valid.token.here"

    with patch("src.routes.auth.decode_auth_token") as mock_decode, \
         patch("src.routes.auth.Session_Factory") as mock_session_factory:

        mock_decode.return_value = 1
        mock_session = MagicMock()
        mock_session.query.return_value.filter_by.return_value.first.return_value = None
        mock_session_factory.return_value.__enter__.return_value = mock_session

        response = client.post("/auth/logout", headers={"Authorization": f"Bearer {valid_token}"})
        assert response.status_code == 200
        assert response.get_json()["message"] == "Successfully logged out"


def test_logout_already_blacklisted(client):
    with patch("src.routes.auth.decode_auth_token") as mock_decode, \
         patch("src.routes.auth.Session_Factory") as mock_session_factory:

        mock_decode.return_value = 1
        mock_session = MagicMock()
        mock_session.query.return_value.filter_by.return_value.first.return_value = True
        mock_session_factory.return_value.__enter__.return_value = mock_session

        response = client.post("/auth/logout", headers={"Authorization": "Bearer faketoken"})
        assert response.status_code == 400
        assert response.get_json()["message"] == "Token already blacklisted"


def test_logout_invalid_token(client):
    with patch("src.routes.auth.decode_auth_token") as mock_decode:
        mock_decode.return_value = "Invalid token"

        response = client.post("/auth/logout", headers={"Authorization": "Bearer invalid"})
        assert response.status_code == 401
        assert "Invalid token" in response.get_json()["message"]


def test_status_success(client):
    with patch("src.routes.auth.token_required", lambda f: lambda *a, **kw: f(*a, user_id=1, **kw)), \
         patch("src.routes.auth.Session_Factory") as mock_session_factory:

        mock_user = MagicMock(id=1, email="user@example.com")
        mock_session = MagicMock()
        mock_session.query.return_value.filter_by.return_value.first.return_value = mock_user
        mock_session_factory.return_value.__enter__.return_value = mock_session

        response = client.get("/auth/status")
        assert response.status_code == 200
        assert response.get_json()["status"] == "success"


def test_status_user_not_found(client):
    with patch("src.routes.auth.token_required", lambda f: lambda *a, **kw: f(*a, user_id=1, **kw)), \
         patch("src.routes.auth.Session_Factory") as mock_session_factory:

        mock_session = MagicMock()
        mock_session.query.return_value.filter_by.return_value.first.return_value = None
        mock_session_factory.return_value.__enter__.return_value = mock_session

        response = client.get("/auth/status")
        assert response.status_code == 404
        assert response.get_json()["message"] == "User not found"
