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

@app.post("/weather")
async def create_weather_request(request: WeatherRequest):  # Remove Form() and use Pydantic model
    try:
        # Your existing weather API call
        data = requests.get(
            f"https://api.weatherstack.com/current?access_key=8c605e052b2b019be106f884970f96fd&query={request.location}"
        ).json()
        
        # Store data
        global weather_id_counter
        weather_id_counter += 1
        weather_id = str(weather_id_counter)
        weather_storage[weather_id] = {
            "date": request.date,
            "location": request.location,
            "notes": request.notes,
            "weather_data": data
        }
        
        return {"id": weather_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))  # Simple error format

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