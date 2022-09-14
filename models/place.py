#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Integer, String, Column, ForeignKey, Float


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
    __tablename = "places"
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=False)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    amenity_ids = []

    if environ.get('HBNB_TYPE_STORAGE') == "db":
        reviews = relationship("Review",
                               backref="place",
                               cascade="all, delete, delete-orphan")
        amenities = relationship("Amenity",
                                 secondary=place_amenity,
                                 viewonly=False)

    else:
        @property
        def reviews(self):
            """
            Returns the list of Review instances
            with place_id equals to the current Place.id
            """
            all_reviews = models.storage.all(Review)
            place_reviews = []
            for review_ins in all_reviews.values():
                if review_ins.place_id == self.id:
                    place_reviews.append(review_ins)

            return place_reviews

        @property
        def amenities(self):
            """
            Returns the list of Amenity instances based on the
            attribute amenity_ids that contains all Amenity.id
            linked to the Place
            """
            all_amenities = models.storage.all(Amenity)
            place_amenities = []
            for amenity_ins in all_amenities.values():
                if amenity_ins.place_id == self.id:
                    place_amenities.append(amenity_ins)

            return place_amenities

        @amenities.setter
        def amenities(self, amenity_obj):
            """
            Handles append method for adding an Amenity.id to the attribute
            amenity_ids
            """
            if isinstance(amenity_obj, models.Amenity):
                self.amenities.append(amenity_obj.id)
