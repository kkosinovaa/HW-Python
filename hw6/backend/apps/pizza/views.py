from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from django_filters.rest_framework import DjangoFilterBackend

from apps.pizza.filter import PizzaFilter
from apps.pizza.models import PizzaModel
from apps.pizza.serializers import PizzaPhotoSerializer, PizzaSerializer

class PizzaListCreateView(ListCreateAPIView):
    serializer_class = PizzaSerializer

    def get_queryset(self):
        queryset = PizzaModel.objects.all()

        only_margarita = self.request.query_params.get("only_margarita")

        if only_margarita == "true":
            queryset = PizzaModel.objects.only_margarita()

        return queryset
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PizzaFilter
    # permission_classes = (IsAuthenticated,)
    permission_classes = (AllowAny,)
class PizzaRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = PizzaSerializer
    queryset = PizzaModel.objects.all()
    http_method_names = ['get', 'put', 'delete','patch']

    def perform_destroy(self, instance):
        instance.photo.delete(save=False)
        instance.delete()

class PizzaAddPhotoView(UpdateAPIView):
    serializer_class = PizzaPhotoSerializer
    queryset = PizzaModel.objects.all()
    permission_classes = (AllowAny,)
    http_method_names = ['put']
    def perform_update(self, serializer):
        pizza = self.get_object()
        pizza.photo.delete(save=False)
        super().perform_update(serializer)





