from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import asyncio

from .weather_services import fetch_weather_for_city
from .schemas import ForecastResponse, CurrentWeather, WeatherItem

app = FastAPI(title="Weather Forecast API")

# Allow local dev frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/weather", response_model=ForecastResponse)
async def get_weather(city: Optional[str] = "London"):
    try:
        data = await fetch_weather_for_city(city)
        # Pydantic models expect correct types; we return raw dict matching schema
        return data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
