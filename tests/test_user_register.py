import allure
import pytest
import requests
from helpers import generate_login, generate_password, generate_username


class TestUserRegistration:

    @allure.title('Проверка успешного создания нового юзера')
    def test_register_successful_registration(self, base_url, user_generate_and_delete):
        payload = {
            'email': user_generate_and_delete['email'],
            'password': user_generate_and_delete['password'],
            'name': user_generate_and_delete['name']
        }
        response = requests.post(f'{base_url}/auth/register', data=payload)

        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title('Проверка ошибки создания юзера: повторное создание существующего юзера')
    def test_register_duplicate_user_failed_registration(self, base_url, user):

        payload = {
            'email': user['email'],
            'password': user['password'],
            'name': user['name']
        }
        response = requests.post(f'{base_url}/auth/register', data=payload)

        assert response.status_code == 403
        assert response.json().get("success") is False
        assert response.json()['message'] == 'User already exists'

    @allure.title('Проверка ошибки создания юзера: запросы без обязательных полей "email"/"password"/"name"')
    @pytest.mark.parametrize('payload', [
        {'email': generate_login(), 'name': generate_username(5)},
        {'email': generate_login(), 'password': generate_password(6)},
        {'password': generate_password(6), 'name': generate_username(5)}
    ])
    def test_register_no_required_field_failed_registration(self, base_url, payload):
        response = requests.post(f'{base_url}/auth/register', data=payload)

        assert response.status_code == 403
        assert response.json().get("success") is False
        assert response.json()['message'] == 'Email, password and name are required fields'
