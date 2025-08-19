from typing import List, Optional
from .models import NotificationChannel


CHANNEL_PRIORITY: Optional[List[str]] = None


def load_channel_priority() -> None:
    """
    Загрузка приоритета каналов из базы.
    """
    global CHANNEL_PRIORITY
    CHANNEL_PRIORITY = list(
        NotificationChannel.objects
        .filter(is_active=True)
        .order_by("priority")
        .values_list("name", flat=True)
    )


def get_channel_priority() -> List[str]:
    """
    Возвращает кэшированный приоритет, если не загружен – загружает.
    """
    global CHANNEL_PRIORITY
    if CHANNEL_PRIORITY is None:
        load_channel_priority()
    return CHANNEL_PRIORITY
