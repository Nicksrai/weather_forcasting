import React, { useState } from "react";
import SearchBar from "./components/SearchBar";
import ForecastCard from "./components/ForecastCard";

export default function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleSearch(city) {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch(`https://waether-backend.onrender.com/api/weather?city=${encodeURIComponent(city)}`);
      if (!res.ok) throw new Error("City not found or backend error");
      const json = await res.json();
      setData(json);
    } catch (err) {
      setError(err.message || "Error");
      setData(null);
    } finally {
      setLoading(false);
    }
  }

  function getTheme(weather) {
    if (!weather) return "sunny";

    weather = weather.toLowerCase();

    if (weather.includes("clear")) return "sunny";
    if (weather.includes("cloud")) return "cloudy";
    if (weather.includes("rain")) return "rainy";
    if (weather.includes("storm") || weather.includes("thunder")) return "storm";
    if (weather.includes("snow")) return "snowy";

    return "cloudy";
  }

  return (
    <div className={`weather-container ${getTheme(data?.current?.weather_main)}`}>
      <div className="cloud-animation"></div>

      <div className="app-glass-panel">
        <header>
          <h1 className="app-title">Weather Forecast</h1>
        </header>

        <main>
          <SearchBar onSearch={handleSearch} />

          {loading && <p className="loading">Loading...</p>}
          {error && <p className="error">{error}</p>}

          {data && (
            <div className="weather-layout">
              {/* LEFT SIDE: Current Weather */}
              <div className="weather-main glass-card">
                <h2 className="city-name">{data.current.city}</h2>
                <div className="current-section">
                  <img
                    className="main-icon"
                    src={`https://openweathermap.org/img/wn/${data.current.icon}@4x.png`}
                    alt={data.current.weather_desc}
                  />

                  <div>
                    <p className="big-temp">{data.current.temp}°C</p>
                    <p className="condition-text">
                      {data.current.weather_main} — {data.current.weather_desc}
                    </p>
                    <p>Feels like: {data.current.feels_like}°C</p>
                    <p>Humidity: {data.current.humidity}%</p>
                  </div>
                </div>
              </div>

              {/* RIGHT SIDE: Forecast */}
              <div className="forecast-card glass-card">
                <h3 className="forecast-title">5-Day Forecast</h3>

                <div className="forecast-list">
                  {data.forecast.map((f) => (
                    <ForecastCard key={f.dt} item={f} />
                  ))}
                </div>
              </div>
            </div>
          )}
        </main>

        <footer>
          <p className="footer-text">Data from OpenWeatherMap</p>
        </footer>
      </div>
    </div>
  );
}
