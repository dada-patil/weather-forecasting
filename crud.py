from sqlalchemy.orm import Session

from models import Weather
from schemas import WeatherCreate
from schemas import WeatherUpdate


# CREATE
def create_weather(
    db: Session,
    weather: WeatherCreate
):

    new_weather = Weather(
        city=weather.city,
        temperature=weather.temperature,
        humidity=weather.humidity,
        wind_speed=weather.wind_speed,
        condition=weather.condition
    )

    db.add(new_weather)

    db.commit()

    db.refresh(new_weather)

    return new_weather


# READ ALL
def get_all_weather(
    db: Session
):

    return db.query(Weather).all()


# READ BY ID
def get_weather_by_id(
    db: Session,
    weather_id: int
):

    return db.query(Weather).filter(
        Weather.id == weather_id
    ).first()


# READ BY CITY
def get_weather_by_city(
    db: Session,
    city: str
):

    return db.query(Weather).filter(
        Weather.city.ilike(city)
    ).first()


# UPDATE
def update_weather(
    db: Session,
    weather_id: int,
    weather: WeatherUpdate
):

    existing_weather = get_weather_by_id(
        db,
        weather_id
    )

    if existing_weather is None:
        return None

    update_data = weather.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():

        setattr(
            existing_weather,
            key,
            value
        )

    db.commit()

    db.refresh(existing_weather)

    return existing_weather


# DELETE
def delete_weather(
    db: Session,
    weather_id: int
):

    existing_weather = get_weather_by_id(
        db,
        weather_id
    )

    if existing_weather is None:
        return None

    db.delete(existing_weather)

    db.commit()

    return existing_weather