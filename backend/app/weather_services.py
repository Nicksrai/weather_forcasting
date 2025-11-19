import os
import httpx
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY")
BASE_URL = os.getenv("OPENWEATHER_BASE_URL", "https://api.openweathermap.org")



# These endpoints assume OpenWeatherMap:
CURRENT_URL = f"{BASE_URL}/data/2.5/weather"
FORECAST_URL = f"{BASE_URL}/data/2.5/forecast"

# helper to convert Kelvin -> Celsius
def k_to_c(k):
    return round(k - 273.15, 1)

async def fetch_weather_for_city(city: str):
    """Fetch current weather + 5-day forecast (3h intervals), simplify to daily summary."""
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Current weather
        cur_resp = await client.get(CURRENT_URL, params={"q": city, "appid": API_KEY})
        cur_resp.raise_for_status()
        cur = cur_resp.json()

        # Forecast (3-hourly)
        f_resp = await client.get(FORECAST_URL, params={"q": city, "appid": API_KEY})
        f_resp.raise_for_status()
        frc = f_resp.json()

    # Build current simplified object
    current = {
        "city": cur.get("name"),
        "temp": k_to_c(cur["main"]["temp"]),
        "feels_like": k_to_c(cur["main"]["feels_like"]),
        "humidity": cur["main"]["humidity"],
        "weather_main": cur["weather"][0]["main"],
        "weather_desc": cur["weather"][0]["description"],
        "icon": cur["weather"][0]["icon"],
    }

    # Process forecast: reduce 3-hour entries to one per day (midday if possible)
    # We'll pick the forecast entry at 12:00:00 each day; fallback to first entry of day.
    days = {}
    for item in frc.get("list", []):
        dt_txt = item["dt_txt"]  # "2025-11-20 12:00:00"
        date = dt_txt.split(" ")[0]
        time = dt_txt.split(" ")[1]
        # prefer 12:00:00
        if date not in days or time == "12:00:00":
            days[date] = item

    # create list of next 5 days (exclude today's date if you want)
    forecast_items = []
    today = datetime.utcnow().date().isoformat()
    sorted_dates = sorted(days.keys())
    for date in sorted_dates:
        if date < today:
            continue
        entry = days[date]
        wi = {
            "dt": entry["dt"],
            "temp": k_to_c(entry["main"]["temp"]),
            "temp_min": k_to_c(entry["main"].get("temp_min", entry["main"]["temp"])),
            "temp_max": k_to_c(entry["main"].get("temp_max", entry["main"]["temp"])),
            "weather_main": entry["weather"][0]["main"],
            "weather_desc": entry["weather"][0]["description"],
            "icon": entry["weather"][0]["icon"],
        }
        forecast_items.append(wi)
        if len(forecast_items) >= 5:
            break

    return {"current": current, "forecast": forecast_items}
