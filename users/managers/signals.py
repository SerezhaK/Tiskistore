from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import receiver

from cart.models.cart import Cart
from users.models.user import User


@receiver(post_save, sender=User)
def save_or_create_profile(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)
    else:
        try:
            instance.cart.save()
        except ObjectDoesNotExist:
            Cart.objects.create(user=instance)
