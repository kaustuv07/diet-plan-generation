import pandas as pd
import joblib
import numpy as np

# Load the pre-trained model and other necessary objects
classifier = joblib.load('classifier.pkl')
scaler = joblib.load('scaler.pkl')
imputer = joblib.load('imputer.pkl')

# Function to initialize daily goals
def initialize_daily_goals(bmi=None, fitness_level=None, health_issues=None, veg_preference=None, weight_goal=None):
    # Base goals
    daily_goals = {
        'calories': 2000,
        'protein': 50,
        'carbs': 275,
        'fat': 70,
        'fiber': 30,
        'sodium': 2300,
        'potassium': 3500
    }
    
    # Adjustments based on BMI
    if bmi:
        if bmi < 18.5:
            daily_goals['calories'] *= 1.15
            daily_goals['protein'] *= 1.15
        elif 25 <= bmi < 30:
            daily_goals['calories'] *= 0.9
            daily_goals['protein'] *= 1.1
        elif bmi >= 30:
            daily_goals['calories'] *= 0.85
            daily_goals['fat'] *= 0.9
            daily_goals['fiber'] *= 1.1
    
    # Adjustments based on fitness level
    if fitness_level:
        if fitness_level == 'sedentary':
            daily_goals['calories'] *= 0.95
            daily_goals['fiber'] *= 1.05
        elif fitness_level == 'highly active':
            daily_goals['calories'] *= 1.1
            daily_goals['carbs'] *= 1.1
    
    # Adjustments based on health issues
    if health_issues:
        if 'diabetes' in health_issues:
            daily_goals['carbs'] *= 0.85
            daily_goals['fiber'] *= 1.15
        if 'heart disease' in health_issues:
            daily_goals['fat'] *= 0.9
            daily_goals['saturated_fat'] = daily_goals.get('saturated_fat', 0) * 0.8  # Assuming this is tracked
            daily_goals['polyunsaturated_fats'] = daily_goals.get('polyunsaturated_fats', 0) * 1.1
        if 'hypertension' in health_issues:
            daily_goals['sodium'] *= 0.8
            daily_goals['potassium'] *= 1.1
    
    # Adjustments based on weight goal
    if weight_goal == 'gain':
        for key in daily_goals:
            daily_goals[key] *= 1.1
    elif weight_goal == 'lose':
        for key in daily_goals:
            daily_goals[key] *= 0.9
    
    return daily_goals

# Function to select a meal and update the remaining goals
def select_meal(meal_type, remaining_goals, available_foods, min_calories, max_calories=None):
    if max_calories:
        meal_options = available_foods[(available_foods['predicted_meal_type'] == meal_type) & 
                                       (available_foods['Caloric Value'] >= min_calories) & 
                                       (available_foods['Caloric Value'] <= max_calories)]
    else:
        meal_options = available_foods[(available_foods['predicted_meal_type'] == meal_type) & 
                                       (available_foods['Caloric Value'] >= min_calories)]
    
    if meal_options.empty:
        return pd.DataFrame(), available_foods
    
    # Add randomness to meal selection
    meal_options = meal_options.sample(frac=1).reset_index(drop=True)  # Shuffle
    
    # Calculate scores
    meal_options['score'] = (
        (meal_options['Caloric Value'] / remaining_goals['calories']).abs() +
        (meal_options['Protein'] / remaining_goals['protein']).abs() +
        (meal_options['Carbohydrates'] / remaining_goals['carbs']).abs() +
        (meal_options['Fat'] / remaining_goals['fat']).abs() +
        (meal_options['Dietary Fiber'] / remaining_goals['fiber']).abs() +
        (meal_options['Sodium'] / remaining_goals['sodium']).abs() +
        (meal_options['Potassium'] / remaining_goals['potassium']).abs()
    )
    
    selected_meal = meal_options.sort_values(by='score').iloc[0]
    
    # Update remaining goals based on the selected meal
    remaining_goals['calories'] -= selected_meal['Caloric Value']
    remaining_goals['protein'] -= selected_meal['Protein']
    remaining_goals['carbs'] -= selected_meal['Carbohydrates']
    remaining_goals['fat'] -= selected_meal['Fat']
    remaining_goals['fiber'] -= selected_meal['Dietary Fiber']
    remaining_goals['sodium'] -= selected_meal['Sodium']
    remaining_goals['potassium'] -= selected_meal['Potassium']
    
    selected_meal = selected_meal.to_frame().T
    selected_meal['meal_type'] = meal_type
    
    # Remove the selected meal from the available options to avoid repetition
    available_foods = available_foods[available_foods['food'] != selected_meal['food'].values[0]]
    
    return selected_meal, available_foods

