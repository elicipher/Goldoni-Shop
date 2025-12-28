from rest_framework import serializers
from .models import Article , LikeAndDislike


class ArticleListSerializer(serializers.ModelSerializer):
    body = serializers.SerializerMethodField() 

    class Meta :
        model = Article
        fields = ["id","image" , "title", "author", "created_at","body","likes_count","dislikes_count",]
        
    def get_body(self, obj):
        
        if len(obj.body) > 50:
            return obj.body[:50] + "..."  # 50 کاراکتر + ... برای کوتاهی
        return obj.body
    
    
class ArticleDetailSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    dislikes_count = serializers.IntegerField(read_only=True)
    class Meta :
        model = Article
        fields = "__all__"
        



class ArticleLikeSerializer(serializers.Serializer):
    is_like = serializers.BooleanField()
