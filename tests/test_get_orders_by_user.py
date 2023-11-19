import allure
import requests


class TestGetOrdersByUser:

    @allure.title('Проверка успешного получения заказов авторизоавнного юзера')
    def test_get_orders_authorized_user_successful_getting(self, base_url, user, make_order):

        headers = {'Authorization': user['access_token']}
        response = requests.get(f'{base_url}/orders', headers=headers)

        assert response.status_code == 200
        assert response.json().get("success") is True
        assert response.json()['orders'][0]['number'] == make_order

    @allure.title('Проверка ошибки получения заказов неавторизованного юзера')
    def test_get_orders_unauthorized_user_failed_getting(self, base_url):

        response = requests.get(f'{base_url}/orders')

        assert response.status_code == 401
        assert response.json().get("success") is False
        assert response.json()['message'] == 'You should be authorised'
