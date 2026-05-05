import json
import logging
import re

import httpx
from bs4 import BeautifulSoup

from bot.config import settings
from bot.models import EncarCarData

logger = logging.getLogger(__name__)


async def fetch_encar_car_data(url: str, car_id: str) -> EncarCarData:
    logger.info("Fetching Encar page for car_id=%s", car_id)
    async with httpx.AsyncClient(timeout=settings.encar_request_timeout) as client:
        response = await client.get(url)
        response.raise_for_status()

    html = response.text
    soup = BeautifulSoup(html, "lxml")
    raw_text = soup.get_text(" ", strip=True)

    # MVP parser: tries to infer mandatory fields from script blocks/text.
    scripts_text = "\n".join(script.get_text(" ", strip=True) for script in soup.find_all("script"))
    source = f"{scripts_text}\n{raw_text}"

    def pick_int(pattern: str) -> int | None:
        match = re.search(pattern, source, flags=re.IGNORECASE)
        if not match:
            return None
        digits = re.sub(r"\D", "", match.group(1))
        return int(digits) if digits else None

    brand_model_match = re.search(r'"manufacturerName"\s*:\s*"([^"]+)".*?"modelGroupName"\s*:\s*"([^"]+)"', scripts_text, re.I | re.S)
    year = pick_int(r'"year"\s*:\s*"?(\d{4})')
    mileage = pick_int(r'"mileage"\s*:\s*"?([\d,]+)')
    engine = pick_int(r'"displacement"\s*:\s*"?([\d,]+)')

    fuel_match = re.search(r'"fuelTypeName"\s*:\s*"([^"]+)"', scripts_text, re.I)
    drive_match = re.search(r'"transmissionName"\s*:\s*"([^"]+)"', scripts_text, re.I)
    trim_match = re.search(r'"gradeName"\s*:\s*"([^"]+)"', scripts_text, re.I)
    price = pick_int(r'"price"\s*:\s*"?([\d,]+)')

    return EncarCarData(
        car_id=car_id,
        url=url,
        brand=brand_model_match.group(1) if brand_model_match else None,
        model=brand_model_match.group(2) if brand_model_match else None,
        year=year,
        mileage_km=mileage,
        engine_volume_cc=engine,
        fuel_type=fuel_match.group(1).lower() if fuel_match else None,
        drivetrain=drive_match.group(1) if drive_match else None,
        trim=trim_match.group(1) if trim_match else None,
        price_krw=price,
        insurance_status=None,
    )
