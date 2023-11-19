import allure
import requests
from helpers import generate_login, generate_password


class TestUserLogin:

    @allure.title('Проверка успешного логина существующего юзера')
    def test_login_successful_login(self, base_url, user):
        payload = {
            'email': user['email'],
            'password': user['password']
        }
        response = requests.post(f'{base_url}/auth/login', data=payload)

        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title('Проверка ошибки логина: запрос с некорректным логином')
    def test_login_incorrect_email_failed_login(self, base_url, user):

        payload = {
            'email': generate_login(),
            'password': user['password']
        }
        response = requests.post(f'{base_url}/auth/login', data=payload)

        assert response.status_code == 401
        assert response.json().get("success") is False
        assert response.json()['message'] == 'email or password are incorrect'

    @allure.title('Проверка ошибки логина: запрос с некорректным паролем')
    def test_login_incorrect_password_failed_login(self, base_url, user):

        payload = {
            'email': user['email'],
            'password': generate_password(6)
        }
        response = requests.post(f'{base_url}/auth/login', data=payload)

        assert response.status_code == 401
        assert response.json().get("success") is False
        assert response.json()['message'] == 'email or password are incorrect'
