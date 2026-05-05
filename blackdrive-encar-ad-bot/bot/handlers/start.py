from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.utils.auth import is_allowed_user

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    if not is_allowed_user(message):
        await message.answer("⛔ У вас нет доступа к этому боту.")
        return

    await message.answer("Отправьте ссылку на автомобиль Encar, и я сформирую объявление.")
