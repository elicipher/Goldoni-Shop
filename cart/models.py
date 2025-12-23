from django.db import models
from products.models import Product
from django.conf import settings
from django.core.validators import MinValueValidator , MaxValueValidator
from uuid import uuid4
import random
from django.utils.translation import gettext_lazy as _



# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL , on_delete=models.CASCADE , related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.PositiveIntegerField()

    def save(self, *args, **kwargs):

        total = sum(item.total_price for item in self.items.all()) or 0
        self.total_price = total
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Cart of {self.user.full_name} - {self.user.phone_number}"




class CartItem(models.Model):
    cart = models.ForeignKey(Cart , on_delete= models.CASCADE ,related_name="items" )
    product = models.ForeignKey(Product , on_delete= models.CASCADE )
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1) , MaxValueValidator(10)],default=1)
    total_price = models.PositiveIntegerField()




    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

    def save(self, *args, **kwargs):
        if self.product:  # مطمئن میشیم محصول انتخاب شده
            self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product' , "cart"], name='unique_carts_items')
        ]

class Order(models.Model):

    STATUS_CHOICES = [
        ('shipping' , 'جاری'),
        ('delivered', 'تحویل داده شده'),
        ('returned', 'مرجوع شده'),
    ]




    id = models.UUIDField(default= uuid4 , editable=False , unique=True , primary_key=True , verbose_name=_("آیدی" ))
    order_code = models.CharField(max_length=9, unique=True, editable=False , verbose_name=_("کد سفارش"))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE )
    total_amount = models.PositiveIntegerField(default=0)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES , default="shipping" , verbose_name=_("وضعیت"))
    created_at = models.DateTimeField(auto_now_add=True)



    def save(self, *args ,**kwargs):
        if not self.order_code :
            self.order_code = self.generate_code()
        super().save(*args, **kwargs)


    def generate_code(self):
        """ساخت کد سفارش ۹ رقمی یکتا """
        while True :
            code = str(random.randint(100000000 , 999999999))
            if not Order.objects.filter(order_code=code).exists():
                return code


    def __str__(self):
        return f"Order #{self.order_code} - {self.user.full_name}"




class OrderItem(models.Model):
    order = models.ForeignKey(Order , on_delete=models.CASCADE , related_name="items")
    product = models.ForeignKey(Product , on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1) , MaxValueValidator(10)],default=1)

    def total_price(self):
        return self.product.final_price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product' , 'order'], name='unique_order_items')
        ]


