from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from apps.pizza.models import PizzaModel
from apps.pizza_shop.models import PizzaShopModel
from apps.user.models import UserModel


class PizzaAPITestCase(APITestCase):

    def setUp(self):
        pizza_shop = PizzaShopModel.objects.create(
            name='PizzaShop'
        )

        self.pizza1 = PizzaModel.objects.create(
            name='Pizzaone',
            size=30,
            price=200,
            days='Monday',
            pizza_shop=pizza_shop
        )

        self.pizza2 = PizzaModel.objects.create(
            name='Pizzatwo',
            size=30,
            price=200,
            days='Monday',
            pizza_shop=pizza_shop
        )

        self.pizza3 = PizzaModel.objects.create(
            name='Pizzathree',
            size=30,
            price=200,
            days='Monday',
            pizza_shop=pizza_shop
        )

    def _authenticate(self):
        user = UserModel.objects.create_user(
            email='admin@gmail.com',
            password='admin'
        )

        user.is_active = True
        user.save()

        res = self.client.post(
            reverse('auth_login'),
            data={
                'email': user.email,
                'password': 'admin'
            }
        )

        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + res.data['access']
        )

    def test_get_all_pizzas(self):
        res = self.client.get(
            reverse('pizza_list_create')
        )

        self.assertEqual(
            res.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            len(res.data['data']),
            3
        )

        pizza_names = list(
            reversed([
                'Pizzaone',
                'Pizzatwo',
                'Pizzathree'
            ])
        )

        for i, pizza in enumerate(PizzaModel.objects.all()):
            self.assertEqual(
                pizza.name,
                pizza_names[i]
            )

    def test_create_pizza_without_auth(self):
        count_before = PizzaModel.objects.count()

        res = self.client.post(
            reverse('pizza_list_create'),
            data={
                'name': 'Testpizza',
                'size': 30,
                'price': 250,
                'days': 'Tuesday'
            }
        )

        self.assertEqual(
            res.status_code,
            status.HTTP_401_UNAUTHORIZED
        )

        count_after = PizzaModel.objects.count()

        self.assertEqual(
            count_after - count_before,
            0
        )

    def test_create_pizza_with_auth(self):
        self._authenticate()

        count_before = PizzaModel.objects.count()

        res = self.client.post(
            reverse('pizza_list_create'),
            data={
                'name': 'Testpizza',
                'size': 30,
                'price': 250,
                'days': 'Tuesday'
            }
        )

        self.assertEqual(
            res.status_code,
            status.HTTP_201_CREATED
        )

        count_after = PizzaModel.objects.count()

        self.assertEqual(
            count_after - count_before,
            1
        )