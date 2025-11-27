from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializers , CategorySerializers , ProductRetrieveSerializers , LikeAndDislikeSerializers
from .models import Product , Category , ProductLike , CommentLike , Comment
from django.db.models import Avg, Q
from rest_framework.generics import ListAPIView , RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema


# Create your views here.

class ProductRetrieveApiView(RetrieveAPIView):
    """
    Retrieve detailed information about a single product by its ID.

    URL parameters:
        pk (int): The primary key (ID) of the product.

    Returns:
        Response: serialized product details in JSON format.
    """
    serializer_class = ProductRetrieveSerializers
    queryset = Product.objects.all()
    lookup_field = "pk"
    @swagger_auto_schema(tags=['Product'])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)




class ProductListIndexApiView(APIView):

    """
    Retrieve categorized product lists for the homepage.

    Includes:
        - categories: all available categories
        - amazing_sale: products with a discount greater than 0
        - top_products: products with an average rating of 5 stars
        - new_products: latest products ordered by creation date

    Returns:
        Response: serialized data in JSON format with HTTP 200 status
    """

    @swagger_auto_schema(tags=['Home page'])
    def get(self , request):


        product = Product.objects.annotate(average_stars=Avg("comments__stars", filter=Q(comments__status="approved")))
        data = {
            "categories": Category.objects.all(),
            "amazing_sale" : Product.objects.filter(discount__gt = 0)[:5],
            "top_products" : product.filter(average_stars = 5)[:5],
            "new_products" : Product.objects.order_by("-created_at")[:5],


        }
        data_seria = {
            "categories": CategorySerializers(data["categories"] , many = True).data,
            "amazing_sale" : ProductSerializers(data["amazing_sale"] , many = True).data,
            "top_products" : ProductSerializers(data["top_products"] , many = True).data,
            "new_products" : ProductSerializers(data["new_products"] , many = True).data,

        }
        return Response(data_seria , status= status.HTTP_200_OK)

class CategoryListApiView(ListAPIView):
    """
    Retrieve a list of all available product categories.

    Returns:
        Response: serialized list of categories in JSON format.
    """

    serializer_class = CategorySerializers
    queryset = Category.objects.all()
    @swagger_auto_schema(
        tags=['Category List']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ProductListByCategoryApiView(ListAPIView):
    """
    Retrieve all products belonging to a specific category.

    URL parameters:
        category_id (int): The ID of the category.

    Returns:
        Response: serialized list of products filtered by category.
    """
    serializer_class = ProductSerializers
    @swagger_auto_schema(
        tags=['Product'],
    )
    def get_queryset(self):
        category_id = self.kwargs["category_id"]
        return Product.objects.filter(category_id =  category_id)

class ProductAmazingListApiView(ListAPIView):
    """
    List product with a discount greater than 0

    """

    serializer_class = ProductSerializers
    queryset = Product.objects.filter(discount__gt = 0)
    @swagger_auto_schema(
        tags=['Product']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class TopProductListApiView(ListAPIView):
    """
    List product with an average rating of 5 stars

    """

    serializer_class = ProductSerializers
    @swagger_auto_schema(
        tags=['Product']
    )
    def get_queryset(self):
        product = Product.objects.annotate(average_stars=Avg("comments__stars", filter=Q(comments__status="approved")))
        return product.filter(average_stars = 5)

class NewProductListApiView(ListAPIView):
    """
    List latest products ordered by creation date

    """
    serializer_class = ProductSerializers
    queryset = Product.objects.order_by("-created_at")
    @swagger_auto_schema(
        tags=['Product']
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class LikeAndDislikeCommentAPIView(APIView):
    """
    API endpoint to like or dislike a comment.

    This view allows an authenticated user to like or dislike a specific comment.
    If the user has already performed the same action on the comment, the like/dislike will be removed.
    If the user has previously liked/disliked the comment and now sends the opposite action, the status will be updated.

    HTTP Method:
        POST

    URL Parameters:
        comment_id (int): The primary key of the comment to like/dislike.

    Request Body:
        {
            "is_like": bool  # True for like, False for dislike
        }

    Responses:
        201 Created:
            {
                "message": "liked" | "disliked"
            }
            Returned when a new like/dislike is created.

        200 OK:
            {
                "message": "liked" | "disliked"
            }
            Returned when an existing like/dislike is updated.

        200 OK:
            {
                "message": "Like removed."
            }
            Returned when an existing like/dislike is removed by sending the same action again.

        400 Bad Request:
            Returned when the request body is invalid.

        404 Not Found:
            Returned when the comment does not exist or is not approved.
    """
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        tags=['Comment'],
        request_body= LikeAndDislikeSerializers
    )

    def post(self, request, comment_id):
        try:
            comment = Comment.objects.get(pk=comment_id , status = "approved")
        except Comment.DoesNotExist:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)

        srz_data = LikeAndDislikeSerializers(data=request.data)
        if not srz_data.is_valid():
            return Response(srz_data.errors, status=status.HTTP_400_BAD_REQUEST)

        is_like = srz_data.validated_data["is_like"]
        user = request.user

        like_obj, created = CommentLike.objects.get_or_create(
            user=user,
            comment=comment,
            defaults={"is_like": is_like}
        )

        # اگر از قبل وجود داشت
        if not created:
            if like_obj.is_like == is_like:
                like_obj.delete()
                return Response({"message": "Like removed."}, status=status.HTTP_200_OK)
            else:
                like_obj.is_like = is_like
                like_obj.save()
                action = "liked" if like_obj.is_like else "disliked"
                return Response({"message": action}, status=status.HTTP_200_OK)

        action = "liked" if like_obj.is_like else "disliked"
        return Response({"message": action}, status=status.HTTP_201_CREATED)

class LikeProductApiView(APIView):
    """
    API endpoint to like or unlike a product.

    This view allows an authenticated user to like a product.
    If the user has already liked the product, calling this endpoint again will remove the like.

    HTTP Method:
        POST

    Request Body:
        {
            "product_id": int  # The ID of the product to like/unlike
        }

    Responses:
        200 OK:
            {
                "liked": True
            }
            Returned when the product is successfully liked.

        200 OK:
            {
                "liked": False
            }
            Returned when the product was previously liked and the like is removed.

        400 Bad Request:
            {
                "error": "product_id is required"
            }
            Returned when the product_id is missing in the request body.

        404 Not Found:
            Returned when the product with the given ID does not exist.
    """

    permission_classes = [IsAuthenticated,]
    @swagger_auto_schema(
        tags=['Product'],
    )
    def post(self , request):
        user = request.user
        product_id = request.data.get("product_id")
        if not product_id :
            return Response({"error":"product_id is requierd"} , status=status.HTTP_400_BAD_REQUEST)
        product = Product.objects.get(pk=product_id)

        like , created = ProductLike.objects.get_or_create(product = product , user = user)
        if not created :
            like.delete()
            return Response({"liked": False}, status=status.HTTP_200_OK)

        return Response({"like":False} , status=status.HTTP_200_OK)

