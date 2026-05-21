import re

TRIM_MAP = {
    "스타일": "Style",
    "스마트": "Smart",
    "모던": "Modern",
    "프리미엄": "Premium",
    "프리미어": "Premier",
    "밸류 플러스": "Value Plus",
    "밸류플러스": "Value Plus",
    "럭셔리": "Luxury",
    "프레스티지": "Prestige",
    "노블레스": "Noblesse",
    "시그니처": "Signature",
    "트렌디": "Trendy",
    "인스퍼레이션": "Inspiration",
    "익스클루시브": "Exclusive",
    "캘리그래피": "Calligraphy",
    "그래비티": "Gravity",
    "플래티넘": "Platinum",
    "마스터즈": "Masters",
    "에어": "Air",
    "어스": "Earth",
    "GT라인": "GT Line",
    "GT 라인": "GT Line",
    "N라인": "N Line",
    "N 라인": "N Line",
}

FUEL_MAP = {
    "gasoline": "бензин",
    "petrol": "бензин",
    "휘발유": "бензин",
    "가솔린": "бензин",
    "diesel": "дизель",
    "디젤": "дизель",
    "경유": "дизель",
    "hybrid": "гибрид",
    "hev": "гибрид",
    "lpg": "газ",
    "전기": "электро",
    "electric": "электро",
}


def format_krw(value: int | None) -> str:
    if value is None:
        return "требуется проверка"
    return f"{value:,}".replace(",", ".")


def format_mileage(value: int | None) -> str:
    if value is None:
        return "требуется проверка"
    return f"{value:,}".replace(",", ".")


def format_mileage_km(value: int | None) -> str:
    formatted = format_mileage(value)
    if formatted == "требуется проверка":
        return formatted
    return f"{formatted} km"


def format_engine(engine_volume_cc: int | None, fuel_type: str | None) -> str:
    fuel_key = (fuel_type or "").strip().lower()
    fuel = FUEL_MAP.get(fuel_key, fuel_key if fuel_key else "требуется проверка")
    if engine_volume_cc is None:
        return f"требуется проверка {fuel}"
    liters = round(engine_volume_cc / 1000, 1)
    return f"{liters:.1f} {fuel}"


def format_drive(drivetrain: str | None) -> str:
    if drivetrain is None:
        return ""
    value = drivetrain.strip().upper()
    if value in {"2WD"}:
        return "2вд"
    if value in {"4WD", "AWD"}:
        return "4вд"

    raw = drivetrain.strip()
    if raw in {"오토", "자동", "수동"}:
        return ""
    if "전륜" in raw:
        return "передний"
    if "후륜" in raw:
        return "задний"
    if "4륜" in raw or "사륜" in raw:
        return "4вд"
    return ""


def format_trim(trim: str | None) -> str:
    if not trim:
        return ""
    return TRIM_MAP.get(trim.strip(), "")


def format_korean_plate_number(raw_plate: str | None) -> str | None:
    if not raw_plate:
        return None

    normalized = re.sub(r"\s+", "", raw_plate)
    if not normalized:
        return None

    match = re.match(r"^(\d{2,3})([가-힣])(\d{4})$", normalized)
    if match:
        return f"{match.group(1)}{match.group(2)} {match.group(3)}"

    return raw_plate.strip() or None
