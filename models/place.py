#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Integer, String, Column, ForeignKey, Float, Table
from sqlalchemy.orm import relationship


class Place(BaseModel, Base):
    """This is the class for Place
    Attributes:
        city_id: city id
        user_id: user id
        name: name input
        description: string of description
        number_rooms: number of room in int
        number_bathrooms: number of bathrooms in int
        max_guest: maximum guest in int
        price_by_night:: pice for a staying in int
        latitude: latitude in flaot
        longitude: longitude in float
        amenity_ids: list of Amenity ids
    """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'),
                                 nullable=False, primary_key=True),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'), primary_key=True))
    amenities = relationship('Amenity', secondary=place_amenity,
                             viewonly=False, backref='place_amenities')
    reviews = relationship('Review', backref='place',
                           cascade="all, delete, delete-orphan")
    amenity_ids = []

    @property
    def reviews(self):
        """ Returns all review of a place"""
        from models import storage
        filter = []
        for review in storage.all(Review).values():
            if review.place_id == Place.id:
                filter.append(review)
        return filter

    @property
    def amenities(self):
        """ Returns all amenities in places """
        from models import storage
        filter = []
        for amenity in storage.all(Amenity).values():
            if amenity.id in Place.amenity_ids:
                filter.append(amenity)
        return filter

    @amenities.setter
    def amenities(self, obj):
        """ handles append method for adding an Amenity.id
            to amenity_ids"""
        from models.amenity import Amenity
        if obj is Amenity:
            Place.amenity_ids.append(obj.id)
