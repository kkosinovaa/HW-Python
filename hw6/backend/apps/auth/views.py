from django.contrib.auth import get_user_model

from rest_framework import status
# Create your views here.
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from core.services.email_service import EmailService
from core.services.jwt_service import ActivateToken, JWTService, RecoveryToken, SocketToken

from apps.auth.serializers import EmailSerializer, PasswordSerializer
from apps.user.serializers import UserSerializer

UserModel = get_user_model()

class ActivateUserView(GenericAPIView):
    permission_classes = (AllowAny,)

    def patch(self, *args, **kwargs):
        token = kwargs['token']
        user = JWTService.verify_token(token, ActivateToken)
        user.is_active = True
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)

class RecoveryRequestView(GenericAPIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        data = request.data

        serializer=EmailSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        user=get_object_or_404(UserModel,email=serializer.validated_data['email'])
        EmailService.recovery(user)
        return Response({'details':'link send to email'}, status.HTTP_200_OK)

class RecoveryPasswordView(GenericAPIView):
    permission_classes = (AllowAny,)
    def post(self, *args, **kwargs):
        data = self.request.data
        serializer=PasswordSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        token=kwargs['token']
        user=JWTService.verify_token(token, RecoveryToken)
        user.set_password(serializer.validated_data['password'])
        user.save()
        return Response(status=status.HTTP_200_OK)


class SocketTokenView(GenericAPIView):
    # socket token може отримати тільки авторизований користувач
    permission_classes = (IsAuthenticated,)

    def get(self, *args, **kwargs):
        # створюємо короткий токен для websocket підключення
        token = JWTService.create_token(
            user=self.request.user,
            token_class=SocketToken
        )

        # повертаємо токен клієнту
        return Response({'token': str(token)}, status.HTTP_200_OK)

