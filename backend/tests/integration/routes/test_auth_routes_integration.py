# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from src.models import Base, User, BLacklist_Token
# from werkzeug.security import generate_password_hash
# from flask import Flask
# from src.routes.auth import auth_bp

# TEST_DB_URL = "sqlite:///:memory:"


# @pytest.fixture(scope="module")
# def test_app():
#     app = Flask(__name__)
#     app.config["SECRET_KEY"] = "integrationsecret"
#     app.config["TESTING"] = True
#     app.register_blueprint(auth_bp, url_prefix="/auth")
#     return app


# @pytest.fixture(scope="module")
# def test_client(test_app):
#     return test_app.test_client()


# @pytest.fixture(scope="module")
# def db_session():
#     engine = create_engine(TEST_DB_URL)
#     TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#     Base.metadata.create_all(bind=engine)
#     session = TestingSessionLocal()
#     yield session
#     session.close()
#     Base.metadata.drop_all(bind=engine)


# @pytest.fixture(autouse=True)
# def patch_session_factory(monkeypatch, db_session):
#     monkeypatch.setattr("src.routes.auth.Session_Factory", lambda: db_session)


# @pytest.mark.integration
# def test_register_and_login(test_client):
#     response = test_client.post("/auth/register", json={
#         "email": "testuser@example.com",
#         "password": "testpassword"
#     })
#     assert response.status_code == 200
#     assert "auth_token" in response.get_json()

#     response = test_client.post("/auth/login", json={
#         "email": "testuser@example.com",
#         "password": "testpassword"
#     })
#     assert response.status_code == 200
#     assert "auth_token" in response.get_json()


# @pytest.mark.integration
# def test_status_and_logout(test_client):
#     reg = test_client.post("/auth/register", json={
#         "email": "statuser@example.com",
#         "password": "somepass"
#     })
#     token = reg.get_json()["auth_token"]

#     headers = {"Authorization": f"Bearer {token}"}
#     status = test_client.get("/auth/status", headers=headers)
#     assert status.status_code == 200
#     assert status.get_json()["status"] == "success"

#     logout = test_client.post("/auth/logout", headers=headers)
#     assert logout.status_code == 200
#     assert logout.get_json()["message"] == "Successfully logged out"
