from http.client import responses

import pytest
import requests
import random
import string

BASE_URL = "https://stellarburgers.nomoreparties.site/api"
HEADERS = {'Content-Type': 'application/json'}


def generate_unique_email():
    return f"test_{''.join(random.choices(string.ascii_lowercase, k=7))}@examlpe.com"

@pytest.fixture
def auth_token():
    user_data = {
        "email": generate_unique_email(),
        "password": "test12345",
        "name": "User_test"
    }

    registration_response = requests.post(f"{BASE_URL}/auth/register", json=user_data, headers=HEADERS)
    print(f"Registration response: {registration_response.status_code}, {registration_response.json()}")

    if registration_response.status_code == 403:
      print(f"User already exists")

    login_data = {
        "email": user_data["email"],
        "password": user_data["password"]
    }

    login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data, headers=HEADERS)
    print(f"Login response: {login_response.status_code}, {login_response.json()}")
    return login_response.json().get("accessToken")

@pytest.fixture
def ingredients():
    response = requests.get(f"{BASE_URL}/ingredients", headers=HEADERS)
    return [ingredient["_id"] for ingredient in response.json().get("data", [])]

@pytest.fixture
def create_user():
    user_data = {
       "email": generate_unique_email(),
       "password": "test12345",
        "name": "User test"
    }

    response = requests.post(f"{BASE_URL}/auth/register", json=user_data, headers=HEADERS)
    access_token = response.json().get("accessToken")

    yield user_data, access_token

    requests.delete(f"{BASE_URL}/auth/user", headers={"Authorization": f"Bearer {access_token}"})


@pytest.fixture
def create_test_user():
    user_data = {
       "email": generate_unique_email(),
       "password": "test12345",
        "name": "User test"
    }

    response = requests.post(f"{BASE_URL}/auth/register", json=user_data, headers=HEADERS)
    access_token = response.json().get("accessToken")

    yield user_data, access_token

    requests.delete(f"{BASE_URL}/auth/user", headers={"Authorization": f"Bearer {access_token}"})