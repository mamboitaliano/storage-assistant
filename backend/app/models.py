from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base

class Floor(Base):
    __tablename__ = "floors"

    # define base cols
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    floor_number = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # define relationships
    rooms = relationship("Room", back_populates="floor") # rooms on the floor

class Room(Base):
    __tablename__ = "rooms"

    # define base cols
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True) # name of the room
    floor_id = Column(Integer, ForeignKey("floors.id"), nullable=True) # floor the room belongs to
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # define relationships
    floor = relationship("Floor", back_populates="rooms") # floor the room belongs to
    containers = relationship("Container", back_populates="room") # containers in the room
    items = relationship("Item", back_populates="room") # items in the room

class Container(Base):
    __tablename__ = "containers"

    # define base cols
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True) # name of the container
    qr_code_path = Column(String, nullable=True) # path to the QR code image
    created_at = Column(DateTime, default=datetime.now(timezone.utc)) # timestamp of creation
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=True) # room the container belongs to

    # define relationships
    room = relationship("Room", back_populates="containers") # room the container belongs to
    items = relationship("Item", back_populates="container") # items in the container
    photos = relationship("Photo", back_populates="container") # photos in the container

class Item(Base):
    __tablename__ = "items"

    # define base cols
    id = Column(Integer, primary_key=True, index=True)
    container_id = Column(Integer, ForeignKey("containers.id"), nullable=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    name = Column(String, nullable=False, index=True) # item name
    quantity = Column(Integer, default=1) # quantity of the item
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    room = relationship("Room", back_populates="items") # room the item belongs to
    container = relationship("Container", back_populates="items") # container the item belongs to

class Photo(Base):
    __tablename__ = "photos"

    # define base cols
    id = Column(Integer, primary_key=True, index=True)
    container_id = Column(Integer, ForeignKey("containers.id"), nullable=False)
    file_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    container = relationship("Container", back_populates="photos")