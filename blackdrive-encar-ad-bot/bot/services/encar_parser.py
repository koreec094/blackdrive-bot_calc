import logging
import re

import httpx
from bs4 import BeautifulSoup

from bot.config import settings
from bot.models import EncarCarData
from bot.services.formatter import format_trim

logger = logging.getLogger(__name__)


BRAND_MAP = {
    "르노코리아(삼성)": "Renault Samsung",
    "르노삼성": "Renault Samsung",
    "기아": "Kia",
    "현대": "Hyundai",
    "제네시스": "Genesis",
    "르노코리아": "Renault Korea",
    "삼성": "Renault Samsung",
    "쉐보레(GM대우)": "Chevrolet",
    "GM대우": "Chevrolet",
    "쉐보레": "Chevrolet",
    "대우": "Daewoo",
    "쌍용": "SsangYong",
    "KG모빌리티": "KG Mobility",
    "BMW": "BMW",
    "벤츠": "Mercedes-Benz",
    "메르세데스-벤츠": "Mercedes-Benz",
    "아우디": "Audi",
    "폭스바겐": "Volkswagen",
    "렉서스": "Lexus",
    "토요타": "Toyota",
    "혼다": "Honda",
    "닛산": "Nissan",
    "포드": "Ford",
    "링컨": "Lincoln",
    "지프": "Jeep",
    "볼보": "Volvo",
    "미니": "MINI",
}

MODEL_MAP = {
    "트레일블레이저": "Trailblazer",
    "트랙스": "Trax",
    "스파크": "Spark",
    "말리부": "Malibu",
    "임팔라": "Impala",
    "콜로라도": "Colorado",
    "카마로": "Camaro",
    "QM6": "QM6",
    "SM6": "SM6",
    "XM3": "XM3",
    "SM3": "SM3",
    "SM5": "SM5",
    "SM7": "SM7",
    "마스터": "Master",
    "E-클래스": "E-Class",
    "C-클래스": "C-Class",
    "S-클래스": "S-Class",
    "A-클래스": "A-Class",
    "B-클래스": "B-Class",
    "GLA-클래스": "GLA-Class",
    "GLB-클래스": "GLB-Class",
    "GLC-클래스": "GLC-Class",
    "GLE-클래스": "GLE-Class",
    "GLS-클래스": "GLS-Class",
    "3시리즈": "3-Series",
    "5시리즈": "5-Series",
    "7시리즈": "7-Series",
    "X1": "X1",
    "X3": "X3",
    "X5": "X5",
    "X6": "X6",
    "X7": "X7",
    "모닝": "Morning",
    "레이": "Ray",
    "K3": "K3",
    "K5": "K5",
    "K7": "K7",
    "K8": "K8",
    "K9": "K9",
    "쏘렌토": "Sorento",
    "스포티지": "Sportage",
    "카니발": "Carnival",
    "셀토스": "Seltos",
    "아반떼": "Avante",
    "쏘나타": "Sonata",
    "그랜저": "Grandeur",
    "투싼": "Tucson",
    "싼타페": "Santa Fe",
    "팰리세이드": "Palisade",
    "코나": "Kona",
    "제네시스 G80": "Genesis G80",
    "G80": "G80",
    "GV70": "GV70",
    "GV80": "GV80",
    "G70": "G70",
    "G90": "G90",
    "GV60": "GV60",
}
TITLE_TOKEN_MAP = {
    **BRAND_MAP,
    **MODEL_MAP,
    "5세대": "5th Gen",
    "M 스포츠": "M-Sport",
    "M스포츠": "M-Sport",
    "AMG 라인": "AMG Line",
    "AMG라인": "AMG Line",
    "어반": "Urban",
    "터보": "Turbo",
    "가솔린": "",
    "디젤": "",
    "하이브리드": "Hybrid",
    "가솔린+전기": "Plug-in Hybrid",
    "전기": "Electric",
}

