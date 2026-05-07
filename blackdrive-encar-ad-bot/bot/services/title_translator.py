import re

BRAND_TRANSLATIONS = {
    "르노코리아(삼성)": "Renault Samsung", "르노삼성": "Renault Samsung", "르노코리아": "Renault Korea", "삼성": "Renault Samsung",
    "쉐보레(GM대우)": "Chevrolet", "GM대우": "Chevrolet", "쉐보레": "Chevrolet", "대우": "Daewoo",
    "메르세데스-벤츠": "Mercedes-Benz", "벤츠": "Mercedes-Benz",
    "기아": "Kia", "현대": "Hyundai", "제네시스": "Genesis", "쌍용": "SsangYong", "KG모빌리티": "KG Mobility",
    "아우디": "Audi", "폭스바겐": "Volkswagen", "볼보": "Volvo", "미니": "MINI", "포드": "Ford", "링컨": "Lincoln", "지프": "Jeep",
    "크라이슬러": "Chrysler", "캐딜락": "Cadillac", "테슬라": "Tesla", "렉서스": "Lexus", "토요타": "Toyota", "혼다": "Honda", "닛산": "Nissan",
    "인피니티": "Infiniti", "푸조": "Peugeot", "시트로엥": "Citroen", "랜드로버": "Land Rover", "재규어": "Jaguar", "포르쉐": "Porsche",
    "마세라티": "Maserati", "페라리": "Ferrari", "람보르기니": "Lamborghini", "벤틀리": "Bentley", "롤스로이스": "Rolls-Royce",
    "애스턴마틴": "Aston Martin", "맥라렌": "McLaren", "폴스타": "Polestar",
    "Ford": "Ford", "Audi": "Audi", "Volkswagen": "Volkswagen", "Volvo": "Volvo", "MINI": "MINI", "BMW": "BMW", "Jeep": "Jeep", "Tesla": "Tesla", "Porsche": "Porsche", "Land Rover": "Land Rover", "Maserati": "Maserati",
}

TRANSLATIONS = {
    **BRAND_TRANSLATIONS,
    "2시리즈 액티브 투어러": "2-Series Active Tourer", "티구안 올스페이스": "Tiguan Allspace", "레인지로버 스포츠": "Range Rover Sport",
    "레인지로버": "Range Rover",
    "레인지로버 벨라": "Range Rover Velar", "레인지로버 이보크": "Range Rover Evoque", "랜드크루저": "Land Cruiser", "그랜드 체로키": "Grand Cherokee",
    "디스커버리 스포츠": "Discovery Sport", "렉스턴 스포츠": "Rexton Sports", "존 쿠퍼 웍스": "JCW", "파사트 GT": "Passat GT",
    "플러그인 하이브리드": "Plug-in Hybrid", "로얄 스페셜": "Royal Special", "밸류 플러스": "Value Plus", "베스트 셀렉션": "Best Selection",
    "밸류플러스": "Value Plus", "베스트셀렉션": "Best Selection", "스탠다드 레인지": "Standard Range", "M 스포츠": "M-Sport", "M스포츠": "M-Sport",
    "AMG 라인": "AMG Line", "AMG라인": "AMG Line", "S 라인": "S Line", "S라인": "S Line", "GT 라인": "GT Line", "GT라인": "GT Line",
    "N 라인": "N Line", "N라인": "N Line", "2시리즈": "2-Series", "3시리즈": "3-Series", "5시리즈": "5-Series", "911": "911",
    "E-클래스": "E-Class", "GLB-클래스": "GLB-Class", "카이엔": "Cayenne", "카레라": "Carrera", "카브리올레": "Cabriolet",
    "익스플로러": "Explorer", "머스탱": "Mustang", "랭글러": "Wrangler", "레니게이드": "Renegade", "트레일블레이저": "Trailblazer",
    "골프": "Golf", "아테온": "Arteon", "제타": "Jetta", "기블리": "Ghibli", "쿠퍼 S": "Cooper S", "쿠퍼": "Cooper", "컨트리맨": "Countryman",
    "컨버터블": "Convertible", "스포티지": "Sportage", "모델 S": "Model S", "콰트로": "quattro", "에코부스트": "EcoBoost", "터보": "Turbo",
    "프레스티지": "Prestige", "시그니처": "Signature", "노블레스": "Noblesse", "트렌디": "Trendy", "스마트": "Smart", "모던": "Modern",
    "스타일": "Style", "프리미엄": "Premium", "프리미어": "Premier", "럭셔리": "Luxury", "인스퍼레이션": "Inspiration", "익스클루시브": "Exclusive",
    "캘리그래피": "Calligraphy", "그래비티": "Gravity", "플래티넘": "Platinum", "마스터즈": "Masters", "리미티드": "Limited", "어드밴티지": "Advantage",
    "인스크립션": "Inscription", "모멘텀": "Momentum", "얼티메이트": "Ultimate", "다이나믹": "Dynamic", "오버랜드": "Overland", "루비콘": "Rubicon",
    "사하라": "Sahara", "그란스포츠": "GranSport", "그란루쏘": "GranLusso", "기본형": "Base", "고급형": "High", "스페셜": "Special",
    "마이핏": "My Fit", "초이스": "Choice", "파이니스트": "Finest", "로얄": "Royal", "에어": "Air", "어스": "Earth",
    "플래드": "Plaid", "롱레인지": "Long Range", "퍼포먼스": "Performance", "하이브리드": "Hybrid", "전기": "Electric",
    "1세대": "1st Gen", "2세대": "2nd Gen", "3세대": "3rd Gen", "4세대": "4th Gen", "5세대": "5th Gen", "6세대": "6th Gen", "7세대": "7th Gen", "8세대": "8th Gen",
    "세대": "Gen", "4도어": "4-Door", "2도어": "2-Door",
}

