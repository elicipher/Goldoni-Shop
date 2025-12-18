from rest_framework.views import APIView 
from rest_framework.generics import RetrieveUpdateDestroyAPIView , ListAPIView , CreateAPIView 
from .models import Cart , CartItem , Order , OrderItem
from .serializers import (CartItemCreateSerializer , 
                          CartSerializers , 
                          CartItemListSerializers , 
                          OrderSerializers , 
                          OrderItemSerializers,
                          CartItemUpdateSerializer)
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from rest_framework.permissions import IsAuthenticated 
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

class CartAddItemView(CreateAPIView):

    serializer_class = CartItemCreateSerializer
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
            tags=["cart"], 
            operation_summary="افزودن سبد خرید",
            operation_description=
            """
            این ویو کالا را به سبد خرید اضافه میکند و  اگر دوبار صدا شود کالا را از سبد خرید حذف میکند
            - توکن : نیاز دارد

            """
            ,
            request_body=CartItemCreateSerializer,
            responses={
                200:openapi.Response(
                    description="OK",
                    schema = openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "message":openapi.Schema(type=openapi.TYPE_STRING , example = "کالا به سبد خرید شما اضافه شد"),
                            "message2":openapi.Schema(type=openapi.TYPE_STRING , example ="کالا از سبد خرید حذف شد"),
                        }
                    )
                )

            }
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
    def get_queryset(self):
        """Return only the cart items that belong to the current user."""
        return CartItem.objects.filter(cart__user=self.request.user.id)
    
    def get_serializer_class(self):
        """
        Use CartItemCreateSerializer for PATCH, PUT, DELETE operations.
        Use CartItemListSerializers for GET operation.
        """
        if self.request.method in ['PATCH', 'DELETE', 'PUT']:
            return CartItemUpdateSerializer
        return CartItemListSerializers

    @swagger_auto_schema(
            tags=["cart"],
            operation_summary="حذف آيتم سبد خرید",
            operation_description="این ویو آیتم موجود در سبد خرید را حذف میکند.",
            responses={
                200 :"OK"
            }
            
            )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    @swagger_auto_schema(
            tags=["cart"],
            operation_summary="آپدیت آيتم سبد خرید",
            operation_description="""
             این ویو آیتم موجود در سبد خرید را ویرایش  میکند.
             -  توکن : نیاز دارد
            """
            ,
            responses={
                200 :"OK"
            }
            )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
    @swagger_auto_schema(
            tags=["cart"],
            operation_summary="نمایش جزئیات آيتم سبد خرید",
            operation_description="""
             این ویو جزئیات آیتم موجود در سبد خرید را نمایش می دهد  .
             -  توکن : نیاز دارد
            """
            ,
            responses={
                200 :"OK"
            }
            )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(auto_schema=None )

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)




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
            tags=["cart"],
            operation_summary="نمایش لیست آيتم سبد خرید",
            operation_description="""
             این ویو لیست آیتم موجود در سبد خرید را نمایش می دهد  .
             -  توکن : نیاز دارد
            """
            ,
            responses={
                200 :CartSerializers()
            }
            )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    def get_queryset(self):
        """Return only the carts that belong to the current user."""
        return Cart.objects.filter(user=self.request.user)


class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
            tags=["order"] , 
            operation_summary="ایجاد سفارش",
            operation_description=
            """
            آیتم های موجود در سبد خرید را وارد مرحله سفارش میکند . و سپس از سبد خرید حذف میکند.
            - پارامتر ها : فقط به یوزر نیاز دارد
            """,
            responses={
                201 : openapi.Response(
                        description="Create Order",
                        schema=openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                 'message': openapi.Schema(type=openapi.TYPE_STRING , example="سفارش شما ثبت شد"),
                                 "order_id" : openapi.Schema(type=openapi.TYPE_INTEGER)

                            }
                         ),   
                    ),
                
                400:openapi.Response(
                    description="Bad Request",
                    schema=openapi.Schema(
                        type=openapi.TYPE_OBJECT,properties={"message":openapi.Schema(type=openapi.TYPE_STRING , example="سبد خرید شما خالی است"),}
                    )

                )
            }
            
            
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

#region lists
class OrderListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializers
    queryset = Order.objects.all()
    
    def get_queryset(self):
        return Order.objects.filter( user = self.request.user.id)
    
    @swagger_auto_schema(
            tags=["Profile Screen"],
            operation_summary="لیست سفارشات ",
            operation_description="این ویو لیست سفارشات کاربر را نمایش میدهد." \
            "- توکن : نیاز دارد",
        )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs) 
    
class OrderListshippingView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializers
    queryset = Order.objects.all()
    
    def get_queryset(self):
        return Order.objects.filter(status  = "shipping" , user = self.request.user.id)
    
    @swagger_auto_schema(
            tags=["Profile Screen"],
            operation_summary="لیست سفارشات جاری",
            operation_description="این ویو لیست سفارشات جاری را کاربر را نمایش میدهد." \
            "- توکن : نیاز دارد",
        )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class OrderListDeliveredView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializers
    queryset = Order.objects.all()

    def get_queryset(self):
        return Order.objects.filter(status  = 'delivered' , user = self.request.user.id)
    
    @swagger_auto_schema(
            tags=["Profile Screen"],
            operation_summary="لیست سفارشات تحویل داده شده",
            operation_description="این ویو لیست سفارشات تحویل داده شده را کاربر را نمایش میدهد." \
            "- توکن : نیاز دارد",
        )

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class OrderListReturnedView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializers
    queryset = Order.objects.all()
    def get_queryset(self):
        return Order.objects.filter(status  = 'returned', user = self.request.user.id)
    
    @swagger_auto_schema(
            tags=["Profile Screen"],
            operation_summary= "لیست سفارشات مرجوع شده",
            operation_description="این ویو لیست سفارشات مرجوع شده کاربر را نمایش میدهد." \
            "- توکن : نیاز دارد",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

# endregion


class OrderItemRetrieveView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrderItemSerializers
    queryset = OrderItem.objects.all()
    lookup_field = 'order_id'

    @swagger_auto_schema(tags=["order"] , 
                        operation_summary="نمایش جزئيات سفارش",
                        operation_description="این ویو جزئیات سفارش کاربر را نشان می دهد" \
                        "- توکن : نیاز دارد"
                         )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["order"] , 
                         operation_summary="ویرایش سفارش",
                         operation_description="سفارش کاربر را ویرایش میکند " \
                         "- توکن : نیاز دارد",
                         request_body=OrderItemSerializers)
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
    
    @swagger_auto_schema(tags=["order"] ,
                        operation_summary="حذف سفارش",
                        operation_description= "آیتم سفارش کاربر را حذف میکند" \
                        "- توکن : نیاز دارد",
                        )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
    @swagger_auto_schema(auto_schema=None )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    

    def get_queryset(self):
        order_id = self.kwargs.get('order_id')

        return OrderItem.objects.filter(order__user = self.request.user.id  , order__id = order_id)
    


