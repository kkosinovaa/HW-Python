from django.db import models


# Create your models here.
class PizzaShopModel(models.Model):
    class Meta:
        db_table = 'pizza_shops'
    name = models.CharField(max_length=20)

