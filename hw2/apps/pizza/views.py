from rest_framework import status, viewsets, generics # імпортуємо статуси відповідей, в'юсети та дженеріки з дрф
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView # тягнемо базові класи для в'юх, які вже мають під капотом купу готової логіки
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin # імпортуємо міксіни, це такі шматочки коду, які додають конкретну поведінку (список, створення, видалення і тд)
from rest_framework.response import Response # тягнемо клас для формування правильної http-відповіді
from rest_framework.views import APIView # це найбазовіший клас для створення в'юх в дрф, від якого все росте

from apps.pizza import serializers # імпортуємо файл з серіалізаторами
from apps.pizza.filter import filter_pizza # підтягуємо нашу самописну функцію для фільтрації піц, яку розбирали в минулому файлі
from apps.pizza.models import PizzaModel # тягнемо модельку піци, щоб в'юхи знали з якою таблицею в бд працювати
from apps.pizza.serializers import PizzaSerializer # імпортуємо сам серіалізатор, який переганяє дані з бд в json і навпаки


# class PizzaListCreateView(APIView): # це самий перший спосіб, коли писали все руцями через базовий apiview
#     def get(self,*args, **kwargs): # метод для обробки get запиту (отримати всі піци)
#         pizzas = PizzaModel.objects.all() # дістаємо всі піци з бази
#         serializer = PizzaSerializer(pizzas, many=True) # запихаємо кверісет в серіалізатор, many=true бо об'єктів багато (список)
#         return Response(serializer.data,status=status.HTTP_200_OK) # повертаємо джейсончик з 200 статусом
#     def post(self,*args, **kwargs): # метод для створення нової піци (post запит)
#       data =self.request.data # дістаємо тіло запиту (те, що прислав юзер)
#       serializer = PizzaSerializer(data=data) # передаємо ці дані в серіалізатор для перевірки
#       serializer.is_valid(raise_exception=True) # перевіряємо чи валідні дані, якщо ні - автоматично кине помилку 400
#       serializer.save() # зберігаємо нову піцу в базу
#       return Response(serializer.data,status.HTTP_201_CREATED) # повертаємо створену піцу і статус 201 (створено)

# class PizzaListCreateView(GenericAPIView,ListModelMixin,CreateModelMixin): # другий етап еволюції: юзаємо дженерік і підключаємо міксіни для списку і створення
#     serializer_class = PizzaSerializer # вказуємо, який серіалізатор буде працювати з цією в'юхою
#     def get_queryset(self): # перевизначаємо метод отримання кверісету
#         return filter_pizza(self.request.query_params) # проганяємо наші параметри з урла через ту саму функцію фільтрації
#
#
#     def get(self, request, *args, **kwargs): # тут ми просто ловимо get запит
#         return super().list(request, *args, **kwargs) # і передаємо його під капот міксіну list, який сам все зробить
#     def post(self, request, *args, **kwargs): # аналогічно для post запиту
#         return  super().create(request, *args, **kwargs) # передаємо логіку на міксін create

class PizzaListCreateView(ListCreateAPIView): # і ось фінальний, найкоротший варіант. цей клас вже містить в собі genericapiview та обидва міксіни (list та create)
    queryset = PizzaModel.objects.all() # задаємо базовий кверісет для в'юхи (всі піци)
    serializer_class = PizzaSerializer # прив'язуємо серіалізатор
    def get_queryset(self): # знову перевизначаємо метод для діставання даних
        return filter_pizza(self.request.query_params) # щоб замість всіх піц, воно повертало відфільтровані через нашу кастомну функцію filter_pizza


# class PizzaRetrieveUpdateDestroyAPIView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin): # це був проміжний варіант для в'юхи конкретної піци (по id), з використанням міксінів
#     serializer_class = PizzaSerializer # вказували серіалізатор
#
#     queryset = PizzaModel.objects.all() # вказували базовий кверісет для пошуку
#
#     def get(self, request, *args, **kwargs): # мабуть тут мала бути логіка діставання однієї піци
#         return
#
#     def retrieve(self, request, *args, **kwargs): # метод retrieve з міксіна для діставання одного об'єкта
#         return super().retrieve(request, *args, **kwargs) # делегуємо роботу міксіну
#     def put(self,*args, **kwargs): # обробка повного оновлення
#         return super().update(self.request, *args, **kwargs) # делегуємо міксіну update
#     def patch(self, *args, **kwargs): # обробка часткового оновлення
#         return super().partial_update(self.request, *args, **kwargs) # делегуємо міксіну
#
#     def delete(self, request, *args, **kwargs): # обробка видалення
#          return super().destroy(self.request, *args, **kwargs) # віддаємо на міксін destroy


#     def get(self,*args, **kwargs): # ще більш старий спосіб дістати одну піцу руцями
#         pk = kwargs['pk'] # витягуємо id (primary key) з урла
#         try: # пробуємо...
#             pizza = PizzaModel.objects.get(pk=pk) # знайти піцу в базі по цьому id
#         except PizzaModel.DoesNotExist: # якщо такої немає в базі
#             return Response(status=status.HTTP_404_NOT_FOUND) # повертаємо 404 помилку
#         serializer = PizzaSerializer(pizza) # якщо є - серіалізуємо
#         return Response(serializer.data,status=status.HTTP_200_OK) # і віддаємо джейсон юзеру
#     def put(self, *args, **kwargs): # старий метод для повного оновлення руцями
#         pk=kwargs['pk'] # знов беремо айді з урла
#         try:
#             pizza = PizzaModel.objects.get(pk=pk) # шукаємо в базі об'єкт, який хочемо оновити
#         except PizzaModel.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND) # якщо нема - 404
#         data = self.request.data # беремо нові дані з тіла запиту
#         serializer = PizzaSerializer(pizza,data=data) # передаємо в серіалізатор існуючу піцу і нові дані для оновлення
#         serializer.is_valid(raise_exception=True) # перевіряємо чи все ок з даними
#         serializer.save() # зберігаємо зміни в базу
#         return Response(serializer.data,status.HTTP_200_OK) # віддаємо оновлену піцу


class PizzaRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView): # фінальна магія дрф: цей клас вже вміє і діставати, і оновлювати, і видаляти по id. замінює весь той закоментований код
    serializer_class = PizzaSerializer # просто кажемо йому який серіалізатор юзати
    queryset = PizzaModel.objects.all() # і вказуємо з якої таблиці брати дані для роботи
    http_method_names = ['get', 'put', 'delete'] # обмежуємо методи: дозволяємо тільки читати, повністю оновлювати та видаляти (тут наприклад відключено patch)