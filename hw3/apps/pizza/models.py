from django.db import models # імпортую базовий функціонал джанги для роботи з базами даних і створення полів

from core.models import BaseModel # підтягую нашу абстрактну модельку (з датами створення/оновлення), щоб взяти її за основу

class PizzaModel(BaseModel): # створюю саму модель піци, наслідуючись від нашої базової моделі, щоб автоматично отримати поля created_at та updated_at
    class Meta: # внутрішній клас для додаткових налаштувань самої таблиці
        db_table = 'pizzas' # явно вказую, щоб табличка в базі називалась 'pizzas' (до речі, в минулому варіанті було 'pizza')
    name = models.CharField(max_length=20) # текстове поле для назви піци, обов'язково обмежую довжину до 20 символів
    size = models.IntegerField() # поле для розміру піци, зберігає просто цілі числа
    price =models.FloatField() # поле для ціни, тут float, щоб можна було зберігати числа з крапкою (з копійками)
    pizza_shop = models.ForeignKey('pizza_shop.PizzaShopModel', on_delete=models.CASCADE, related_name='pizzas') # а ось це нове! роблю зв'язок один-до-багатьох (foreign key) з моделлю піцерії. on_delete=models.CASCADE означає, що якщо ми видалимо піцерію з бази, то всі її піци теж автоматично видаляться. related_name='pizzas' дає змогу звертатися до піц прямо з об'єкта піцерії (типу my_shop.pizzas.all())