from django.db import models

from core.models import BaseModel


class PizzaModel(BaseModel):
    class Meta:
        db_table = 'pizza'
    name = models.CharField(max_length=20)
    size = models.IntegerField()
    price = models.FloatField()
