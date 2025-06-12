import requests
from tests.conftest import BASE_URL, HEADERS
import allure
from data import MESSAGE_UNAUTHORIZED, STATUS_OK, STATUS_UNAUTHORIZED

class TestGetUserOrders:

    @allure.title("Получение заказа не авторизованного пользователя")
    def test_get_order_unauthorized_user(self):
        response = requests.get(f"{BASE_URL}/orders", headers=HEADERS)
        assert response.status_code == STATUS_UNAUTHORIZED
        assert response.json()["message"] == MESSAGE_UNAUTHORIZED

    @allure.title("Получение заказа авторизованного пользователя")
    def test_get_order_authorized_user(self, auth_token):
        headers = {**HEADERS, "Authorization": auth_token}
        response = requests.get(f"{BASE_URL}/orders", headers=headers)
        assert response.status_code == STATUS_OK
        assert "orders" in response.json()