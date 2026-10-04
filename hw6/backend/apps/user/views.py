from django.contrib.auth import get_user_model

from rest_framework import generics
from rest_framework.generics import ListCreateAPIView

from apps.user.serializers import UserSerializer

# Create your views here.
UserModel =get_user_model()

class UserListCreateView(ListCreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class= UserSerializer
