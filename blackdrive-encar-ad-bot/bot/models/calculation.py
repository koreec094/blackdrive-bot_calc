from dataclasses import dataclass


@dataclass(slots=True)
class ImportCalculationResult:
    car_price_krw: int | None
    korea_expenses_krw: int
    price_with_expenses_krw: int | None
    customs_usd: int | None
    recycling_fee_usd: int | None
    total_to_vladivostok_usd: int | None
