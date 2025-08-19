from django.urls import path

from notifications.views import SendNotificationView

urlpatterns = [
    path('notifications/send/', SendNotificationView.as_view(), name='send-notification'),
]
