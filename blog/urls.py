from django.urls import path
from . import views

urlpatterns = [
    path("list_article/" , views.ArticleListGenericView.as_view() , name="list_article"),
    path("detail_article/<int:id>/",views.ArticleDetailGenericView.as_view() , name="detail_article"),
    path("like_article/<int:article_id>/",views.ArticleLikeAPIView.as_view() , name="like_article")
]