# Function to generate a daily diet plan
def generate_diet_plan_ml(model, scaler, imputer, df, restrictions=None, health_issues=None, bmi=None, fitness_level=None, veg_preference=None, weight_goal=None):
    # Initialize daily goals
    daily_goals = initialize_daily_goals(bmi, fitness_level, health_issues, veg_preference, weight_goal)
    remaining_goals = daily_goals.copy()
    diet_plan = pd.DataFrame()
    
    # Apply dietary restrictions and preferences
    if restrictions:
        df = df[~df['food'].isin(restrictions)]
    if veg_preference is not None:
        df = df[df['veg_category'] == veg_preference]
    
    # Predict meal types for all food items
    features = df[['Caloric Value', 'Fat', 'Saturated Fats', 'Monounsaturated Fats', 
                   'Polyunsaturated Fats', 'Carbohydrates', 'Sugars', 'Protein', 
                   'Dietary Fiber', 'Cholesterol', 'Sodium', 'Water', 'Vitamin A', 
                   'Vitamin B1', 'Vitamin B11', 'Vitamin B12', 'Vitamin B2', 
                   'Vitamin B3', 'Vitamin B5', 'Vitamin B6', 'Vitamin C', 
                   'Vitamin D', 'Vitamin E', 'Vitamin K', 'Calcium', 'Copper', 
                   'Iron', 'Magnesium', 'Manganese', 'Phosphorus', 'Potassium', 
                   'Selenium', 'Zinc', 'Nutrition Density']]
    
    # Handle missing values
    features_imputed = imputer.transform(features)
    df_scaled = scaler.transform(features_imputed)
    
    df['predicted_meal_type'] = model.predict(df_scaled)
    
    # Copy available foods to a new DataFrame
    available_foods = df.copy()
    
    # Minimum and maximum calorie requirements
    min_calories = {
        'breakfast': 269,
        'lunch': 500,
        'dinner': 500,
        'snack': 70
    }
    max_calories = {
        'snack': 120
    }
    
    # Select exactly one breakfast, lunch, and dinner
    for meal in ['breakfast', 'lunch', 'dinner']:
        meal_plan, available_foods = select_meal(meal, remaining_goals, available_foods, min_calories[meal])
        diet_plan = pd.concat([diet_plan, meal_plan], ignore_index=True)
    
    # Select up to 6 snacks until nutritional goals are met
    snack_count = 0
    while remaining_goals['calories'] > 0 and snack_count < 6:
        snack, available_foods = select_meal('snack', remaining_goals, available_foods, min_calories['snack'], max_calories['snack'])
        if snack.empty:  # Break if no more snacks are available
            break
        diet_plan = pd.concat([diet_plan, snack], ignore_index=True)
        snack_count += 1
    
    # Ensure food variety and servings are met
    # Example: Check for fruit and vegetable inclusion
    fruit_veg_count = diet_plan['food'].apply(lambda x: 'fruit' in x or 'vegetable' in x).sum()
    if fruit_veg_count < 5:
        additional_fruit_veg = df[(df['food'].str.contains('fruit') | df['food'].str.contains('vegetable')) & (df['predicted_meal_type'] == 'snack')]
        for _, row in additional_fruit_veg.iterrows():
            if fruit_veg_count >= 5:
                break
            if snack_count >= 6:
                break
            diet_plan = pd.concat([diet_plan, row.to_frame().T], ignore_index=True)
            fruit_veg_count += 1
            snack_count += 1
    
    # Ensure sufficient proteins and whole grains
    proteins_needed = 2 - diet_plan['food'].apply(lambda x: 'protein' in x).sum()
    grains_needed = 6 - diet_plan['food'].apply(lambda x: 'grain' in x).sum()
    
    if proteins_needed > 0:
        additional_proteins = df[(df['food'].str.contains('protein')) & (df['predicted_meal_type'] == 'snack')]
        for _, row in additional_proteins.iterrows():
            if proteins_needed <= 0:
                break
            if snack_count >= 6:
                break
            diet_plan = pd.concat([diet_plan, row.to_frame().T], ignore_index=True)
            proteins_needed -= 1
            snack_count += 1
    
    if grains_needed > 0:
        additional_grains = df[(df['food'].str.contains('grain')) & (df['predicted_meal_type'] == 'snack')]
        for _, row in additional_grains.iterrows():
            if grains_needed <= 0:
                break
            if snack_count >= 6:
                break
            diet_plan = pd.concat([diet_plan, row.to_frame().T], ignore_index=True)
            grains_needed -= 1
            snack_count += 1
    
    diet_plan = diet_plan[['food', 'Caloric Value', 'Protein', 'Fat', 'Sugars', 'meal_type', 'veg_category']]
    return diet_plan
