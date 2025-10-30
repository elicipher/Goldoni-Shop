from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('add_item/',views.CartAddItemView.as_view()),
    path('rud_item/<int:pk>/',views.CartItemUpdateView.as_view()),
    path('list_items/',views.CartItemListView.as_view()),
]
