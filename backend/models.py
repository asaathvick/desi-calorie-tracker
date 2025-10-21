from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(String, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    meals = relationship("Meal", back_populates="user")
    workouts = relationship("Workout", back_populates="user")

class Meal(Base):
    __tablename__ = "meals"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    calories = Column(Float, nullable=False)
    protein = Column(Float, default=0.0)
    fat = Column(Float, default=0.0)
    carbs = Column(Float, default=0.0)
    logged_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="meals")

class Workout(Base):
    __tablename__ = "workouts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"))
    activity = Column(String, nullable=False)
    duration_minutes = Column(Float, nullable=False)
    calories_burned = Column(Float, nullable=False)
    logged_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="workouts")
