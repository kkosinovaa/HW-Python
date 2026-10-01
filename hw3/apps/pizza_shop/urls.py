from django.urls import path # дістаю функцію path з джанги щоб прописувати маршрути

from apps.pizza_shop.views import PizzaShopAddPizzaView, PizzaShopListCreateView # імпортую наші в'юхи для піцерії щоб прив'язати їх до урлів

urlpatterns = [ # стандартний список маршрутів
    path('', PizzaShopListCreateView.as_view()), # пустий шлях для отримання списку всіх піцерій або створення нової
    path('/<int:pk>/pizzas', PizzaShopAddPizzaView.as_view()), # вкладений шлях щоб додавати піци до конкретної піцерії по її айдішці
]