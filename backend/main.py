from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional, Annotated
import uvicorn
import requests

app = FastAPI(title="Weather Data System", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for weather data
weather_storage: Dict[str, Dict[str, Any]] = {}

class WeatherRequest(BaseModel):
    date: str
    location: str
    notes: Optional[str] = ""

class WeatherResponse(BaseModel):
    id: str

weather_id_counter = 0

@app.post("/weather", response_model=WeatherResponse)
async def create_weather_request(
    date: Annotated[str, Form()],
    location: Annotated[str, Form()],
    notes: Annotated[Optional[str], Form()] = ""
):
    """
    Handle weather data submission:
    1. Receive form data (date, location, notes)
    2. Calls WeatherStack API for the location
    3. Stores combined data with unique ID in memory
    4. Returns the ID to frontend
    """
    global weather_id_counter
    
    # Get weather data from WeatherStack
    weather_data = requests.get(
        f"https://api.weatherstack.com/current?access_key=8c605e052b2b019be106f884970f96fd&query={location}"
    ).json()
    
    # Create new entry
    weather_id_counter += 1
    weather_id = str(weather_id_counter)
    
    weather_storage[weather_id] = {
        "date": date,
        "location": location,
        "notes": notes,
        "weather_data": weather_data
    }
    
    return {"id": weather_id}

@app.get("/weather/{weather_id}")
async def get_weather_data(weather_id: str):
    """
    Retrieve stored weather data by ID.
    """
    if weather_id not in weather_storage:
        raise HTTPException(status_code=404, detail="Weather data not found")
    
    return weather_storage[weather_id]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)