import requests
from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

import models
import crud

from database import engine
from database import SessionLocal

from schemas import WeatherCreate
from schemas import WeatherUpdate
from schemas import WeatherResponse

from weather_api import get_weather


# -----------------------------------------
# CREATE DATABASE TABLE
# -----------------------------------------

models.Base.metadata.create_all(
    bind=engine
)


# -----------------------------------------
# FASTAPI APP
# -----------------------------------------

app = FastAPI(
    title="Weather Forecasting API",
    description="Weather Forecasting CRUD Application",
    version="1.0"
)


# -----------------------------------------
# DATABASE CONNECTION
# -----------------------------------------

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


# -----------------------------------------
# HOME
# -----------------------------------------

@app.get("/")
def home():

    return {
        "message": "Weather Forecasting API",
        "status": "Running"
    }


# =========================================
# CREATE
# =========================================

@app.post(
    "/weather",
    response_model=WeatherResponse
)
def create_weather(
    weather: WeatherCreate,
    db: Session = Depends(get_db)
):

    return crud.create_weather(
        db,
        weather
    )


# =========================================
# READ ALL
# =========================================

@app.get(
    "/weather",
    response_model=list[WeatherResponse]
)
def read_all_weather(
    db: Session = Depends(get_db)
):

    return crud.get_all_weather(db)


# =========================================
# READ BY ID
# =========================================

@app.get(
    "/weather/id/{weather_id}",
    response_model=WeatherResponse
)
def read_weather_by_id(
    weather_id: int,
    db: Session = Depends(get_db)
):

    weather = crud.get_weather_by_id(
        db,
        weather_id
    )

    if weather is None:

        raise HTTPException(
            status_code=404,
            detail="Weather record not found"
        )

    return weather


# =========================================
# LIVE WEATHER BY CITY
# =========================================

@app.get(
    "/weather/city/{city}"
)
def live_weather(city: str):

    try:

        weather = get_weather(city)

        if weather is None:

            raise HTTPException(
                status_code=404,
                detail="City not found"
            )

        return weather

    except requests.exceptions.RequestException:

        raise HTTPException(
            status_code=503,
            detail="Weather service unavailable"
        )


# =========================================
# UPDATE
# =========================================

@app.put(
    "/weather/{weather_id}",
    response_model=WeatherResponse
)
def update_weather(
    weather_id: int,
    weather: WeatherUpdate,
    db: Session = Depends(get_db)
):

    updated_weather = crud.update_weather(
        db,
        weather_id,
        weather
    )

    if updated_weather is None:

        raise HTTPException(
            status_code=404,
            detail="Weather record not found"
        )

    return updated_weather


# =========================================
# DELETE
# =========================================

@app.delete(
    "/weather/{weather_id}"
)
def delete_weather(
    weather_id: int,
    db: Session = Depends(get_db)
):

    weather = crud.delete_weather(
        db,
        weather_id
    )

    if weather is None:

        raise HTTPException(
            status_code=404,
            detail="Weather record not found"
        )

    return {
        "message": "Weather deleted successfully",
        "id": weather_id
    }