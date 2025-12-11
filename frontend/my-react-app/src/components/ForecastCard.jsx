import React from "react";

function formatDateFromDt(dt) {
  const d = new Date(dt * 1000);
  return d.toLocaleDateString(undefined, { weekday: "short", month: "short", day: "numeric" });
}

export default function ForecastCard({ item }) {
  return (
    <div className="forecast-day">
      <p className="date">{formatDateFromDt(item.dt)}</p>
      <img
        className="weather-icon"
        src={`https://openweathermap.org/img/wn/${item.icon}@2x.png`}
        alt={item.weather_desc}
        width="64"
        height="64"
      />
      <p className="temp">{item.temp}°C</p>
      <p className="desc">{item.weather_main}</p>
      <p className="mini">{item.temp_min}° / {item.temp_max}°</p>
    </div>
  );
}