FUEL_MAP = {
    "가솔린": "бензин",
    "휘발유": "бензин",
    "디젤": "дизель",
    "경유": "дизель",
    "LPG": "газ",
    "엘피지": "газ",
    "하이브리드": "гибрид",
    "가솔린+전기": "гибрид",
    "디젤+전기": "дизель гибрид",
    "전기": "электро",
    "수소": "водород",
}


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
    "베스트 셀렉션": "Best Selection",
    "베스트셀렉션": "Best Selection",
    "트렌디": "Trendy",
    "스페셜": "Special",
    "마이핏": "My Fit",
    "초이스": "Choice",
    "파이니스트": "Finest",
    "로얄 스페셜": "Royal Special",
    "로얄": "Royal",
}

TITLE_TOKEN_MAP.update({k: v for k, v in TRIM_MAP.items()})
MODEL_BRAND_HINTS = {
    "Sportage": "Kia",
    "Morning": "Kia",
    "Sorento": "Kia",
    "Carnival": "Kia",
    "Seltos": "Kia",
    "Ray": "Kia",
    "E-Class": "Mercedes-Benz",
    "C-Class": "Mercedes-Benz",
    "S-Class": "Mercedes-Benz",
    "A-Class": "Mercedes-Benz",
    "B-Class": "Mercedes-Benz",
    "3-Series": "BMW",
    "5-Series": "BMW",
    "7-Series": "BMW",
    "QM6": "Renault Samsung",
    "Trailblazer": "Chevrolet",
}


def _first_non_empty(*values: str | None) -> str:
    for value in values:
        if value and value.strip():
            return value.strip()
    return ""


def _normalize_title_spacing(raw_title: str) -> str:
    normalized = raw_title.replace("  ", " ")
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def clean_raw_title(title: str) -> str:
    cleaned = _normalize_title_spacing(title)
    if not cleaned:
        return ""

    for marker in [
        " 중고차",
        ": 내차팔기",
        "내차팔기",
        "내차사기",
        "| 엔카",
        "- 엔카",
        "엔카",
        "Encar",
    ]:
        idx = cleaned.find(marker)
        if idx >= 0:
            cleaned = cleaned[:idx]

    cleaned = _normalize_title_spacing(cleaned)
    trailing_regions = [
        "서울", "경기", "인천", "부산", "대구", "대전", "광주", "울산", "세종", "제주",
        "강원", "충북", "충남", "전북", "전남", "경북", "경남",
    ]
    cleaned = re.sub(rf"(?:\s+(?:{'|'.join(trailing_regions)}))+\s*$", "", cleaned).strip()
    return _normalize_title_spacing(cleaned)


def translate_full_title(raw_title: str) -> str:
    normalized = _normalize_title_spacing(raw_title)
    if not normalized:
        return ""

    translated = normalized
    for source in sorted(TITLE_TOKEN_MAP, key=len, reverse=True):
        replacement = TITLE_TOKEN_MAP[source]
        translated = re.sub(rf"(?<!\w){re.escape(source)}(?!\w)", replacement, translated)

    translated = translated.replace("(", " ").replace(")", " ")
    translated = re.sub(r"\s+", " ", translated).strip()
    translated = re.sub(r"\b([A-Z]{1,5}\d{2,3}|\d{3})\s+d\b", r"\1d", translated)
    translated = re.sub(r"(Renault Samsung)(\s+\1)+", r"\1", translated)
    translated = re.sub(r"(Chevrolet)(\s+\1)+", r"\1", translated)
    if translated:
        if not any(translated.startswith(f"{brand} ") or translated == brand for brand in BRAND_MAP.values()):
            for model_token, brand_name in MODEL_BRAND_HINTS.items():
                if re.search(rf"(?<!\w){re.escape(model_token)}(?!\w)", translated):
                    return f"{brand_name} {translated}"
    return translated


def build_display_title(car: EncarCarData) -> str:
    raw_title = (car.title or "").strip()
    if raw_title:
        full_title = translate_full_title(clean_raw_title(raw_title))
        if full_title:
            first_token = full_title.split(" ", 1)[0]
            if first_token in BRAND_MAP.values():
                return full_title

            brand = (car.brand or "").strip()
            if brand:
                return f"{brand} {full_title}".strip()
            return full_title

    fallback_parts = [(car.brand or "").strip(), (car.model or "").strip(), format_trim(car.trim)]
    return " ".join(part for part in fallback_parts if part).strip()

