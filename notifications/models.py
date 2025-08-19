from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    telegram_id = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.user.username


class NotificationChannel(models.Model):
    CHANNEL_CHOICES = [
        ("telegram", "Telegram"),
        ("email", "Email"),
        ("sms", "SMS"),
    ]
    name = models.CharField(max_length=20, choices=CHANNEL_CHOICES, unique=True)
    priority = models.PositiveIntegerField(default=0)  # меньше = выше приоритет
    is_active = models.BooleanField(default=True)


