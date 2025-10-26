from django.db import models
from django.core.validators import MinValueValidator ,MaxValueValidator
from accounts.models import User
from PIL import Image

# Create your models here.
def validate_real_image(value):
    try:
        img =Image.open(value)
        img.verify()
    except Exception:
        raise ValueError("فایل نامعتبر است")
        



class Category(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField(null= True , blank= True)

    def __str__(self):
        return self.title 


class Product(models.Model):
    STATUS_CHOICE = [
        ('available', 'موجود'),
        ('unavailable', 'ناموجود'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category , on_delete=models.SET_NULL , related_name="products" , null= True , blank= True)
    price = models.PositiveIntegerField(default=0)
    discount = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="The value must be between 0 and 100"
    )
    final_price = models.PositiveBigIntegerField(default=0)
    status = models.CharField(choices=STATUS_CHOICE, max_length=100, default="unavailable")
    created_at = models.DateTimeField(auto_now=True)
    

    def save(self, *args, **kwargs):
        # چون discount همیشه یه عدد داره، نیازی به چک کردن None نیست
        self.final_price = int(self.price * (100 - self.discount) / 100)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title




class ProductImage(models.Model):

    product = models.ForeignKey(Product , on_delete= models.CASCADE , related_name="product_images")
    image = models.ImageField(upload_to='product_image/' ,validators=[validate_real_image])

    def clean(self):
        if self.product.product_images.count() > 6 :
            raise ValueError("هر محصول فقط 6 تصویر میتواند داشته باشد")
        
    def save(self, *args , **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
     



class Like(models.Model):

    user = models.ForeignKey(User , on_delete= models.CASCADE , related_name="user_likes")
    product = models.ForeignKey(Product , on_delete= models.CASCADE , related_name="produt_like")

    class Meta:
        constraints  = [
            models.UniqueConstraint(fields=['user','product'] , name="uniqe_user_product_like")
        ]

