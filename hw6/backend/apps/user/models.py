from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from core.models import BaseModel

from apps.user.managers import UserManager


# Create your models here.
class UserModel(AbstractBaseUser, PermissionsMixin,BaseModel):
    class Meta:
        db_table = 'auth_user'
        ordering = ['-id',]
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) #чи є адміністратором

    USERNAME_FIELD = 'email'#поле яке відповідає за логін
    objects = UserManager()

class ProfileModel(BaseModel):
    class Meta:
        db_table = 'profile'
        ordering = ['-id',]
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    age = models.IntegerField()
    user =models.OneToOneField(UserModel, on_delete=models.CASCADE,related_name='profile')
    objects = models.Manager()
