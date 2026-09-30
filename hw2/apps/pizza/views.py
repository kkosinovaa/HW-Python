from rest_framework import status, viewsets, generics
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.pizza import serializers
from apps.pizza.filter import filter_pizza
from apps.pizza.models import PizzaModel
from apps.pizza.serializers import PizzaSerializer


# class PizzaListCreateView(APIView):
#     def get(self,*args, **kwargs):
#         pizzas = PizzaModel.objects.all()
#         serializer = PizzaSerializer(pizzas, many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)
#     def post(self,*args, **kwargs):
#       data =self.request.data
#       serializer = PizzaSerializer(data=data)
#       serializer.is_valid(raise_exception=True)
#       serializer.save()
#       return Response(serializer.data,status.HTTP_201_CREATED)
# class PizzaListCreateView(GenericAPIView,ListModelMixin,CreateModelMixin):
#     serializer_class = PizzaSerializer
#     def get_queryset(self):
#         return filter_pizza(self.request.query_params)
#
#
#     def get(self, request, *args, **kwargs):
#         return super().list(request, *args, **kwargs)
#     def post(self, request, *args, **kwargs):
#         return  super().create(request, *args, **kwargs)
class PizzaListCreateView(ListCreateAPIView):
    queryset = PizzaModel.objects.all()
    serializer_class = PizzaSerializer
    def get_queryset(self):
        return filter_pizza(self.request.query_params)


# class PizzaRetrieveUpdateDestroyAPIView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
#     serializer_class = PizzaSerializer
#
#     queryset = PizzaModel.objects.all()
#
#     def get(self, request, *args, **kwargs):
#         return
#
#     def retrieve(self, request, *args, **kwargs):
#         return super().retrieve(request, *args, **kwargs)
#     def put(self,*args, **kwargs):
#         return super().update(self.request, *args, **kwargs)
#     def patch(self, *args, **kwargs):
#         return super().partial_update(self.request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#          return super().destroy(self.request, *args, **kwargs)


#     def get(self,*args, **kwargs):
#         pk = kwargs['pk']
#         try:
#             pizza = PizzaModel.objects.get(pk=pk)
#         except PizzaModel.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         serializer = PizzaSerializer(pizza)
#         return Response(serializer.data,status=status.HTTP_200_OK)
#     def put(self, *args, **kwargs):
#         pk=kwargs['pk']
#         try:
#             pizza = PizzaModel.objects.get(pk=pk)
#         except PizzaModel.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#         data = self.request.data
#         serializer = PizzaSerializer(pizza,data=data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data,status.HTTP_200_OK)
class PizzaRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = PizzaSerializer
    queryset = PizzaModel.objects.all()
    http_method_names = ['get', 'put', 'delete']