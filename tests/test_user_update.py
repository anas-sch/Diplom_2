import requests
from tests.conftest import BASE_URL, HEADERS
import allure
from data import MESSAGE_UNAUTHORIZED, STATUS_OK, STATUS_UNAUTHORIZED, UPDATED_NAME

class TestUserUpdate:

    @allure.title("Изменение данных пользователя с авторизацией")
    def test_user_update_with_auth(self, create_user):
        _, auth_token = create_user
        headers = {**HEADERS, "Authorization": auth_token}
        update_data = {"name": UPDATED_NAME}
        response = requests.patch(f"{BASE_URL}/auth/user", json=update_data, headers=headers)
        assert response.status_code == STATUS_OK
        assert response.json()["user"]["name"] == UPDATED_NAME


    @allure.title("Изменение данных пользователя без авторизации")
    def test_user_update_no_auth(self):
        update_data =  {"name": "new_name"}
        response = requests.patch(f"{BASE_URL}/auth/user", json=update_data, headers=HEADERS)
        assert response.status_code == STATUS_UNAUTHORIZED
        assert response.json()["message"] == MESSAGE_UNAUTHORIZED
