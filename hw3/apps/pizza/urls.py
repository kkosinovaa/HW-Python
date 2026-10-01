from django.urls import path # імпортую функцію path з джанги щоб прописувати маршрути

from .views import PizzaListCreateView, PizzaRetrieveUpdateDestroyView # підтягую наші в'юхи з сусіднього файлу views щоб прив'язати їх до урлів

urlpatterns = [ # створюю список маршрутів який джанга шукає за замовчуванням
    path("", PizzaListCreateView.as_view()), # базовий шлях для списку всіх піц та створення нової і обов'язково викликаю as_view
    path("/<int:pk>", PizzaRetrieveUpdateDestroyView.as_view()), # шлях для конкретної піци де чекаємо айдішку як ціле число щоб діставати чи видаляти запис
]