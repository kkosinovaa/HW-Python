from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ComputerViewSet

router = DefaultRouter()
router.register(r'computers', ComputerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]