"""
URL configuration for configs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path

urlpatterns = [
# include працює як делегатор: він каже джанзі "всі запити, що починаються на 'pizzas', шукай у файлі apps.pizza.urls".
    # 'pizzas' тут виступає базовим префіксом. джанга бере цей префікс і автоматично приклеює до нього маршрути з підключеного файлу.
    # тобто, якщо в apps.pizza.urls лежить шлях '/<int:pk>', то під капотом вони склеяться докупи і вийде фінальний урл 'pizzas/<int:pk>'
    path('pizzas', include('apps.pizza.urls')),
    path('pizza_shops', include('apps.pizza_shop.urls')),
]