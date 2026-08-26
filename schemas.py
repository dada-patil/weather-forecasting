from pydantic import BaseModel


class WeatherCreate(BaseModel):

    city: str
    temperature: float
    humidity: float
    wind_speed: float
    condition: str


class WeatherUpdate(BaseModel):

    city: str | None = None
    temperature: float | None = None
    humidity: float | None = None
    wind_speed: float | None = None
    condition: str | None = None


class WeatherResponse(WeatherCreate):

    id: int

    class Config:
        from_attributes = True