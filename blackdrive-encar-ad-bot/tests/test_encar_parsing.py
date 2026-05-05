from bot.services.encar_parser import extract_trim, parse_price_krw_value, parse_specs_line, resolve_trim


def test_parse_specs_line():
    year, mileage_km, fuel_type = parse_specs_line("21/07식 (22년형) · 41,698km · 가솔린 · 369저7681")
    assert year == 2021
    assert mileage_km == 41698
    assert fuel_type == "бензин"


def test_parse_price_manwon():
    assert parse_price_krw_value("1,200만원") == 12000000


def test_extract_trim_from_title_returns_translated_value():
    title = "스포티지 5세대 가솔린 1.6 터보 2WD 프레스티지"
    assert extract_trim(title) == "Prestige"


def test_extract_trim_prefers_longest_match():
    title = "더 뉴 아반떼 AD 1.6 밸류 플러스"
    assert extract_trim(title) == "Value Plus"


def test_resolve_trim_prefers_grade_name_when_present():
    title = "아반떼 CN7 1.6 인스퍼레이션"
    assert resolve_trim("스마트", title, "", "") == "스마트"


def test_extract_trim_self_checks():
    assert extract_trim("스포티지 5세대 가솔린 1.6 터보 2WD 프레스티지") == "Prestige"
    assert extract_trim("모닝 어반 (JA) 프레스티지") == "Prestige"
    assert extract_trim("아반떼 CN7 1.6 인스퍼레이션") == "Inspiration"
