from rest_framework import serializers
from .models import CartItem
from products.serializers import ProductSerializers




class CartItemListSerializers(serializers.ModelSerializer):
    product = ProductSerializers()
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        exclude = ("cart" , )

    def get_total_price(self, obj):
        return obj.total_price()
    
    
class CartItemCreateSerializer(serializers.ModelSerializer):
    product = ProductSerializers()
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = CartItem
        exclude = ("cart" , )

    def get_total_price(self, obj):
        return obj.total_price()
    
