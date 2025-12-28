from rest_framework import generics , status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import ArticleListSerializer , ArticleDetailSerializer , ArticleLikeSerializer
from .models import Article , LikeAndDislike
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.



class ArticleListGenericView(generics.ListAPIView):
    serializer_class = ArticleListSerializer
    queryset = Article.objects.filter(status = "published")



class ArticleDetailGenericView(generics.RetrieveAPIView):
    serializer_class = ArticleDetailSerializer
    queryset = Article.objects.filter(status = "published")
    lookup_field = "id"


class ArticleLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema( 
        operation_summary="لایک و دیس لایک مقاله",
        operation_description="""
        این ویو امکان لایک و دیس لایک کردن مقاله را انجام میدهد.
        وقتی مقدار لایک برابر باشد با true → لایک زده می‌شود و اگر دوباره همین مقدار ارسال شود → لایک حذف می‌شود.
        وقتی مقدار لایک برابر باشد با false → دیس‌لایک زده می‌شود و اگر دوباره همین مقدار ارسال شود → دیس‌لایک حذف می‌شود.
        توکن: نیاز دارد.
        """,
        request_body=ArticleLikeSerializer, 
        responses={
        201: openapi.Response(description="success",examples={ "application/json": {"message": "like or disliked"}}) , 
        200:"deleted like/dislike",
        404:"Article not found",
        400:"Bad request",
        } )
    
    def post(self, request, article_id):
        try :
            article = Article.objects.get(pk=article_id , status="published")
        except Article.DoesNotExist :
            return Response({"error": "Article not found"}, status=status.HTTP_404_NOT_FOUND)
        
        srz_data = ArticleLikeSerializer(data=request.data)
        if not srz_data.is_valid():
            return Response(srz_data.errors , status=status.HTTP_400_BAD_REQUEST)
        
        is_like = srz_data.validated_data["is_like"]
        user = request.user

        like_obj = LikeAndDislike.objects.filter(user=user,article=article).first()
        
        if like_obj :
            if is_like == like_obj.like :
                like_obj.delete()
                return Response({"message": "Like removed."}, status=status.HTTP_200_OK)
            else :
                like_obj.like = is_like
                like_obj.save()
                action = "liked" if like_obj.like  else "disliked"
                return Response({"message": action}, status=status.HTTP_200_OK)
        else :
            like_obj=LikeAndDislike.objects.create(article = article , user = user , like = is_like)
            
        action = "liked" if like_obj.like else "disliked"
        return Response({"message": action}, status=status.HTTP_201_CREATED)


            

        
