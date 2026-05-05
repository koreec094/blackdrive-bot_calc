def format_int_with_dots(value: int | None) -> str:
    if value is None:
        return "требуется проверка"
    return f"{value:,}".replace(",", ".")


def format_mileage_km(value: int | None) -> str:
    if value is None:
        return "требуется проверка"
    return f"{format_int_with_dots(value)} km"


def format_engine(engine_volume_cc: int | None, fuel_type: str | None) -> str:
    if engine_volume_cc is None:
        return "требуется проверка"
    liters = round(engine_volume_cc / 1000, 1)
    fuel = fuel_type or "требуется проверка"
    return f"{liters:.1f} {fuel}"


def format_drive(drivetrain: str | None) -> str:
    if drivetrain is None:
        return "требуется проверка"
    value = drivetrain.upper()
    if value in {"2WD", "FWD", "RWD"}:
        return "2вд"
    if value in {"4WD", "AWD"}:
        return "4вд"
    return drivetrain
