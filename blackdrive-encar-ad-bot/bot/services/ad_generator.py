from bot.models import EncarCarData
from bot.services.formatter import format_drive, format_engine, format_int_with_dots, format_mileage_km


def generate_ad_text(car: EncarCarData, korea_expenses_krw: int) -> str:
    price_with_expenses_krw = None if car.price_krw is None else car.price_krw + korea_expenses_krw

    return (
        f"🚗 {car.brand or 'требуется проверка'} {car.model or 'требуется проверка'}\n\n"
        f"Год: {car.year or 'требуется проверка'}\n"
        f"Пробег: {format_mileage_km(car.mileage_km)}\n"
        f"Объем: {format_engine(car.engine_volume_cc, car.fuel_type)}\n"
        f"Привод: {format_drive(car.drivetrain)}\n"
        f"Комплектация: {car.trim or 'требуется проверка'}\n\n"
        f"Страховые выплаты: {car.insurance_status or 'требуется проверка'}\n\n"
        f"Цена автомобиля и расходов:\n"
        f"{format_int_with_dots(price_with_expenses_krw)} вон\n\n"
        f"Цена таможни и утиля:\n"
        f"требуется проверка\n\n"
        f"Цена авто до Владивостока с таможней:\n"
        f"требуется проверка\n\n"
        f"Ссылка на авто:\n{car.url}"
    )
