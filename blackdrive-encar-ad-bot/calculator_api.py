from __future__ import annotations

import os
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field


class CalculateRequest(BaseModel):
    brand: str | None = None
    model: str | None = None
    year: int | None = None
    engine_volume_cc: int | None = None
    fuel_type: str | None = None
    price_krw: int | None = None
    price_with_expenses_krw: int | None = None
    destination: str | None = Field(default="vladivostok")


class CalculateResponse(BaseModel):
    customs_usd: int
    recycling_fee_usd: int
    total_to_vladivostok_usd: int


def _require_bearer_token(authorization: str | None = Header(default=None)) -> None:
    expected_token = os.getenv("CALCULATOR_API_TOKEN")
    if not expected_token:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="CALCULATOR_API_TOKEN is not configured",
        )

    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    provided_token = authorization.removeprefix("Bearer ").strip()
    if provided_token != expected_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")


def _estimate_customs_usd(price_with_expenses_krw: int, year: int | None, engine_volume_cc: int | None) -> int:
    base_usd = round(price_with_expenses_krw / 1350)
    current_year = datetime.now(timezone.utc).year
    car_age = (current_year - year) if year else 5

    age_multiplier = 1.35 if car_age <= 3 else 1.2 if car_age <= 5 else 1.05
    engine_multiplier = 1.0
    if engine_volume_cc:
        if engine_volume_cc > 3000:
            engine_multiplier = 1.35
        elif engine_volume_cc > 2000:
            engine_multiplier = 1.18
        elif engine_volume_cc > 1600:
            engine_multiplier = 1.1

    return round(base_usd * age_multiplier * engine_multiplier)


app = FastAPI(title="Blackdrive Calculator API", version="1.0.0")


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/calculate", response_model=CalculateResponse, dependencies=[Depends(_require_bearer_token)])
def calculate(payload: CalculateRequest) -> CalculateResponse:
    if payload.price_with_expenses_krw is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="price_with_expenses_krw is required",
        )

    customs_usd = _estimate_customs_usd(
        price_with_expenses_krw=payload.price_with_expenses_krw,
        year=payload.year,
        engine_volume_cc=payload.engine_volume_cc,
    )
    recycling_fee_usd = 340
    logistics_usd = 1100
    total_to_vladivostok_usd = customs_usd + recycling_fee_usd + logistics_usd

    return CalculateResponse(
        customs_usd=customs_usd,
        recycling_fee_usd=recycling_fee_usd,
        total_to_vladivostok_usd=total_to_vladivostok_usd,
    )
