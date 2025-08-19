import asyncio
import logging


from typing import List, Optional

from notifications.cache import get_channel_priority
from notifications.models import UserProfile
from notifications.senders import telegram_sender, email_sender, sms_sender, Notifier

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class NotificationService:
    CHANNEL_MAP = {
        "telegram": telegram_sender,
        "email": email_sender,
        "sms": sms_sender,
    }

    def __init__(self, channel_priority: Optional[List[str]] = None, retry_count: int = 2, timeout: int = 5):
        if channel_priority is None:
            channel_priority = get_channel_priority()

        self.senders = [self.CHANNEL_MAP[ch_name] for ch_name in channel_priority if ch_name in self.CHANNEL_MAP]
        self.retry_count = retry_count
        self.timeout = timeout

    async def _try_send(self, sender: Notifier, user_profile: UserProfile, message: str) -> bool:
        """
        Отправка сообщения через канал с retry и таймаутом.
        """
        for attempt in range(1, self.retry_count + 1):
            try:
                success = await asyncio.wait_for(sender.send(user_profile, message), timeout=self.timeout)
                if success:
                    logging.info(f"{sender.__class__.__name__} sent message on attempt {attempt}")
                    return True
                else:
                    logging.warning(f"{sender.__class__.__name__} failed on attempt {attempt}")
            except asyncio.TimeoutError:
                logging.warning(f"{sender.__class__.__name__} timed out on attempt {attempt}")
            except Exception as e:
                logging.error(f"{sender.__class__.__name__} error on attempt {attempt}: {e}", exc_info=True)
            await asyncio.sleep(0.5)
        return False

    async def send_notification(self, user_profile: UserProfile, message: str) -> bool:
        for sender in self.senders:
            if not sender.can_send(user_profile):
                logging.info(f"Skipping {sender.__class__.__name__}: no contact info")
                continue

            success = await self._try_send(sender, user_profile, message)
            if success:
                logging.info(f"Notification sent via {sender.__class__}")
                return True

        logging.warning("All notification channels failed")
        return False
