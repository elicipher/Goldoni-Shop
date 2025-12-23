from rest_framework import serializers
from .models import FAQ



class ListQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ("id","question",)
        
    
    
    
class AnswerQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=FAQ
        fields = ("id","answer")