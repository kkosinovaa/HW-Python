from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.request import Request

from django_filters.rest_framework import DjangoFilterBackend

from apps.pizza.filter import PizzaFilter
from apps.pizza.models import PizzaModel
from apps.pizza.serializers import PizzaSerializer

class PizzaListCreateView(ListCreateAPIView):
    serializer_class = PizzaSerializer
    # def get_queryset(self):
    #     request:Request = self.request
    #     return filter_pizza(request.query_params)
    queryset = PizzaModel.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PizzaFilter


class PizzaRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = PizzaSerializer
    queryset = PizzaModel.objects.all()
    http_method_names = ['get', 'put', 'delete','patch']