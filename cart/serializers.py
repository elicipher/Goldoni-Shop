from rest_framework import serializers
from .models import CartItem , Cart , Order , OrderItem
from products.serializers import ProductSerializers
from products.models import Product


 
    

class CartItemListSerializers(serializers.ModelSerializer):
    product = ProductSerializers()
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        exclude = ("cart" , )

    def get_total_price(self, obj):
        return obj.total_price()
    
    
class CartItemCreateSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = CartItem
        exclude = ("cart" ,"sum_of_price" )

    def get_total_price(self, obj):
        return obj.total_price()

class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=CartItem
        exclude = ("cart","product","sum_of_price",)

class CartSerializers(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    items = CartItemListSerializers(many = True , read_only = True)
    class Meta :
        model = Cart
        fields ='__all__'

    def get_total_price(self ,obj):
        return obj.total_price()






class OrderSerializers(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderItemSerializers(serializers.ModelSerializer):
    product = ProductSerializers()
    total_price = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = '__all__'

    def get_total_price(self, obj):
        return obj.total_price()
    def get_id(self , obj):
        return obj.order.id