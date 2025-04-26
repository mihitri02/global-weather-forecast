from fastapi import FastAPI, Query
import requests
import psycopg2
from db import get_connection
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend to access the API (important for JS fetch)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for now, can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "7163d9101df5b1f527432772643c4c8b"  # replace this!

@app.get("/weather")
def get_weather(city: str = Query(..., description="City name (e.g. London or London,UK)")):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code != 200:
        return {"error": data.get("message", "Failed to get weather.")}

    city_name = data["name"]
    country = city.split(",")[1] if "," in city else None
    temperature = data["main"]["temp"]
    description = data["weather"][0]["description"]
    icon = f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]

    # Store in PostgreSQL
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO weather_searches 
            (city, country, temperature, description, icon, humidity, wind_speed)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (city_name, country, temperature, description, icon, humidity, wind_speed))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        return {"error": "Database error", "details": str(e)}

    return {
        "city": city_name,
        "country": country,
        "temperature": temperature,
        "description": description,
        "icon": icon,
        "humidity": humidity,
        "wind_speed": wind_speed
    }
    # To run this FastAPI app, use the following command in your terminal:
    #python -m uvicorn main:app --reload

    # Make sure you are in the directory containing main.py before running the command.