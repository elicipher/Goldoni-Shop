from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView , ListAPIView , CreateAPIView
from .models import Cart , CartItem , Order , OrderItem
from .serializers import CartItemCreateSerializer , CartSerializers , CartItemListSerializers , OrderSerializers , OrderItemSerializers
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema


# Create your views here.

class CartAddItemView(CreateAPIView):
    """
    Add or remove a product from the user's cart.

    POST request behavior:
    - If the product already exists in the cart, it will be removed.
    - If the product does not exist in the cart, it will be added with the specified quantity.

    Expected request data:
    {
        "product": <product_id>,
        "quantity": <optional, default=1>
    }

    Response:
    - 200 OK with a message indicating whether the item was added or removed.
    """

    serializer_classes = CartItemCreateSerializer
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        tags=['Cart'],
    )
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
        """Create a new CartItem in the cart with the specified quantity."""
        CartItem.objects.create(
            product=serializer.validated_data["product"],
            quantity=quantity,
            cart=cart
        )


class CartItemUpdateView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a single CartItem belonging to the current user.

    GET request:
    - Retrieve details of a single cart item.

    PATCH/PUT request:
    - Update quantity of the cart item.

    DELETE request:
    - Remove the cart item from the cart.
    """
    permission_classes = [IsAuthenticated]

    queryset = CartItem.objects.all()
    @swagger_auto_schema(
        tags=['Cart'],
    )
    def get_queryset(self):
        """Return only the cart items that belong to the current user."""
        return CartItem.objects.filter(cart__user=self.request.user)

    def get_serializer_class(self):
        """
        Use CartItemCreateSerializer for PATCH, PUT, DELETE operations.
        Use CartItemListSerializers for GET operation.
        """
        if self.request.method in ['PATCH', 'DELETE', 'PUT']:
            return CartItemCreateSerializer
        return CartItemListSerializers


class CartItemListView(ListAPIView):
    """
    List all carts of the current user along with their items.

    GET request:
    - Returns a list of carts.
    - Each cart includes its total price and list of items.

    Example response:
    [
        {
            "id": 1,
            "user": 1,
            "total_price": 2500,
            "items": [
                {
                    "id": 1,
                    "product": {...},
                    "quantity": 2,
                    "total_price": 1000
                },
                ...
            ]
        },
        ...
    ]
    """
    permission_classes = [IsAuthenticated]


    serializer_class = CartSerializers
    queryset = Cart.objects.all()
    @swagger_auto_schema(
        tags=['Cart'],
    )

    def get_queryset(self):
        """Return only the carts that belong to the current user."""
        return Cart.objects.filter(user=self.request.user)


class OrderCreateView(APIView):

    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        tags=['Order'],
        operation_description = "ادامه فرایند و ثبت سفارش. فقط با زدن دکمه ایجاد میشه و کل آیتم های سبد خرید رو حذف میکنه میریزه داخل خودش اگه دوبار کلیک زده بشه ارور میده "
    )
    def post(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.filter(user = user).first()
        if not cart or not cart.items.exists():
            return Response({"message":"سبد خرید شما خالی است."} , status= status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            order = Order.objects.create(user = user , total_amount = cart.total_price())
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                )
            cart.items.all().delete()


        return Response({"message": "سفارش شما ثبت شد", "order_id": order.id}, status=status.HTTP_201_CREATED)

class OrderListshippingView(ListAPIView):


    permission_classes = [IsAuthenticated]

    serializer_class = OrderSerializers
    queryset = Order.objects.all()
    @swagger_auto_schema(
        tags=['Order'],
        operation_description = "صفحه سفارشات جاری"

    )
    def get_queryset(self):
        return Order.objects.filter(status  = "shipping" , user = self.request.user)

class OrderItemRetrieveView(RetrieveUpdateDestroyAPIView):

    serializer_class = OrderItemSerializers
    queryset = OrderItem.objects.all()
    lookup_field = 'order_id'
    @swagger_auto_schema(
        tags=['ناقص'],
    )

    def get_queryset(self):
        order_id = self.kwargs.get('order_id')

        return OrderItem.objects.filter(order__user = self.request.user  , order__id = order_id)



