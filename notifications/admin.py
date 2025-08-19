from django.contrib import admin

from notifications.models import UserProfile, NotificationChannel


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "email", "phone_number", "telegram_id")
    search_fields = ("user__username", "email", "phone_number", "telegram_id")


@admin.register(NotificationChannel)
class NotificationChannelAdmin(admin.ModelAdmin):
    list_display = ("name", "priority", "is_active")
    list_editable = ("priority", "is_active")
    list_filter = ("is_active",)
    ordering = ("priority",)
