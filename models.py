from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Float

from database import Base


class Weather(Base):

    __tablename__ = "weather"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    city = Column(
        String,
        nullable=False
    )

    temperature = Column(
        Float,
        nullable=False
    )

    humidity = Column(
        Float,
        nullable=False
    )

    wind_speed = Column(
        Float,
        nullable=False
    )

    condition = Column(
        String,
        nullable=False
    )