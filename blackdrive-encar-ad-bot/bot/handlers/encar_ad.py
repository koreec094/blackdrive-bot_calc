import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.config import settings
from bot.keyboards import result_actions_keyboard
from bot.services.ad_generator import generate_ad_text
from bot.services.encar_parser import fetch_encar_car_data
from bot.states import EncarAdStates
from bot.utils.url import extract_car_id, is_encar_url

router = Router()
logger = logging.getLogger(__name__)


@router.message(F.text == "📝 Создать объявление по Encar")
async def ask_for_encar_url(message: Message, state: FSMContext) -> None:
    await state.set_state(EncarAdStates.waiting_for_url)
    await message.answer("Отправьте ссылку на автомобиль с Encar.")


@router.message(F.text == "👨‍💼 Связаться с менеджером")
async def contact_manager(message: Message) -> None:
    await message.answer(settings.manager_telegram_url)


@router.message(EncarAdStates.waiting_for_url)
async def handle_encar_url(message: Message, state: FSMContext) -> None:
    url = (message.text or "").strip()
    logger.info("Incoming URL: %s", url)
    if not is_encar_url(url):
        await message.answer("Пожалуйста, отправьте корректную ссылку на автомобиль с Encar.")
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
    await message.answer(ad_text, reply_markup=result_actions_keyboard(settings.manager_telegram_url))


@router.callback_query(F.data == "new_ad")
async def create_new_ad(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(EncarAdStates.waiting_for_url)
    await callback.message.answer("Отправьте ссылку на автомобиль с Encar.")
    await callback.answer()
