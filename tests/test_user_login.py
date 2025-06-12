import requests
from tests.conftest import BASE_URL, HEADERS
import allure
from data import MESSAGE_INVALID_CREDENTIALS, STATUS_OK, STATUS_UNAUTHORIZED

class TestUserLogin:

    @allure.title("Логин под существующим пользователем")
    def test_login_exiting_user(self,create_user):
        user_data, _ = create_user
        response = requests.post(f"{BASE_URL}/auth/login", json=user_data, headers=HEADERS)
        assert response.status_code == STATUS_OK
        assert "accessToken" in response.json()

    @allure.title("Логин с неверным логином и паролем")
    def test_login_invalid(self):
        user_data = {
            "email": "invalid_user@example.com",
            "password": "nopass"
        }

        response = requests.post(f"{BASE_URL}/auth/login", json=user_data, headers=HEADERS)
        assert response.status_code == STATUS_UNAUTHORIZED
        assert response.json()["message"] == MESSAGE_INVALID_CREDENTIALS
