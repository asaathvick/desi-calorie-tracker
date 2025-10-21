from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
import uuid
import hashlib

app = FastAPI(title="Calorie Tracker API")

# In-memory stores (use a real database in production)
users: Dict[str, Dict] = {}
meals: List[Dict] = []
workouts: List[Dict] = []
foods: List[Dict] = [
    {"id": "rice", "name": "Rice, cooked", "calories": 130, "protein": 2.7, "fat": 0.3, "carbs": 28},
    {"id": "dal", "name": "Dal (lentil soup)", "calories": 170, "protein": 9.0, "fat": 2.0, "carbs": 30},
    {"id": "roti", "name": "Roti", "calories": 100, "protein": 3.0, "fat": 1.5, "carbs": 20},
    # …add more Indian foods as needed
]

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class MealLog(BaseModel):
    user_id: str
    food_id: Optional[str] = None
    name: Optional[str] = None
    calories: float = Field(..., gt=0)
    protein: float = 0.0
    fat: float = 0.0
    carbs: float = 0.0
    logged_at: datetime = datetime.utcnow()

class WorkoutLog(BaseModel):
    user_id: str
    activity: str
    duration_minutes: float = Field(..., gt=0)
    calories_burned: float = Field(..., ge=0)
    logged_at: datetime = datetime.utcnow()

@app.post("/register")
def register(user: UserCreate):
    if user.username in users:
        raise HTTPException(status_code=400, detail="Username already exists.")
    user_id = str(uuid.uuid4())
    users[user.username] = {"id": user_id, "password_hash": hash_password(user.password)}
    return {"user_id": user_id, "message": "User registered successfully"}

@app.post("/login")
def login(credentials: UserLogin):
    user = users.get(credentials.username)
    if not user or user["password_hash"] != hash_password(credentials.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"user_id": user["id"], "message": "Login successful"}

@app.get("/foods")
def list_foods():
    return {"foods": foods}

@app.post("/log-meal")
def log_meal(meal: MealLog):
    # If a food_id is provided, auto-fill macro values
    if meal.food_id:
        food = next((f for f in foods if f["id"] == meal.food_id), None)
        if food:
            meal.name = food["name"]
            meal.calories = food["calories"]
            meal.protein = food["protein"]
            meal.fat = food["fat"]
            meal.carbs = food["carbs"]
    # Validate user
    if meal.user_id not in [u["id"] for u in users.values()]:
        raise HTTPException(status_code=404, detail="User not found.")
    entry = meal.dict()
    meals.append(entry)
    return {"message": "Meal logged", "meal": entry}

@app.post("/log-workout")
def log_workout(workout: WorkoutLog):
    if workout.user_id not in [u["id"] for u in users.values()]:
        raise HTTPException(status_code=404, detail="User not found.")
    entry = workout.dict()
    workouts.append(entry)
    return {"message": "Workout logged", "workout": entry}

@app.get("/summary/{user_id}")
def get_summary(user_id: str):
    user_meals = [m for m in meals if m["user_id"] == user_id]
    user_workouts = [w for w in workouts if w["user_id"] == user_id]
    net_calories = sum(m["calories"] for m in user_meals) - sum(w["calories_burned"] for w in user_workouts)
    return {
        "meals": user_meals,
        "workouts": user_workouts,
        "net_calories": net_calories
    }
