from rest_framework import serializers  # імпортуємо базові класи серіалізаторів з дрф, щоб перетворювати об'єкти пітони в json і навпаки

from apps.pizza.models import PizzaModel  # підтягуємо нашу модельку піци, щоб серіалізатор розумів, з якою таблицею він працює


class PizzaSerializer(
    serializers.ModelSerializer):  # створюємо наш клас серіалізатора, який наслідується від modelserializer. це розумна штука, яка сама згенерує поля на основі моделі
    class Meta:  # внутрішній клас мета потрібен для налаштувань самого серіалізатора
        model = PizzaModel  # вказуємо йому, що базою для серіалізації буде саме моделька піци
        fields = ('id', 'name', 'size', 'price', 'updated_at',
                  'created_at')  # явно перераховуємо всі поля, які хочемо приймати від юзера і віддавати йому (можна було б юзати '__all__', але так безпечніше і зрозуміліше)

    # далі йде закоментований блок - це те, як би виглядав код, якби ми юзали базовий serializers.serializer замість modelserializer
    # id = serializers.IntegerField(read_only=True) # ручками вказували б, що айдішка це ціле число, і воно read_only (ми його не передаємо при створенні, база генерує сама)
    # name = serializers.CharField(max_length=100) # ручками дублювали б поле імені та його максимальну довжину
    # size = serializers.FloatField() # вказували б, що розмір це число з плаваючою комою
    # price = serializers.FloatField() # так само для ціни
    # created_at = serializers.DateTimeField(read_only=True) # дата створення, теж тільки для читання
    # updated_at = serializers.DateTimeField(read_only=True) # дата оновлення
    #
    # def create(self, validated_data:dict): # в базовому серіалізаторі треба було б самому писати логіку створення об'єкта
    #     return PizzaModel.objects.create(**validated_data) # брали б очищені дані (validated_data), розпаковували їх і створювали запис в базі
    #
    # def update(self, instance:PizzaModel, validated_data:dict): # так само ручками треба було б писати логіку оновлення
    #     for k, v in validated_data.items(): # пробігались би циклом по словнику з новими даними
    #         setattr(instance, k, v) # через setattr змінювали б атрибути у нашої існуючої піци (instance) на нові
    #     instance.save() # зберігали б ці зміни в базу
    #     return instance # і повертали б оновлений об'єкт. а зараз завдяки modelserializer вся ця логіка (create та update) працює під капотом автоматично!