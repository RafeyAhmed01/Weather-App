const resultsDiv = document.getElementById("results");
const errorDiv = document.getElementById("error");

async function searchWeather() {
    const city = document.getElementById('cityInput').value.trim();

    if (!city) {
        document.getElementById('cityInput').focus();
        return;
    }

    resultsDiv.style.display = "none";
    errorDiv.style.display = "none";

    try {
        const response = await fetch(`https://weather-app-production-4428.up.railway.app/api/v1/${encodeURIComponent(city)}`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Something went wrong");
        }

        document.getElementById("pCityName").textContent = data.name;
        document.getElementById("pCountryName").textContent = data.country;
        document.getElementById("pWeather").textContent = data.weather;
        document.getElementById("pTemperature").textContent = `${data.temperature}°C`;
        document.getElementById("pFeelsLike").textContent = `${data.feels_like}°C`;
        document.getElementById("pHumidity").textContent = `${data.humidity}%`;

        resultsDiv.style.display = "block";

    } catch (err) {
        console.error("Fetch error:", err);
        errorDiv.textContent = `❌ ${err.message}`;
        errorDiv.style.display = "block";
    }
}

document.getElementById('cityInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        searchWeather();
    }
});