from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from users.models import MyUser
from django.db.models import Avg
from .models import Review


@receiver(post_save, sender=Review)
def update_rating_on_save(sender, instance, **kwargs):
    update_user_rating(instance.to_user)


@receiver(post_delete, sender=Review)
def update_rating_on_delete(sender, instance, **kwargs):
    update_user_rating(instance.to_user)


def update_user_rating(user):
    avg_rating = Review.objects.filter(to_user=user).aggregate(avg=Avg('rating'))['avg']
    user.rating = round(avg_rating, 1) if avg_rating else 0.0
    user.save(update_fields=['rating'])
