from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView # тягну готові класи з дрф щоб не писати базові crud операції руками
from rest_framework.request import Request # імпортую клас реквесту суто для типізації щоб редактор коду краще підказував

from apps.pizza.filter import filter_pizza # підтягую нашу самописну функцію для фільтрації піц
from apps.pizza.models import PizzaModel # імпортую модельку піци
from apps.pizza.serializers import PizzaSerializer # імпортую серіалізатор для піци


# Create your views here.
class PizzaListCreateView(ListCreateAPIView): # клас для списку всіх піц та створення нової наслідується від зручного дженеріка
    serializer_class = PizzaSerializer # просто кажу який серіалізатор тут юзати
    def get_queryset(self): # перевизначаю метод діставання даних з бази
        request:Request = self.request # зберігаю запит в змінну і відразу типізую його
        return filter_pizza(request.query_params) # проганяю параметри урла через нашу функцію і віддаю відфільтровані піци


# RetrieveUpdateDestroyAPIView дає нам повністю готовий crud для одного об'єкта.
    # порівняно з ручним APIView нам не треба писати методи get, put, patch чи delete руками.
    # він сам шукає запис в базі по id (і сам видає 404 помилку, якщо такого id немає),
    # сам проганяє дані через серіалізатор, перевіряє їх на валідність і зберігає або видаляє.
    # тобто замість десятків рядків коду ми просто даємо йому кверісет і серіалізатор,
    # а всю рутину з базою і відповідями він робить під капотом.
class PizzaRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView): # клас для операцій над однією піцою по айдішці
    serializer_class = PizzaSerializer # теж прив'язую серіалізатор
    queryset = PizzaModel.objects.all() # вказую базовий запит до бази з якого в'юха сама буде шукати потрібну піцу
    http_method_names = ['get', 'put', 'delete','patch'] # явно вказую які http методи тут дозволені (додали patch для часткового оновлення)