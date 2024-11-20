from sqlalchemy import create_engine, Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Location(Base):
    __tablename__ = 'locations'
    id = Column(Integer, primary_key=True, autoincrement=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    city = Column(String, nullable=False)
    country = Column(String, nullable=False)

    emails = relationship('Email', back_populates='location')

class DeviceInfo(Base):
    __tablename__ = 'device_info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    browser = Column(String, nullable=False)
    os = Column(String, nullable=False)
    device_id = Column(String, nullable=False)

    emails = relationship('Email', back_populates='device_info')

class Email(Base):
    __tablename__ = 'emails'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    ip_address = Column(String, nullable=False)
    created_at = Column(String, nullable=False)
    location_id = Column(Integer, ForeignKey('locations.id'), nullable=False)
    device_info_id = Column(Integer, ForeignKey('device_info.id'), nullable=False)

    location = relationship('Location', back_populates='emails')
    device_info = relationship('DeviceInfo', back_populates='emails')
    sentences = relationship('Sentence', back_populates='email')


class Sentence(Base):
    __tablename__ = 'sentences'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sentence = Column(String, nullable=False)
    email_id = Column(Integer, ForeignKey('emails.id'), nullable=False)

    email = relationship('Email', back_populates='sentences')

