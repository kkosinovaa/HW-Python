from rest_framework import serializers # імпортую базовий функціонал серіалізаторів з дрф щоб ганяти дані туди сюди

from apps.pizza.models import PizzaModel # підтягую нашу модель піци з якою будемо працювати


class PizzaSerializer(serializers.ModelSerializer): # створюю клас серіалізатора наслідуюсь від modelserializer щоб не писати ручками кожне поле
    class Meta: # клас мета суто для налаштувань
        model = PizzaModel # вказую що базою для цього серіалізатора є саме модель піци
        fields = ('id','name','size','price', 'updated_at', 'created_at') # тупо перераховую всі поля які хочу приймати і віддавати юзеру (тут до речі поки не додали поле піцерії)