from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Container(Base):
    __tablename__ = "containers"

    # define base cols
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True) # name of the container
    qr_code_path = Column(String, nullable=True) # path to the QR code image
    created_at = Column(DateTime, default=datetime.utcnow) # timestamp of creation

    # define relationships
    items = relationship("Item", back_populates="container", cascade="all, delete-orphan") # items in the container
    photos = relationship("Photo", back_populates="container", cascade="all, delete-orphan") # photos in the container


class Item(Base):
    __tablename__ = "items"

    # define base cols
    id = Column(Integer, primary_key=True, index=True)
    container_id = Column(Integer, ForeignKey("containers.id"), nullable=False)
    name = Column(String, nullable=False, index=True) # item name
    quantity = Column(Integer, default=1) # quantity of the item
    created_at = Column(DateTime, default=datetime.utcnow)

    container = relationship("Container", back_populates="items")


class Photo(Base):
    __tablename__ = "photos"

    # define base cols
    id = Column(Integer, primary_key=True, index=True)
    container_id = Column(Integer, ForeignKey("containers.id"), nullable=False)
    file_path = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    container = relationship("Container", back_populates="photos")