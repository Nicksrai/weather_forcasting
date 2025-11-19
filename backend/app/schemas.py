from pydantic import BaseModel
from typing import List, Optional

class WeatherItem(BaseModel):
    dt: int
    temp: float
    temp_min: Optional[float] = None
    temp_max: Optional[float] = None
    weather_main: str
    weather_desc: str
    icon: str

class CurrentWeather(BaseModel):
    city: str
    temp: float
    feels_like: float
    humidity: int
    weather_main: str
    weather_desc: str
    icon: str

class ForecastResponse(BaseModel):
    current: CurrentWeather
    forecast: List[WeatherItem]
