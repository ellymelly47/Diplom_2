import pytest
import requests
from helpers import generate_login, generate_password, generate_username


@pytest.fixture
def base_url():
    return 'https://stellarburgers.nomoreparties.site/api'


@pytest.fixture
def get_ingredients(base_url):
    bun = None
    main = None
    sauce = None
    response = requests.get(f'{base_url}/ingredients')
    ingredients = response.json()['data']
    for ingredient in ingredients:
        if ingredient['type'] == 'bun':
            bun = ingredient['_id']
        elif ingredient['type'] == 'main':
            main = ingredient['_id']
        elif ingredient['type'] == 'sauce':
            sauce = ingredient['_id']
    return bun, main, sauce


@pytest.fixture
def user(base_url):
    email = generate_login()
    password = generate_password(6)
    name = generate_username(5)

    payload = {
        'email': email,
        'password': password,
        'name': name
    }
    response = requests.post(f'{base_url}/auth/register', data=payload)
    access_token = response.json().get("accessToken")

    yield {
        'email': email,
        'password': password,
        'name': name,
        'access_token': access_token
    }
    headers = {'Authorization': access_token}
    requests.delete(f'{base_url}/auth/user', headers=headers)


@pytest.fixture
def make_order(base_url, user):
    order_payload = {
        'ingredients': ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]
    }
    headers = {'Authorization': user['access_token']}
    response = requests.post(f'{base_url}/orders', data=order_payload, headers=headers)
    order_number = response.json()['order']['number']
    return order_number


@pytest.fixture
def user_generate_and_delete(base_url):

    email = generate_login()
    password = generate_password(6)
    name = generate_username(5)

    yield {
        'email': email,
        'password': password,
        'name': name
    }
    payload = {
        'email': email,
        'password': password
        }
    response = requests.post(f'{base_url}/auth/login', data=payload)
    access_token = response.json().get("accessToken")

    headers = {'Authorization': access_token}
    requests.delete(f'{base_url}/auth/user', headers=headers)
