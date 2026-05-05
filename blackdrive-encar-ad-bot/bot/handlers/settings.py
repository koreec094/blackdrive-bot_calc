from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text == "⚙️ Настройки")
async def show_settings(message: Message) -> None:
    await message.answer("MVP: настройки будут добавлены во второй версии.")
