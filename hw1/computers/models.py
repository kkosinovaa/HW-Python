from django.db import models

class Computer(models.Model):
    brand = models.CharField(max_length=100, verbose_name="Бренд")
    model_name = models.CharField(max_length=100, verbose_name="Модель")
    cpu = models.CharField(max_length=100, verbose_name="Процесор")
    ram_gb = models.IntegerField(verbose_name="Об'єм ОЗП (ГБ)")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна")

    def __str__(self):
        return f"{self.brand} {self.model_name}"