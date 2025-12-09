from django.urls import path , include
from . import views


list_urls = [
    path("slider/",views.SlideImageApiView.as_view()),
    path("index/" , views.ProductListIndexApiView.as_view()),
    path("categories/" , views.CategoryListApiView.as_view()),
    path("categories/<int:category_id>/" , views.ProductListByCategoryApiView.as_view()),
    path("amazing/" , views.ProductAmazingListApiView.as_view()),
    path("top/" , views.TopProductListApiView.as_view()),
    path("new/" , views.NewProductListApiView.as_view()),

]
urlpatterns = [
    path("" , include(list_urls)),
    path("retrieve/<int:pk>/" , views.ProductRetrieveApiView.as_view()),
    path("like/<int:product_id>/" , views.LikeProductApiView.as_view()),
    path("comment/<int:comment_id>/like/" , views.LikeAndDislikeCommentAPIView.as_view()),
    path("favorite_list/" , views.ListProductLikedGenericView.as_view()),    
]

