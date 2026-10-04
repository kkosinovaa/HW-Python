


from django_filters import rest_framework as filters

from apps.pizza.models import DaysChoices
from apps.pizza.serializers import PizzaSerializer


class PizzaFilter(filters.FilterSet):
  name_starts_with = filters.CharFilter(field_name='name', lookup_expr='startswith')
  name_ends_with = filters.CharFilter(field_name='name', lookup_expr='endswith')
  name_contains = filters.CharFilter(field_name='name', lookup_expr='contains')

  days_starts_with = filters.CharFilter(field_name='days', lookup_expr='startswith')
  days_ends_with = filters.CharFilter(field_name='days', lookup_expr='endswith')
  days_contains = filters.CharFilter(field_name='days', lookup_expr='contains')

  size_gt = filters.NumberFilter(field_name='size', lookup_expr='gt')
  size_lt = filters.NumberFilter(field_name='size', lookup_expr='lt')
  size_gte = filters.NumberFilter(field_name='size', lookup_expr='gte')
  size_lte = filters.NumberFilter(field_name='size', lookup_expr='lte')

  price_gt = filters.NumberFilter(field_name='price', lookup_expr='gt')
  price_lt = filters.NumberFilter(field_name='price', lookup_expr='lt')
  price_gte = filters.NumberFilter(field_name='price', lookup_expr='gte')
  price_lte = filters.NumberFilter(field_name='price', lookup_expr='lt')

  order=filters.OrderingFilter(
      fields= PizzaSerializer.Meta.fields
  )


