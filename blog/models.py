from django.db import models
from django.conf import settings
# Create your models here.
class Article(models.Model):
    
    STATUS_CHOICE = [
        ("published","منتشر شده"),
        ("draft","پیش نویس"),
    ]
    image = models.ImageField(upload_to="blog/images/%Y/%m/%d")
    title = models.CharField(max_length=150)
    author = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE , related_name="articles")
    body = models.TextField()
    status = models.CharField(choices=STATUS_CHOICE , default="draft" , max_length=25)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} --- {self.created_at}"
    
    @property
    def likes_count(self):
        return self.likes.filter(like=True).count()

    @property
    def dislikes_count(self):
        return self.likes.filter(like=False).count()
        
    

class LikeAndDislike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE , related_name="article_likes")
    article = models.ForeignKey(Article , on_delete=models.CASCADE , related_name="likes")
    like = models.BooleanField()
    
    class Meta :
        constraints = [
            models.UniqueConstraint(
                fields=("user", "article"),
                name="unique_user_article_like"
            )
        ]

        
    
    
    
    
    