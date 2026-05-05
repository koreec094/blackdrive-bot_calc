import logging

import httpx

from bot.config import settings
from bot.models import EncarCarData, ImportCalculationResult

logger = logging.getLogger(__name__)


async def calculate_import_cost(car: EncarCarData) -> ImportCalculationResult:
    car_price = car.price_krw
    price_with_expenses = (car_price + settings.korea_expenses_krw) if car_price is not None else None

    if not settings.calculator_api_url:
        logger.warning("CALCULATOR_API_URL is not configured, returning partial result")
        return ImportCalculationResult(
            car_price_krw=car_price,
            korea_expenses_krw=settings.korea_expenses_krw,
            price_with_expenses_krw=price_with_expenses,
            customs_usd=None,
            recycling_fee_usd=None,
            total_to_vladivostok_usd=None,
        )

    payload = {
        "brand": car.brand,
        "model": car.model,
        "year": car.year,
        "engine_volume_cc": car.engine_volume_cc,
        "fuel_type": car.fuel_type,
        "price_krw": car.price_krw,
        "price_with_expenses_krw": price_with_expenses,
        "destination": "vladivostok",
    }
    headers = {"Authorization": f"Bearer {settings.calculator_api_token}"} if settings.calculator_api_token else {}

    async with httpx.AsyncClient(timeout=15) as client:
        response = await client.post(settings.calculator_api_url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

    logger.info("Calculation result received: %s", data)
    return ImportCalculationResult(
        car_price_krw=car_price,
        korea_expenses_krw=settings.korea_expenses_krw,
        price_with_expenses_krw=price_with_expenses,
        customs_usd=data.get("customs_usd"),
        recycling_fee_usd=data.get("recycling_fee_usd"),
        total_to_vladivostok_usd=data.get("total_to_vladivostok_usd"),
    )
