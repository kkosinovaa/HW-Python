from rest_framework import viewsets
from .models import Computer
from .serializers import ComputerSerializer

class ComputerViewSet(viewsets.ModelViewSet):
    queryset = Computer.objects.all()
    serializer_class = ComputerSerializer