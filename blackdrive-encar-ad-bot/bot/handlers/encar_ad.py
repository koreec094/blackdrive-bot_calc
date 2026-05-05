import logging

from aiogram import F, Router
from aiogram.types import Message

from bot.config import settings
from bot.services.ad_generator import generate_ad_text
from bot.services.encar_parser import fetch_encar_car_data
from bot.utils.auth import is_allowed_user
from bot.utils.url import extract_car_id, is_encar_url

router = Router()
logger = logging.getLogger(__name__)


@router.message(F.text)
async def handle_encar_url(message: Message) -> None:
    if not is_allowed_user(message):
        await message.answer("⛔ У вас нет доступа к этому боту.")
        return

    url = (message.text or "").strip()
    logger.info("Incoming URL: %s", url)
    if not is_encar_url(url):
        await message.answer("Отправьте ссылку на автомобиль Encar.")
        return

    car_id = extract_car_id(url)
    if not car_id:
        await message.answer("Не удалось определить ID автомобиля из ссылки. Проверьте ссылку и попробуйте снова.")
        return

    try:
        car = await fetch_encar_car_data(url, car_id)
    except Exception:
        logger.exception("Failed to fetch Encar data")
        await message.answer("Не удалось получить данные с Encar. Попробуйте позже.")
        return

    ad_text = generate_ad_text(car, settings.korea_expenses_krw)
    await message.answer(ad_text)