def parse_specs_line(specs_line: str) -> tuple[int | None, int | None, str | None]:
    year = None
    mileage = None
    fuel = None

    yy_mm_match = re.search(r"\b(\d{2})\s*/\s*(\d{1,2})\s*식", specs_line)
    if yy_mm_match:
        yy = int(yy_mm_match.group(1))
        year = 2000 + yy if yy <= 30 else 1900 + yy
    else:
        for pattern in [r"\b(\d{4})\s*년식", r"\b(\d{4})\s*년\b", r"\b(\d{2})\s*년식\b"]:
            match = re.search(pattern, specs_line)
            if not match:
                continue
            value = int(match.group(1))
            year = value if value >= 100 else (2000 + value if value <= 30 else 1900 + value)
            break

    mileage_match = re.search(r"([\d,]+)\s*km", specs_line, flags=re.IGNORECASE)
    if mileage_match:
        mileage = int(mileage_match.group(1).replace(",", ""))

    for raw, translated in FUEL_MAP.items():
        if raw in specs_line:
            fuel = translated
            break

    return year, mileage, fuel


def parse_price_krw_value(raw_value: str) -> int | None:
    manwon_match = re.search(r"(\d[\d,\.]*)\s*만원", raw_value, flags=re.IGNORECASE)
    if manwon_match:
        amount = manwon_match.group(1).replace(",", "").replace(".", "")
        return int(amount) * 10000 if amount.isdigit() else None
    digits = re.sub(r"\D", "", raw_value)
    return int(digits) if digits else None


def extract_trim(text: str | None) -> str:
    if not text:
        return ""
    normalized = " ".join(str(text).split())
    if not normalized:
        return ""

    best_match = ""
    for candidate in TRIM_MAP:
        if candidate in normalized and len(candidate) > len(best_match):
            best_match = candidate

    return TRIM_MAP.get(best_match, "")


def resolve_trim(trim_raw: str | None, title_text: str, subtitle_text: str, page_text: str) -> str:
    if trim_raw and trim_raw.strip():
        return trim_raw.strip()

    title_trim = extract_trim(title_text)
    if title_trim:
        return title_trim

    combined_text = " ".join(filter(None, [title_text, subtitle_text, page_text]))
    return extract_trim(combined_text)


