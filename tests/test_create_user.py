import requests
from tests.conftest import BASE_URL, HEADERS, create_user, generate_unique_email
import allure

class TestCreateUser:
    @allure.title("Создание уникального пользователя")
    def test_create_user(self, create_user):
        user_data, access_token = create_user
        assert access_token is not None


    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_existing_user(self, create_user):
        user_data, _ = create_user
        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=user_data,
            headers=HEADERS
        )

        assert response.status_code == 403
        assert response.json()["message"] == "User already exists"


    @allure.title("Создание пользователя без обязательного поля")
    def test_create_user_missing_field(self, auth_token):
        user_data = {
            "email": generate_unique_email(),
            "name": "User_test"
        }

        response = requests.post(
            f"{BASE_URL}/auth/register",
            json=user_data,
            headers=HEADERS
        )

        assert response.status_code == 403
        assert response.json()["message"] == "Email, password and name are required fields"