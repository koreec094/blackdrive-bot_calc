from dataclasses import dataclass


@dataclass(slots=True)
class EncarCarData:
    car_id: str
    url: str
    brand: str | None = None
    model: str | None = None
    year: int | None = None
    mileage_km: int | None = None
    engine_volume_cc: int | None = None
    fuel_type: str | None = None
    drivetrain: str | None = None
    trim: str | None = None
    price_krw: int | None = None
    insurance_status: str | None = None
    title: str | None = None
