from django.db.models.signals import post_save
from django.dispatch import receiver

from .cache import load_channel_priority
from .models import NotificationChannel


@receiver(post_save, sender=NotificationChannel)
def update_channel_cache(sender, instance, **kwargs):
    """
    Обновление кэша при изменении каналов в БД.
    """
    load_channel_priority()
