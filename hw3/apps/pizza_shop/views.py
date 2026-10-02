from rest_framework import status # імпортую статуси для відповідей щоб не писати цифри руками
from rest_framework.generics import GenericAPIView, ListCreateAPIView # тягну базові класи дрф для в'юх щоб зекономити час
from rest_framework.response import Response # клас для формування правильної відповіді клієнту

from apps.pizza.serializers import PizzaSerializer # підтягую серіалізатор піци бо будемо її тут створювати
from apps.pizza_shop.models import PizzaShopModel # імпортую модельку піцерії
from apps.pizza_shop.serializer import PizzaShopSerializer # і її серіалізатор теж тягну


class PizzaShopListCreateView(ListCreateAPIView): # стандартна в'юха для списку піцерій і створення нової
    serializer_class = PizzaShopSerializer # вказую який серіалізатор тут працює
    queryset = PizzaShopModel.objects.all() # кажу джанзі де брати піцерії з бази

class PizzaShopAddPizzaView(GenericAPIView): # кастомна в'юха щоб додавати нову піцу в конкретну піцерію
    queryset = PizzaShopModel.objects.all() # базовий запит щоб метод get_object міг знайти піцерію по айдішці з урла

    def post(self, *args, **kwargs): # обробляю пост запит для створення
        pizza_shop = self.get_object() # магія дрф яка сама шукає піцерію в базі по pk з урла
        data = self.request.data # дістаю те що прислав юзер в json
        serializer = PizzaSerializer(data=data) # передаю ці дані в серіалізатор піци для валідації
        serializer.is_valid(raise_exception=True) # перевіряю чи все ок якщо ні то автоматично вилетить помилка 400
        serializer.save(pizza_shop = pizza_shop) # зберігаю піцу і жорстко прив'язую її до піцерії яку ми знайшли вище
        shop_serializer = PizzaShopSerializer(instance=pizza_shop) # пакую оновлену піцерію назад в серіалізатор
        return Response(shop_serializer.data, status=status.HTTP_201_CREATED) # повертаю дані піцерії і статус 201 що все успішно створено