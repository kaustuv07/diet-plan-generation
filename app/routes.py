from flask import render_template, url_for, flash, redirect
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, GoalForm
from app.models import User, Goal
from flask_login import login_user, current_user, logout_user, login_required
import pandas as pd
from flask import request, jsonify
from app.models import DietPlan

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
        goal = Goal(
            calories=form.calories.data,
            protein=form.protein.data,
            carbs=form.carbs.data,
            fat=form.fat.data,
            bmi=form.bmi.data,
            fitness_level=form.fitness_level.data,
            health_issues=form.health_issues.data,
            veg_preference=form.veg_preference.data,
            weight_goal=form.weight_goal.data,
            dietary_restrictions=form.dietary_restrictions.data,
            user_id=current_user.id
        )
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

    # Convert DataFrame to a list of dictionaries for easier use in Jinja2 template
    diet_plan_list = diet_plan_df.to_dict(orient='records')

    return render_template('diet_plan.html', diet_plan=diet_plan_list)


@app.route('/current_diet_plan', methods=['GET'])
@login_required
def current_plan():
    user_id = current_user.username
    diet_plan_df = fetch_diet_plan(user_id)
    # Convert DataFrame to list of dictionaries
    diet_plan = diet_plan_df.to_dict(orient='records')
    return render_template('current_plan.html', diet_plan=diet_plan)
def fetch_diet_plan(user_id):
    # Fetch the diet plan from the database based on the user_id
    diet_plans = DietPlan.query.filter_by(user_id=user_id).all()
    # Convert query results to DataFrame
    records = [plan.diet_plan for plan in diet_plans]
    if records:
        # Flatten the list of records if needed
        diet_plan_df = pd.DataFrame([item for sublist in records for item in sublist])
        return diet_plan_df
    else:
        return pd.DataFrame()  # Return an empty DataFrame if no records found



@app.route('/save_diet_plan', methods=['POST'])
@login_required
def save_diet_plan():
    data = request.json
    diet_plan = data.get('diet_plan')
    user_id = current_user.username

    if not diet_plan:
        return jsonify({'error': 'No diet plan provided'}), 400

    # Convert the received diet plan to a DataFrame if needed
    diet_plan_df = pd.DataFrame(diet_plan)
    
    # Convert DataFrame to list of dicts
    diet_plan_records = diet_plan_df.to_dict(orient='records')

    # Check if a diet plan for this user already exists
    existing_plan = DietPlan.query.filter_by(user_id=user_id).first()
    if existing_plan:
        # Update the existing record
        existing_plan.diet_plan = diet_plan_records
    else:
        # Create a new DietPlan record
        new_diet_plan = DietPlan(user_id=user_id, diet_plan=diet_plan_records)
        db.session.add(new_diet_plan)

    db.session.commit()

    return jsonify({'message': 'Diet plan saved successfully'}), 200



