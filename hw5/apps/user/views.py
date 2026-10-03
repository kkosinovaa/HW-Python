from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.response import Response

from apps.user.serializers import UserSerializer
from rest_framework.permissions import IsAdminUser, AllowAny

UserModel =get_user_model()

class UserListCreateView(ListCreateAPIView):
    queryset = UserModel.objects.all()
    serializer_class= UserSerializer
    permission_classes = [AllowAny]

class BlockUserView(GenericAPIView):
    permission_classes = [IsAdminUser]
    def get_queryset(self):#
        return UserModel.objects.exclude(id=self.request.user.id)

    def patch(self,request,*args,**kwargs):
        user=self.get_object()
        if user.is_active:
            user.is_active=False
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)

class UnBlockUserView(GenericAPIView):
    permission_classes = [IsAdminUser]
    def get_queryset(self):#
        return UserModel.objects.exclude(id=self.request.user.id)

    def patch(self,request,*args,**kwargs):
        user=self.get_object()
        if not user.is_active:
            user.is_active=True
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)

class UserToAdminView(GenericAPIView):
    permission_classes = [IsAdminUser]
    def get_queryset(self):#
        return UserModel.objects.exclude(id=self.request.user.id)

    def patch(self,request,*args,**kwargs):
        user=self.get_object()
        if not user.is_staff:
            user.is_staff=True
            user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)

