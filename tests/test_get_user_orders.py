import requests
from tests.conftest import BASE_URL, HEADERS
import allure

class TestGetUserOrders:

    @allure.title("Получение заказа не авторизованного пользователя")
    def test_get_order_unauthorized_user(self):
        response = requests.get(f"{BASE_URL}/orders", headers=HEADERS)
        assert response.status_code == 401
        assert response.json()["message"] == "You should be authorised"

    @allure.title("Получение заказа авторизованного пользователя")
    def test_get_order_authorized_user(self, auth_token):
        headers = {**HEADERS, "Authorization": auth_token}
        response = requests.get(f"{BASE_URL}/orders", headers=headers)
        assert response.status_code == 200
        assert "orders" in response.json()