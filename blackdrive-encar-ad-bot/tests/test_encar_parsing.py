from bot.services.encar_parser import parse_price_krw_value, parse_specs_line


def test_parse_specs_line():
    year, mileage_km, fuel_type = parse_specs_line("21/07식 (22년형) · 41,698km · 가솔린 · 369저7681")
    assert year == 2021
    assert mileage_km == 41698
    assert fuel_type == "бензин"


def test_parse_price_manwon():
    assert parse_price_krw_value("1,200만원") == 12000000
