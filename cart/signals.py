from django.db.models.signals import post_delete , post_save
from django.dispatch import receiver
from django.db.models import Sum, F
from .models import CartItem



@receiver([post_save , post_delete],sender=CartItem)
def update_cart_total(sender , instance , **kwargs):
    cart = instance.cart
    total = cart.items.aggregate(
        total=Sum(F("quantity") * F("product__final_price"))
    )["total"] or 0
    cart.total_price = total
    cart.save(update_fields=["total_price"])

    # فقط برای debug
    print(f"Signal from {sender.__name__}, cart id={cart.id}, total={total}")
