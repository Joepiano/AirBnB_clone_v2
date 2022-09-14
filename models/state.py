#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship
from models.city import City


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state",
                          cascade="all, delete, delete-orphan")

    @property
    def cities(self):
        """ return the cities that matches the state_id
            that match the class attribute id """

        from models import storage
        filter = []
        for city in storage.all(City).values():
            if city.state_id == State.id:
                filter.append(city)
        return filter

