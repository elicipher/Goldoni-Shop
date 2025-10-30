from rest_framework.views import APIView 
from rest_framework.generics import RetrieveUpdateDestroyAPIView , ListAPIView , CreateAPIView
from .models import Cart , CartItem , Order , OrderItem
from .serializers import CartItemCreateSerializer , CartItemListSerializers
from rest_framework.response import Response
from rest_framework import status

# Create your views here.



class CartAddItemView(CreateAPIView):
    serializer_class = CartItemCreateSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = serializer.validated_data["product"]
        quantity = serializer.validated_data.get("quantity", 1)
        cart, _ = Cart.objects.get_or_create(user=request.user)

        cart_item = CartItem.objects.filter(cart=cart, product=product)
        if cart_item.exists():
            cart_item.delete()
            return Response({"message": "کالا از سبد خرید حذف شد"}, status=status.HTTP_200_OK)
        else:
            self.perform_create(serializer, cart, quantity)
            return Response({"message": "کالا به سبد خرید شما اضافه شد"}, status=status.HTTP_200_OK)
        
    def perform_create(self, serializer, cart, quantity):
        CartItem.objects.create(
            product=serializer.validated_data["product"],
            quantity=quantity,
            cart=cart
        )

            
class CartItemUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    def get_queryset(self):
        return CartItem.objects.filter(cart__user = self.request.user)
    
    def get_serializer_class(self):
        if self.request.method in ['PATCH' , 'DELETE' , 'PUT']:
            return CartItemCreateSerializer
        return CartItemListSerializers
    

class CartItemListView(ListAPIView):
    serializer_class = CartItemListSerializers
    queryset = CartItem.objects.all()

    def get_queryset(self):
        return CartItem.objects.filter(cart__user = self.request.user)
    





