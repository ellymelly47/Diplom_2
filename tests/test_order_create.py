import allure
import requests


class TestOrderCreation:

    @allure.title('Проверка успешного создания заказа с авторизацией')
    def test_orders_authorized_user_successful_creation(self, base_url, user, get_ingredients):

        payload = {
            'ingredients': [get_ingredients[0], get_ingredients[1], get_ingredients[2]]
        }
        headers = {'Authorization': user['access_token']}
        response = requests.post(f'{base_url}/orders', data=payload, headers=headers)

        assert response.status_code == 200
        assert response.json().get("success") is True
        assert 'number' in response.json()['order'] and isinstance(response.json()['order']['number'], int)

    @allure.title('Проверка успешного создания заказа без авторизации')
    def test_orders_unauthorized_user_successful_creation(self, base_url, get_ingredients):

        payload = {
            'ingredients': [get_ingredients[0], get_ingredients[1], get_ingredients[2]]
        }
        response = requests.post(f'{base_url}/orders', data=payload)

        assert response.status_code == 200
        assert response.json().get("success") is True
        assert 'number' in response.json()['order'] and isinstance(response.json()['order']['number'], int)

    @allure.title('Проверка ошибки создания зазказа без ингредиентов')
    def test_orders_no_ingredients_failed_creation(self, base_url, user):

        payload = {
            'ingredients': []
        }
        headers = {'Authorization': user['access_token']}
        response = requests.post(f'{base_url}/orders', data=payload, headers=headers)

        assert response.status_code == 400
        assert response.json().get("success") is False
        assert response.json()['message'] == 'Ingredient ids must be provided'

    @allure.title('Проверка ошибки создания заказа с некорректным ингердиентом')
    def test_orders_incorrect_ingredients_failed_creation(self, base_url, user):

        payload = {
            'ingredients': ["12345678"]
        }
        headers = {'Authorization': user['access_token']}
        response = requests.post(f'{base_url}/orders', data=payload, headers=headers)

        assert response.status_code == 500
        assert 'Internal Server Error' in response.text
