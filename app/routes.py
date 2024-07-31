from flask import render_template, url_for, flash, redirect
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, GoalForm
from app.models import User, Goal
from flask_login import login_user, current_user, logout_user, login_required
import pandas as pd

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/goals", methods=['GET', 'POST'])
@login_required
def goals():
    form = GoalForm()
    if form.validate_on_submit():
        goal = Goal(calories=form.calories.data, protein=form.protein.data, carbs=form.carbs.data, fat=form.fat.data, user_id=current_user.id)
        db.session.add(goal)
        db.session.commit()
        flash('Your goals have been set!', 'success')
        return redirect(url_for('home'))
    return render_template('goals.html', form=form)

@app.route("/diet_plan")
@login_required
def diet_plan():
    # Load the pre-trained model and other necessary objects
    from diet_plan_ml import generate_diet_plan_ml, classifier, scaler, imputer

    # Load the food dataset
    df = pd.read_csv('food_dataset_with_meal_types_categories_and_veg.csv')

    # Get the user's goals from the database
    goal = Goal.query.filter_by(user_id=current_user.id).first()
    daily_goals = {
        'calories': goal.calories,
        'protein': goal.protein,
        'carbs': goal.carbs,
        'fat': goal.fat
    }

    # Generate the diet plan
    diet_plan_df = generate_diet_plan_ml(classifier, scaler, imputer, df, daily_goals)

    # Convert the DataFrame to HTML for display
    diet_plan_html = diet_plan_df.to_html(classes='table table-striped')

    return render_template('diet_plan.html', diet_plan=diet_plan_html)

@app.route("/current_plan")
@login_required
def current_plan():
    return render_template('current_plan.html')
