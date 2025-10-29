from django.db import models
from products.models import Product
from django.conf import settings
from django.core.validators import MinValueValidator , MaxValueValidator
# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE , related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())
    
    def __str__(self):
        return f"Cart of {self.user.full_name} - {self.user.phone_number}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart , on_delete= models.CASCADE ,related_name="items" )
    product = models.ForeignKey(Product , on_delete= models.CASCADE )
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1) , MaxValueValidator(10)],default=1) 

    def total_price(self):
        return self.product.final_price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} x {self.product.title}"
    
class Order(models.Model):

    STATUS_CHOICES = [
        ('shipping' , 'جاری'),
        ('delivered', 'تحویل داده شده'),
        ('returned', 'مرجوع شده'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('online', 'پرداخت آنلاین'),
        ('cod', 'پرداخت درب منزل'),
    ]



    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    total_amount = models.PositiveIntegerField()
    is_paid = models.BooleanField(default=False)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES, default='online')
    created_at = models.DateTimeField(auto_now_add=True)



    def total_amount(self):
        return self.cart.total_price()

    def __str__(self):
        return f"Order #{self.id} - {self.user.full_name}"


