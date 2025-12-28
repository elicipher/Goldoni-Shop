from django.contrib import admin
from .models import Article , LikeAndDislike
# Register your models here.
admin.site.register(Article)
admin.site.register(LikeAndDislike)