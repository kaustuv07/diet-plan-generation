from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    goals = db.relationship('Goal', backref='owner', lazy=True)

class Goal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    calories = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Integer, nullable=False)
    carbs = db.Column(db.Integer, nullable=False)
    fat = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    caloric_value = db.Column(db.Float, nullable=False)
    fat = db.Column(db.Float, nullable=False)
    saturated_fats = db.Column(db.Float, nullable=False)
    monounsaturated_fats = db.Column(db.Float, nullable=False)
    polyunsaturated_fats = db.Column(db.Float, nullable=False)
    carbohydrates = db.Column(db.Float, nullable=False)
    sugars = db.Column(db.Float, nullable=False)
    protein = db.Column(db.Float, nullable=False)
    dietary_fiber = db.Column(db.Float, nullable=False)
    cholesterol = db.Column(db.Float, nullable=False)
    sodium = db.Column(db.Float, nullable=False)
    water = db.Column(db.Float, nullable=False)
    vitamin_a = db.Column(db.Float, nullable=False)
    vitamin_b1 = db.Column(db.Float, nullable=False)
    vitamin_b11 = db.Column(db.Float, nullable=False)
    vitamin_b12 = db.Column(db.Float, nullable=False)
    vitamin_b2 = db.Column(db.Float, nullable=False)
    vitamin_b3 = db.Column(db.Float, nullable=False)
    vitamin_b5 = db.Column(db.Float, nullable=False)
    vitamin_b6 = db.Column(db.Float, nullable=False)
    vitamin_c = db.Column(db.Float, nullable=False)
    vitamin_d = db.Column(db.Float, nullable=False)
    vitamin_e = db.Column(db.Float, nullable=False)
    vitamin_k = db.Column(db.Float, nullable=False)
    calcium = db.Column(db.Float, nullable=False)
    copper = db.Column(db.Float, nullable=False)
    iron = db.Column(db.Float, nullable=False)
    magnesium = db.Column(db.Float, nullable=False)
    manganese = db.Column(db.Float, nullable=False)
    phosphorus = db.Column(db.Float, nullable=False)
    potassium = db.Column(db.Float, nullable=False)
    selenium = db.Column(db.Float, nullable=False)
    zinc = db.Column(db.Float, nullable=False)
    nutrition_density = db.Column(db.Float, nullable=False)
    meal_type = db.Column(db.String(50), nullable=False)  # e.g., 'breakfast', 'lunch', 'dinner', 'snack'