FUEL_WORDS_TO_REMOVE = ["가솔린", "디젤", "경유", "휘발유", "LPG", "엘피지"]
SEO_MARKERS = [" 중고차", ": 내차팔기", "내차팔기", "내차사기", "| 엔카", "- 엔카", "엔카", "Encar"]
REGIONS = ["서울","경기","인천","부산","대구","대전","광주","울산","세종","제주","강원","충북","충남","전북","전남","경북","경남"]


def _normalize(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,)])", r"\1", text)
    return text


def clean_raw_title(raw_title: str) -> str:
    cleaned = _normalize(raw_title or "")
    for m in SEO_MARKERS:
        idx = cleaned.find(m)
        if idx >= 0:
            cleaned = cleaned[:idx]
    cleaned = _normalize(cleaned)
    cleaned = re.sub(rf"(?:\s+(?:{'|'.join(REGIONS)}))+$", "", cleaned).strip()
    return _normalize(cleaned)


def _ensure_brand(title: str) -> str:
    if any(title.startswith(b + " ") or title == b for b in BRAND_TRANSLATIONS.values()):
        return title
    hints = [("E-Class", "Mercedes-Benz"), ("3-Series", "BMW"), ("5-Series", "BMW"), ("Sportage", "Kia")]
    for token, brand in hints:
        if re.search(rf"(?<!\w){re.escape(token)}(?!\w)", title):
            return f"{brand} {title}"
    return title


def translate_full_title(raw_title: str) -> str:
    text = _normalize(raw_title or "")
    if not text:
        return ""
    for source in sorted(TRANSLATIONS, key=len, reverse=True):
        text = text.replace(source, TRANSLATIONS[source])
    for fuel in FUEL_WORDS_TO_REMOVE:
        text = re.sub(rf"(?<!\w){re.escape(fuel)}(?!\w)", " ", text)
    text = re.sub(r"\b([A-Z]{0,4}\d{2,4}|\d{3})\s+([di])\b", r"\1\2", text)
    text = text.replace("플러스", "Plus")
    text = _normalize(text)
    text = re.sub(r"^(BMW|Ford|Audi|Volkswagen|Volvo|MINI|Jeep|Tesla|Porsche|Land Rover|Maserati|Mercedes-Benz|Chevrolet|Renault Samsung)\s+\1\b", r"\1", text)
    return _ensure_brand(text)
