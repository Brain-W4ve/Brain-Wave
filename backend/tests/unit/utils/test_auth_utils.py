import jwt
from unittest.mock import patch, MagicMock
from freezegun import freeze_time
from datetime import datetime, timezone, timedelta
from src.utils.auth_utils import encode_auth_token, decode_auth_token

SECRET_KEY = "supersecret"
USER_ID = 123

@freeze_time("2024-04-21 12:00:00")
def test_encode_auth_token():
    token = encode_auth_token(USER_ID, SECRET_KEY)
    decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    
    assert decoded["sub"] == str(USER_ID)
    assert decoded["iat"] == datetime(2024, 4, 21, 12, 0, 0, tzinfo=timezone.utc).timestamp()
    assert decoded["exp"] == (datetime(2024, 4, 21, 12, 30, 0, tzinfo=timezone.utc)).timestamp()


@patch("src.utils.auth_utils.BLacklist_Token")
def test_decode_valid_token(mock_blacklist_model):
    token = encode_auth_token(USER_ID, SECRET_KEY)

    mock_session = MagicMock()
    mock_blacklist_model.check_blacklist.return_value = False

    result = decode_auth_token(token, SECRET_KEY, mock_session)
    assert result == USER_ID


@patch("src.utils.auth_utils.BLacklist_Token")
def test_decode_blacklisted_token(mock_blacklist_model):
    token = encode_auth_token(USER_ID, SECRET_KEY)

    mock_session = MagicMock()
    mock_blacklist_model.check_blacklist.return_value = True

    result = decode_auth_token(token, SECRET_KEY, mock_session)
    assert result == "Token blacklisted. Please log in again"


def test_decode_expired_token():
    now = datetime.now(timezone.utc)
    expired_payload = {
        "exp": now - timedelta(minutes=1),
        "iat": now - timedelta(hours=1),
        "sub": str(USER_ID),
    }
    token = jwt.encode(expired_payload, SECRET_KEY, algorithm="HS256")
    
    mock_session = MagicMock()
    result = decode_auth_token(token, SECRET_KEY, mock_session)
    assert result == "Signature expired. Please log in again."


def test_decode_invalid_token():
    invalid_token = "totally.invalid.token"
    mock_session = MagicMock()

    result = decode_auth_token(invalid_token, SECRET_KEY, mock_session)
    assert result == "Invalid token. Please log in again."