from django.urls import path
from . import views


urlpatterns = [
    path('add_item/',views.CartAddItemView.as_view()),
    path('rud_item/<int:pk>/',views.CartItemUpdateView.as_view()),
    path('list_items/',views.CartItemListView.as_view()),
    path('order/',views.OrderCreateView.as_view()),
    path('order/shipping/',views.OrderListshippingView.as_view()),
    path('order/delivered/',views.OrderListDeliveredView.as_view()),
    path('order/returned/',views.OrderListReturnedView.as_view()),
    path('order/all/',views.OrderListView.as_view()),
    path('order/retrieve/<uuid:order_id>/',views.OrderItemRetrieveView.as_view()),
]
