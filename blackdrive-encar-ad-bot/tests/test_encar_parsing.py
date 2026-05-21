from bot.services.encar_parser import clean_raw_title, extract_trim, parse_price_krw_value, parse_specs_line, resolve_trim, translate_full_title


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


def test_translate_full_title_self_checks():
    assert translate_full_title("E-클래스 W213 E300e 4MATIC 익스클루시브") == "Mercedes-Benz E-Class W213 E300e 4MATIC Exclusive"
    assert translate_full_title("스포티지 5세대 가솔린 1.6 터보 2WD 프레스티지") == "Kia Sportage 5th Gen 1.6 Turbo 2WD Prestige"
    assert translate_full_title("쉐보레(GM대우) 트레일블레이저") == "Chevrolet Trailblazer"
    assert translate_full_title("르노코리아(삼성) QM6") == "Renault Samsung QM6"
    assert translate_full_title("GLB-클래스 X247 GLB200 d") == "Mercedes-Benz GLB-Class X247 GLB200d"


def test_clean_raw_title_self_checks():
    assert clean_raw_title("GLB-클래스 X247 GLB200 d 경기 중고차 : 내차팔기·내차사기") == "GLB-클래스 X247 GLB200 d"
    assert clean_raw_title("E-클래스 W213 E300e 4MATIC 익스클루시브 서울 중고차 : 내차팔기·내차사기") == "E-클래스 W213 E300e 4MATIC 익스클루시브"
    assert (
        translate_full_title(clean_raw_title("스포티지 5세대 가솔린 1.6 터보 2WD 프레스티지 경기 중고차 : 내차팔기·내차사기"))
        == "Kia Sportage 5th Gen 1.6 Turbo 2WD Prestige"
    )
from bot.services.formatter import format_korean_plate_number
from bot.services.encar_parser import parse_plate_number


def test_format_korean_plate_number():
    assert format_korean_plate_number("238어4590") == "238어 4590"
    assert format_korean_plate_number("123가 4567") == "123가 4567"
    assert format_korean_plate_number("45나6789") == "45나 6789"
    assert format_korean_plate_number(" 45나 6789 ") == "45나 6789"
    assert format_korean_plate_number("") is None


def test_parse_plate_number():
    text = "21/07식 (22년형) · 41,698km · 가솔린 · 369저7681"
    assert parse_plate_number(text) == "369저7681"
