import os

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET"])

@app.get("favicon.ico")
def get_icon():
    return 

@app.get("/api/v1/{city_name}")
def fetch_weather(city_name: str) -> dict:
    if not city_name.strip():
        raise HTTPException(status_code=400, detail="City name cannot be empty")

    API_KEY = os.getenv("API_KEY")

    geo_response = requests.get(
        f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&limit=1&appid={API_KEY}"
    )
    raw_json = geo_response.json()

    if not raw_json:
        raise HTTPException(status_code=404, detail=f"City '{city_name}' not found")

    lat = raw_json[0]["lat"]
    lon = raw_json[0]["lon"]

    weather_response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    )
    weather_data = weather_response.json()

    return {
        "name": weather_data["name"],
        "country": weather_data["sys"]["country"],
        "weather": weather_data["weather"][0]["main"],
        "temperature": weather_data["main"]["temp"],
        "feels_like": weather_data["main"]["feels_like"],
        "humidity": weather_data["main"]["humidity"],
    }