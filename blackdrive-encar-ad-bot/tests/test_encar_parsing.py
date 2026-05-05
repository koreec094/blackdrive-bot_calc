from bot.services.encar_parser import extract_trim, parse_price_krw_value, parse_specs_line


def test_parse_specs_line():
    year, mileage_km, fuel_type = parse_specs_line("21/07식 (22년형) · 41,698km · 가솔린 · 369저7681")
    assert year == 2021
    assert mileage_km == 41698
    assert fuel_type == "бензин"


def test_parse_price_manwon():
    assert parse_price_krw_value("1,200만원") == 12000000


def test_extract_trim_from_fallback_text_prefers_longest_match():
    title = "더 뉴 아반떼 AD 1.6 밸류 플러스"
    assert extract_trim(None, title) == "밸류 플러스"


def test_extract_trim_prefers_grade_name_when_present():
    title = "아반떼 CN7 1.6 인스퍼레이션"
    assert extract_trim("스마트", title) == "스마트"
