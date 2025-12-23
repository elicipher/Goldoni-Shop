from django.urls import path
from chatbot import views


urlpatterns = [
    path("questions/" ,views.ListQuestionGenericView.as_view() , name="questionS_list"),
    path("answer/<int:pk>/" ,views.AnswerQuestionGenericView.as_view() , name="questionS_list"),
    
]