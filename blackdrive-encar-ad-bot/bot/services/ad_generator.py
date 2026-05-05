from bot.models import EncarCarData
from bot.services.encar_parser import extract_trim
from bot.services.formatter import format_drive, format_engine, format_krw, format_mileage_km, format_trim


def generate_ad_text(car: EncarCarData, korea_expenses_krw: int) -> str:
    if not car.trim:
        car.trim = extract_trim(car.title or "")

    price_with_expenses_krw = None if car.price_krw is None else car.price_krw + korea_expenses_krw
    normalized_url = f"https://fem.encar.com/cars/detail/{car.car_id}" if car.car_id else (car.url or "")
    drive = format_drive(car.drivetrain)
    insurance_status = "" if not car.insurance_status else car.insurance_status

    return (
        f"🚗 {car.brand or ''} {car.model or ''}\n\n"
        f"📅 Год: {car.year or ''}\n"
        f"📍 Пробег: {format_mileage_km(car.mileage_km)}\n"
        f"⛽ Объем: {format_engine(car.engine_volume_cc, car.fuel_type)}\n"
        f"⚙️ Привод: {drive}\n"
        f"🎛 Комплектация: {format_trim(car.trim)}\n\n"
        f"🛡 Страховые выплаты: {insurance_status}\n\n"
        f"🇰🇷 Цена автомобиля + {format_krw(korea_expenses_krw)} вон расходов:\n"
        f"💰 {format_krw(price_with_expenses_krw)} вон\n\n"
        f"🧾 Цена таможни и утиля:\n\n"
        f"🚢 Цена авто до Владивостока с таможней:\n\n"
        f"🔗 Ссылка на авто:\n{normalized_url}"
    )
