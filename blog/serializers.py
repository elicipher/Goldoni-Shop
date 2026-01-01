from rest_framework import serializers
from .models import Article , LikeAndDislike


class ArticleListSerializer(serializers.ModelSerializer):
    body = serializers.SerializerMethodField() 
    author = serializers.SerializerMethodField()

    class Meta :
        model = Article
        fields = ["id","image" , "title", "author", "created_at","body"]
        
    def get_body(self, obj):
        
        if len(obj.body) > 50:
            return obj.body[:50] + "..."  # 50 کاراکتر + ... برای کوتاهی
        return obj.body
    
    def get_author(self , obj):
        return obj.author.full_name
    
    
class ArticleDetailSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    dislikes_count = serializers.IntegerField(read_only=True)
    author = serializers.SerializerMethodField()

    class Meta :
        model = Article
        fields = "__all__"
        
    def get_author(self , obj):
        return obj.author.full_name
        



class ArticleLikeSerializer(serializers.Serializer):
    is_like = serializers.BooleanField()
