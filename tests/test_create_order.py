import requests
from tests.conftest import BASE_URL, HEADERS
import allure
from data import (STATUS_OK, STATUS_BAD_REQUEST, SUCCESS_TRUE, SUCCESS_FALSE, MESSAGE_NO_INGREDIENTS,
                  ORDER_SHOULD_CONTAIN_INGREDIENTS)

class TestCreateOrder:
    @allure.title("Оформление заказа без авторизации с ингредиентами")
    def test_create_order_no_auth(self, ingredients):
        order_data = {"ingredients": ingredients}

        response = requests.post(f"{BASE_URL}/orders", json=order_data, headers=HEADERS)
        response_data = response.json()

        assert response.status_code == STATUS_OK
        assert response_data.get("success") is SUCCESS_TRUE
        assert "order" in response_data

    @allure.title("Оформление заказа с авторизацией с ингредиентами")
    def test_create_order_with_auth(self, auth_token, ingredients):
        headers = {**HEADERS, "Authorization": auth_token}
        order_data = {"ingredients": ingredients}

        response = requests.post(f"{BASE_URL}/orders", json=order_data, headers=headers)
        response_data = response.json()

        assert response.status_code == STATUS_OK
        assert response_data.get("success") is SUCCESS_TRUE
        assert "order" in response_data
        assert response_data["order"].get("ingredients"), ORDER_SHOULD_CONTAIN_INGREDIENTS

    @allure.title("Оформление заказа без ингредиентов")
    def test_create_order_empty_ingredients(self, auth_token):
        headers = {**HEADERS, "Authorization": auth_token}
        order_data = {"ingredients": []}

        response = requests.post(f"{BASE_URL}/orders", json=order_data, headers=headers)
        response_data = response.json()

        assert response.status_code == STATUS_BAD_REQUEST
        assert response_data.get("message") == MESSAGE_NO_INGREDIENTS

    @allure.title("Оформление заказа с неверным хешем ингредиентов")
    def test_create_order_invalid_ingredients(self, auth_token):
        headers = {**HEADERS, "Authorization": auth_token}
        order_data = {"ingredients": ["invalid_hash"]}

        response = requests.post(f"{BASE_URL}/orders", json=order_data, headers=headers)
        response_data = response.json()


        assert response.status_code == STATUS_BAD_REQUEST
        assert response_data.get("success") is SUCCESS_FALSE
        assert "message" in response_data