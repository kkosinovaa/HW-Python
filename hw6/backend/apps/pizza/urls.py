from django.urls import path

from .views import (
    PizzaAddPhotoView,
    PizzaListCreateView,
    PizzaRetrieveUpdateDestroyView
)


urlpatterns = [
    path(
        '',
        PizzaListCreateView.as_view(),
        name='pizza_list_create'
    ),
    path(
        '/<int:pk>',
        PizzaRetrieveUpdateDestroyView.as_view(),
        name='pizza_retrieve_update_destroy'
    ),
    path(
        '/<int:pk>/photos',
        PizzaAddPhotoView.as_view(),
        name='pizza_add_photo'
    ),
]