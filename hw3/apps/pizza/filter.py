from django.db.models import QuerySet # імпортую кверісет, щоб підказати тип результату функції
from django.http import QueryDict # тягну тип для параметрів запиту, які прилітають з урла

from rest_framework.exceptions import ValidationError # дістаю помилку з дрф, щоб гарно відбивати криві запити

from apps.pizza.models import PizzaModel # підтягую нашу модельку піци


def filter_pizza (query:QueryDict) ->QuerySet: # функція для фільтрації, на вхід бере кверідікт, віддає готовий кверісет
    qs= PizzaModel.objects.all() # витягую абсолютно всі піци з бази, це наша основа на яку будемо вішати фільтри
    for k, v in query.items(): # пробігаюсь циклом по всіх переданих параметрах, розбиваю на ключ (k) і значення (v)
      match k: # юзаю конструкцію match-case для зручної перевірки ключа
        case 'price_gt': # якщо юзер передав price_gt (ціна більша за)
            qs=qs.filter(price__gt=v) # докидаю фільтр у кверісет, щоб ціна була строго більша за вказане значення
        case 'price_lt': # якщо прилетів ключ price_lt (ціна менша за)
            qs=qs.filter(price__lt=v) # фільтрую так, щоб залишилися тільки ті піци, що дешевші
        case _: # якщо прислали якийсь лівий ключ, якого ми не чекали
             raise ValidationError({'detail': f'"{k}" not allowed'}) # викидаю 400 помилку з текстом, що такий параметр не дозволений
    return qs # повертаю повністю відфільтрований результат