async def fetch_encar_car_data(url: str, car_id: str) -> EncarCarData:
    logger.info("Fetching Encar page for car_id=%s", car_id)
    async with httpx.AsyncClient(timeout=settings.encar_request_timeout) as client:
        response = await client.get(url)
        response.raise_for_status()

    html = response.text
    soup = BeautifulSoup(html, "lxml")
    raw_text = soup.get_text(" ", strip=True)
    page_title = soup.title.get_text(" ", strip=True) if soup.title else ""
    og_title_meta = soup.find("meta", attrs={"property": "og:title"})
    og_title = og_title_meta.get("content", "").strip() if og_title_meta else ""
    h1_title = ""
    h1_tag = soup.find("h1")
    if h1_tag:
        h1_title = h1_tag.get_text(" ", strip=True)

    biggest_heading = ""
    for tag_name in ("h1", "h2", "strong"):
        candidate = soup.find(tag_name)
        if candidate:
            biggest_heading = candidate.get_text(" ", strip=True)
            if biggest_heading:
                break
    meta_chunks = []
    for meta_name in ["og:title", "twitter:title", "description"]:
        meta = soup.find("meta", attrs={"property": meta_name}) or soup.find("meta", attrs={"name": meta_name})
        if meta and meta.get("content"):
            meta_chunks.append(meta.get("content"))

    # MVP parser: tries to infer mandatory fields from script blocks/text.
    scripts_text = "\n".join(script.get_text(" ", strip=True) for script in soup.find_all("script"))
    source = f"{scripts_text}\n{raw_text}"
    subtitle_text = ""
    subtitle_match = re.search(r'"subTitle"\s*:\s*"([^"]+)"', scripts_text, re.I)
    if subtitle_match:
        subtitle_text = subtitle_match.group(1).strip()

    script_title = ""
    for pattern in [r'"displayName"\s*:\s*"([^"]+)"', r'"carNm"\s*:\s*"([^"]+)"', r'"title"\s*:\s*"([^"]+)"']:
        match = re.search(pattern, scripts_text, re.I)
        if match:
            script_title = match.group(1).strip()
            if script_title:
                break

    full_title = _first_non_empty(og_title, script_title, page_title, h1_title, biggest_heading)

    def pick_int(pattern: str) -> int | None:
        match = re.search(pattern, source, flags=re.IGNORECASE)
        if not match:
            return None
        digits = re.sub(r"\D", "", match.group(1))
        return int(digits) if digits else None

    def translate(value: str | None, mapping: dict[str, str]) -> str | None:
        if not value:
            return None
        return mapping.get(value.strip(), value.strip())

    def parse_year() -> int | None:
        candidates = [
            r'"year"\s*:\s*"?(\d{4})',
            r'(\d{4})\s*년식',
            r'\b(\d{2})\s*년\b',
            r'\b(\d{4})\s*/\s*\d{1,2}\b',
            r'최초등록[^\d]{0,12}(\d{4})',
        ]
        for pattern in candidates:
            match = re.search(pattern, source, flags=re.IGNORECASE)
            if not match:
                continue
            value = int(match.group(1))
            if value < 100:
                value = 2000 + value if value <= 30 else 1900 + value
            if 1900 <= value <= 2100:
                return value
        return None

    def parse_price_krw() -> int | None:
        manwon_match = re.search(r'(\d[\d,\.]*)\s*만원', source, flags=re.IGNORECASE)
        if manwon_match:
            return parse_price_krw_value(manwon_match.group(0))
        return pick_int(r'"price"\s*:\s*"?([\d,]+)')

    brand_model_match = re.search(r'"manufacturerName"\s*:\s*"([^"]+)".*?"modelGroupName"\s*:\s*"([^"]+)"', scripts_text, re.I | re.S)
    specs_line_match = re.search(r"\d{2}/\d{1,2}식[^\n]*", raw_text)
    specs_line = specs_line_match.group(0) if specs_line_match else ""
    spec_year, spec_mileage, spec_fuel = parse_specs_line(specs_line) if specs_line else (None, None, None)

    year = spec_year or parse_year()
    mileage = spec_mileage or pick_int(r'"mileage"\s*:\s*"?([\d,]+)')
    engine = pick_int(r'"displacement"\s*:\s*"?([\d,]+)')

    fuel_match = re.search(r'"fuelTypeName"\s*:\s*"([^"]+)"', scripts_text, re.I)
    drive_match = re.search(r'"drivetrainName"\s*:\s*"([^"]+)"', scripts_text, re.I)
    trim_match = re.search(r'"gradeName"\s*:\s*"([^"]+)"', scripts_text, re.I)
    price = parse_price_krw()

    brand = translate(brand_model_match.group(1), BRAND_MAP) if brand_model_match else None
    model = translate(brand_model_match.group(2), MODEL_MAP) if brand_model_match else None
    if model and re.search(r"[가-힣]", model):
        model = MODEL_MAP.get(model, model)

    extracted_trim = resolve_trim(trim_match.group(1) if trim_match else None, full_title, subtitle_text, raw_text)
    logger.info("Encar title=%r trim=%r extracted_trim=%r", full_title, trim_match.group(1) if trim_match else None, extracted_trim)

    return EncarCarData(
        car_id=car_id,
        url=url,
        brand=brand,
        model=model,
        year=year,
        mileage_km=mileage,
        engine_volume_cc=engine,
        fuel_type=spec_fuel or (translate(fuel_match.group(1), FUEL_MAP) if fuel_match else None),
        drivetrain=drive_match.group(1) if drive_match else None,
        trim=extracted_trim,
        price_krw=price,
        insurance_status=None,
        title=full_title,
    )
