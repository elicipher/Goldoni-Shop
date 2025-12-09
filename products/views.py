from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework import status
from .serializers import (ProductSerializers , 
                          CategorySerializers , 
                          ProductRetrieveSerializers , 
                          LikeAndDislikeSerializers , 
                          SlideImageSerializers,
                          ProductLikeSerializers )
from .models import Product , Category , ProductLike , CommentLike , Comment  , SlideImage
from django.db.models import Avg, Q 
from rest_framework.generics import ListAPIView , RetrieveAPIView 
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Q


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
    @swagger_auto_schema(
            tags=["products"],
            operation_summary="جزئیات محصول",
            operation_description="""
            این ویو جزئیات محصول را نمایش میدهد. و تنها پارامتر مورد نیاز آیدی محصول است.
            توکن :‌نیاز ندارد.

            """
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# region  Lists
class SlideImageApiView(ListAPIView):
    pagination_class = None
    serializer_class=SlideImageSerializers
    queryset = SlideImage.objects.all()

    @swagger_auto_schema(tags=["home views"], operation_summary= "تصاویر اسلاید بالا" , operation_description="تصاویر اسلاید را به شکل لیست برمیگرداند.")
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
    
    @swagger_auto_schema(
            tags=["home views"],
            operation_summary="نمایش محصولات در صفحه اول",
            operation_description="""
            این ویو محصولات را در سه دسته بندی نمایش می دهد.
            - categories : نمایش دسته بندی های موجود
            - amazing_sale : نمایش محصولاتی که تخفیف دارند.
            - top_products : محصولاتی که پنج ستاره دارند.
            - new_products : محصولات جدید.
            توکن :‌نیاز ندارد.

            """
           
     
    )
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
            tags=["home views"],
            operation_summary="لیست دسته بندی",
            operation_description="""
            لیست دسته بندی های موجود را برمیگرداند
            توکن :‌نیاز ندارد.

            """
           
     
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

    def get_queryset(self):
        category_id = self.kwargs["category_id"]
        return Product.objects.filter(category_id =  category_id)
    
    @swagger_auto_schema(
            tags=["home views"],
            operation_summary="نمایش محصولات بر اساس دسته بندی",
            operation_description="""
            لیست  محصولات را بر اساس دسته بندی نمایش می دهد. فقط آیدی دسته بندی را میگیرد.
            توکن :‌نیاز ندارد.

            """
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class ProductAmazingListApiView(ListAPIView):
    """
    List product with a discount greater than 0

    """
    serializer_class = ProductSerializers
    queryset = Product.objects.filter(discount__gt = 0)
    @swagger_auto_schema(
            tags=["home views"],
            operation_summary="لیست محصولات شگفت انگیز",
            operation_description="""
       این ویو لیست محصولاست ویژه که تخفیف خورده اند را بر میگرداند.
            توکن :‌نیاز ندارد.

            """
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class TopProductListApiView(ListAPIView):
    """
    List product with an average rating of 5 stars

    """
    serializer_class = ProductSerializers
    def get_queryset(self):
        product = Product.objects.annotate(average_stars=Avg("comments__stars", filter=Q(comments__status="approved")))
        return product.filter(average_stars = 5)
    
    @swagger_auto_schema(
            tags=["home views"],
            operation_summary="لیست محصولات  برتر",
            operation_description="""
       لیست محصولاتی که پنج ستاره دارند را برمیگرداند.
            توکن :‌نیاز ندارد.

            """
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class NewProductListApiView(ListAPIView):
    """
    List latest products ordered by creation date

    """
    serializer_class = ProductSerializers
    queryset = Product.objects.order_by("-created_at")

    @swagger_auto_schema(
            tags=["home views"],
            operation_summary="لیست جدید ترین محصولات",
            operation_description="""
        لیست محصولات جدید را نمایش میدهد
            توکن :‌نیاز ندارد.

            """
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
# endregion


# region like
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
            tags=["products"],
            operation_summary="لایک و دیس لایک کامنت",
            operation_description="""
            این ویو امکان لایک و دیس لایک کردن کامنت را را انجام میدهد.
            وقتی مقدار لایک برابر باشه با true لایک میخورد و اگر دوباره این مقدار ارسال شود لایک حذف میشود.
            وقتی مقدار لایک برابر باشه با false دیس لایک میخورد و اگر دوباره این مقدار ارسال شود دیس لایک حذف میشود.
            توکن :‌نیاز دارد.

            """,
            request_body=LikeAndDislikeSerializers,
            responses={
                200:"deleted like/dislike",
                201:"created like/dislike",
                404:"Not found comment",
                400:"Bad request",

            }
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
    tags=["products"],
    operation_summary="لایک یا آنلایک محصول",
    operation_description="""
این ویو برای لایک کردن محصول است. اگر کاربر قبلاً محصول را لایک کرده باشد، 
با صدا زدن دوباره این API، لایک حذف می‌شود.

پارامترهای لازم:
- product_id: آیدی محصول
- توکن نیاز دارد (کاربر باید لاگین باشد)
""",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=["product_id"],
        properties={
            "product_id": openapi.Schema(
                type=openapi.TYPE_INTEGER,
                example=12,
                description="آیدی محصولی که قرار است لایک شود"
            )
        }
    ),
    responses={
        200: openapi.Response(
            description="وضعیت لایک",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "liked": openapi.Schema(
                        type=openapi.TYPE_BOOLEAN,
                        example=True
                    )
                }
            )
        ),
        400: openapi.Response(
            description="پارامتر ناقص",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="product_id is required"
                    )
                }
            )
        ),
        404: openapi.Response(
            description="محصول یافت نشد",
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "error": openapi.Schema(
                        type=openapi.TYPE_STRING,
                        example="Product not found"
                    )
                }
            )
        )
    }
)

    def post(self, request):
        user = request.user
        product_id = request.data.get("product_id")

        if not product_id:
            return Response({"error": "product_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        like, created = ProductLike.objects.get_or_create(product=product, user=user)

        if not created:
            like.delete()
            return Response({"liked": False}, status=status.HTTP_200_OK)

        return Response({"liked": True}, status=status.HTTP_200_OK)

class ListProductLikedGenericView(ListAPIView):

    permission_classes = [IsAuthenticated,]
    serializer_class = ProductLikeSerializers
    def get_queryset(self):
        return ProductLike.objects.filter(user=self.request.user)
    @swagger_auto_schema(
            operation_summary="لیست محصولات موردعلاقه",
            tags=["Profile Screen"],
            
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

# endregion


class ProductSearchView(ListAPIView):
    serializer_class = ProductSerializers

    def get_queryset(self):
        q = self.request.query_params.get("q", "")
        return Product.objects.filter(Q(title__icontains=q) | Q(category__title__icontains=q))
        
    @swagger_auto_schema(tags=["search"],
                         operation_summary="جستجوی محصول",
                         operation_description="""
                        این ویو امکان جستجوی محصول را بر اساس نام محصول یا نام دسته بندی فراهم میکند.
                        کوئری باید با پارامتر q ارسال شود.
                        در صورت نبودن مقدار نال میفرستد
                            - توکن :‌نیاز ندارد.
                         """,
                         responses={200:ProductSerializers(many=True)})
    
                         
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class CategorySearchView(ListAPIView):
    serializer_class = CategorySerializers

    def get_queryset(self):
        q = self.request.query_params.get("q", "")
        return Category.objects.filter(title__icontains=q)
    @swagger_auto_schema(tags=["search"],
                         operation_summary="جستجوی دسته بندی",
                         operation_description="""
                        این ویو امکان جستجوی دسته بندی را بر اساس نام دسته بندی فراهم میکند.پارامتر q باید با کوئری ارسال شود.
                            - توکن :‌نیاز ندارد.
                         """,
                        responses={200:CategorySerializers(many=True)})
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    