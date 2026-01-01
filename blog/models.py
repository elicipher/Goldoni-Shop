from django.db import models
from django.conf import settings
from django_jalali.db import models as jmodels
from jdatetime import date as jdata
from jdatetime import datetime
# Create your models here.
def article_image_path(instance, filename):

    
    # تاریخ شمسی امروز
    today = jdata.today()
    year = today.year
    month = today.month
    day = today.day

    return f"blog/article/{year}/{month}/{day}/{filename}"

class Article(models.Model):
    
    STATUS_CHOICE = [
        ("published","منتشر شده"),
        ("draft","پیش نویس"),
    ]
    image = models.ImageField(upload_to=article_image_path)
    title = models.CharField(max_length=150)
    author = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE , related_name="articles")
    body = models.TextField()
    status = models.CharField(choices=STATUS_CHOICE , default="draft" , max_length=25)
    created_at = jmodels.jDateField(auto_now_add=True)
    updated_at = jmodels.jDateTimeField(auto_now=True)
    
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

        
    
    
    
    
    