from aiogram.types import Message

from bot.config import settings


def is_allowed_user(message: Message) -> bool:
    username = message.from_user.username if message.from_user else None
    if not username:
        return False

    return username.strip().lower().lstrip("@") in settings.allowed_usernames_set
