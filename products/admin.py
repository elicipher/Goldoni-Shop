from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Product)
admin.site.register(ProductLike)
admin.site.register(ProductImage)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(CommentLike)
admin.site.register(SlideImage)
