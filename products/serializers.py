from rest_framework import serializers
from .models import Category ,  Product , Comment ,SlideImage, ProductImage
from accounts.models import User


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ("description",)

class ProductSerializers(serializers.ModelSerializer):

    class Meta :
        model = Product
        fields = ["id","title", "price","discount","final_price","main_image"]



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["full_name"]



class CommentSerializers(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta :
        model = Comment
        fields = ["id","stars" , "user" ,"text", "is_buyer" , "created_at" , "like_count" , "dislike_count"]

    def get_like_count(self , obj):
        return obj.like_count()

    def get_dislike_count(self , obj):
        return obj.dislike_count()

    def get_user(self , obj):
        return obj.user.full_name

class ProductImageSerializers(serializers.ModelSerializer):
    class Meta:
        model =  ProductImage
        fields = "__all__"


class ProductRetrieveSerializers(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    average_stars = serializers.SerializerMethodField()
    count_comments = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    class Meta :
        model = Product
        exclude = ("user",)

    def get_comments(self, obj):
        comments = obj.comments.filter(status="approved")[:5]
        return CommentSerializers(comments, many=True).data

    def get_average_stars(self , obj ):
        return obj.average_stars()

    def get_count_comments(self , obj):
        return obj.comments.count()

    def get_category(self , obj):
        return obj.category.title

    def get_images(self, obj):
        images = obj.product_images.all()
        return ProductImageSerializers(images, many=True).data





class LikeAndDislikeSerializers(serializers.Serializer):
    is_like = serializers.BooleanField()

class SlideImageSerializers(serializers.ModelSerializer):
    class Meta:
        model= SlideImage
        fields = "__all__"
