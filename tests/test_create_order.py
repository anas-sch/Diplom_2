import requests
from tests.conftest import BASE_URL, HEADERS
import allure

class TestCreateOrder:
    @allure.title("Оформление заказа без авторизации с ингредиентами")
    def test_create_order_no_auth(self, ingredients):
        order_data = {"ingredients": ingredients}

        response = requests.post(f"{BASE_URL}/orders", json=order_data, headers=HEADERS)
        response_data = response.json()

        assert response.status_code == 200
        assert response_data.get("success") is True
        assert "order" in response_data

    @allure.title("Оформление заказа с авторизацией с ингредиентами")
    def test_create_order_with_auth(self, auth_token, ingredients):
        headers = {**HEADERS, "Authorization": auth_token}
        order_data = {"ingredients": ingredients}

        response = requests.post(f"{BASE_URL}/orders", json=order_data, headers=headers)
        response_data = response.json()

        assert response.status_code == 200
        assert response_data.get("success") is True
        assert "order" in response_data
        assert response_data["order"].get("ingredients"), "Order should contain ingredients"

    @allure.title("Оформление заказа без ингредиентов")
    def test_create_order_empty_ingredients(self, auth_token):
        headers = {**HEADERS, "Authorization": auth_token}
        order_data = {"ingredients": []}

        response = requests.post(f"{BASE_URL}/orders", json=order_data, headers=headers)
        response_data = response.json()

        assert response.status_code == 400
        assert response_data.get("message") == "Ingredient ids must be provided"

    @allure.title("Оформление заказа с неверным хешем ингредиентов")
    def test_create_order_invalid_ingredients(self, auth_token):
        headers = {**HEADERS, "Authorization": auth_token}
        order_data = {"ingredients": ["invalid_hash"]}

        response = requests.post(f"{BASE_URL}/orders", json=order_data, headers=headers)
        response_data = response.json()


        assert response.status_code == 400
        assert response_data.get("success") is False
        assert "message" in response_data