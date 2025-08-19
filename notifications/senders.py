import logging
import random

from notifications.models import UserProfile

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class Notifier:
    async def send(self, user_profile, message):
        raise NotImplementedError

    def can_send(self, user_profile) -> bool:
        raise NotImplementedError


class TelegramSender(Notifier):
    def __init__(self, api_token: str):
        self.api_token = api_token

    def can_send(self, user_profile: UserProfile) -> bool:
        return bool(user_profile.telegram_id)

    async def send(self, user_profile: UserProfile, message: str) -> bool:
        # Симулируем случайный успех/неудачу
        send = random.choice([True, False])
        logging.info(f"Telegram message to {user_profile.telegram_id}: {message} -> {send}")
        return send


class EmailSender(Notifier):
    def __init__(self, smtp_config: str):
        self.smtp_config = smtp_config

    def can_send(self, user_profile: UserProfile) -> bool:
        return bool(user_profile.email)

    async def send(self, user_profile: UserProfile, message: str) -> bool:
        send = random.choice([True, False])
        logging.info(f"Email to {user_profile.email}: {message} -> {send}")
        return send


class SmsSender(Notifier):
    def __init__(self, api_key: str):
        self.api_key = api_key

    def can_send(self, user_profile: UserProfile) -> bool:
        return bool(user_profile.phone_number)

    async def send(self, user_profile: UserProfile, message: str) -> bool:
        send = random.choice([True, False])
        logging.info(f"SMS to {user_profile.phone_number}: {message} -> {send}")
        return send


# Экземпляры отправителей с настройками
telegram_sender = TelegramSender(api_token="XXXX")
email_sender = EmailSender(smtp_config="smtp://example")
sms_sender = SmsSender(api_key="API_KEY_123")