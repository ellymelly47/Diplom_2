import allure
import pytest
import requests
from helpers import generate_login, generate_password, generate_username


class TestUserChangeData:

    @allure.title('Проверка успешного изменения почты авторизованного юзера')
    def test_user_authorized_change_email_successful(self, base_url, user):
        new_email = generate_login()
        payload = {'email': new_email}
        headers = {'Authorization': user['access_token']}
        response = requests.patch(f'{base_url}/auth/user', data=payload, headers=headers)

        assert response.status_code == 200
        assert response.json().get("success") is True
        assert response.json()['user']['email'] == new_email

    @allure.title('Проверка успешного изменения имени авторизованного юзера')
    def test_user_authorized_change_name_successful(self, base_url, user):
        new_name = generate_username(5)
        payload = {'name': new_name}
        headers = {'Authorization': user['access_token']}
        response = requests.patch(f'{base_url}/auth/user', data=payload, headers=headers)

        assert response.status_code == 200
        assert response.json().get("success") is True
        assert response.json()['user']['name'] == new_name

    @allure.title('Проверка успешного изменения пароля авторизованного юзера')
    def test_user_authorized_change_password_successful(self, base_url, user):
        new_password = generate_login()
        payload = {'email': new_password}
        headers = {'Authorization': user['access_token']}
        response = requests.patch(f'{base_url}/auth/user', data=payload, headers=headers)

        assert response.status_code == 200
        assert response.json().get("success") is True

    @allure.title('Проверка ошибки изменения почты/пароля/имени неавторизованного юзера')
    @pytest.mark.parametrize('payload', [
        {'email': generate_login()},
        {'password': generate_password(6)},
        {'name': generate_username(5)}
    ])
    def test_user_unauthorized_change_failed(self, base_url, payload):

        response = requests.patch(f'{base_url}/auth/user', data=payload)

        assert response.status_code == 401
        assert response.json().get("success") is False
        assert response.json()['message'] == 'You should be authorised'
