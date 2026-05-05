from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Создать объявление по Encar")],
            [KeyboardButton(text="⚙️ Настройки"), KeyboardButton(text="👨‍💼 Связаться с менеджером")],
        ],
        resize_keyboard=True,
    )


def result_actions_keyboard(manager_url: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📋 Создать еще одно объявление", callback_data="new_ad")],
            [InlineKeyboardButton(text="👨‍💼 Связаться с менеджером", url=manager_url)],
        ]
    )
