from rest_framework import generics
from .serializers import AnswerQuestionSerializer , ListQuestionSerializer
from .models import FAQ
from drf_yasg.utils import swagger_auto_schema
# Create your views here.


class ListQuestionGenericView(generics.ListAPIView):
    serializer_class = ListQuestionSerializer
    queryset = FAQ.objects.filter(is_active=True)
    pagination_class = None
    @swagger_auto_schema(tags=["Chat Bot"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    
    
class AnswerQuestionGenericView(generics.RetrieveAPIView):
    serializer_class = AnswerQuestionSerializer
    queryset = FAQ.objects.filter(is_active=True)
    lookup_field = "pk"
    
    @swagger_auto_schema(tags=["Chat Bot"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    


    
