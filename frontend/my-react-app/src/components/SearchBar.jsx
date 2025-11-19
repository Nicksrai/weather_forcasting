import React, { useState } from "react";

export default function SearchBar({ onSearch }) {
  const [city, setCity] = useState("");

  function submit(e) {
    e.preventDefault();
    if (city.trim()) onSearch(city.trim());
  }

  return (
    <form className="search" onSubmit={submit}>
      <input
        value={city}
        onChange={(e) => setCity(e.target.value)}
        placeholder="Enter city (e.g., London)"
        aria-label="City"
      />
      <button type="submit">Search</button>
    </form>
  );
}
