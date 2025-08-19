import asyncio
import logging

from celery import shared_task
from django.contrib.auth import get_user_model
from typing import List

from notifications.services import NotificationService

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


@shared_task
def send_message(user_id: int, text: str, channel_priority: List[str]):
    """
    Celery задача для отправки уведомления пользователю через доступные каналы.
    """
    User = get_user_model()
    try:
        user = User.objects.select_related("userprofile").get(
            id=user_id,
            is_active=True
        )
    except User.DoesNotExist:
        logging.warning(f"Failed to send message: user {user_id} not found or not active")
        return

    user_profile = user.userprofile
    service = NotificationService(channel_priority=channel_priority)
    asyncio.run(service.send_notification(user_profile, text))


