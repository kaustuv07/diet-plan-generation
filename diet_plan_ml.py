import pandas as pd

# Load the pre-trained model and other necessary objects
import joblib
classifier = joblib.load('classifier.pkl')
scaler = joblib.load('scaler.pkl')
imputer = joblib.load('imputer.pkl')

# The function to generate a daily diet plan
def generate_diet_plan_ml(model, scaler, imputer, df, daily_goals):
    remaining_goals = daily_goals.copy()
    diet_plan = pd.DataFrame()
    
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
    
    # Helper function to select foods
    def select_meal(meal_type, remaining_goals):
        meal_options = df[df['predicted_meal_type'] == meal_type]
        if meal_options.empty:
            return pd.DataFrame()
        selected_meal = meal_options.sample()
        remaining_goals['calories'] -= selected_meal['Caloric Value'].values[0]
        remaining_goals['protein'] -= selected_meal['Protein'].values[0]
        remaining_goals['carbs'] -= selected_meal['Carbohydrates'].values[0]
        remaining_goals['fat'] -= selected_meal['Fat'].values[0]
        selected_meal['meal_type'] = meal_type
        return selected_meal
    
    # Select foods for each meal type
    for meal in ['breakfast', 'lunch', 'dinner']:
        meal_plan = select_meal(meal, remaining_goals)
        diet_plan = pd.concat([diet_plan, meal_plan], ignore_index=True)
    
    # Select snacks until nutritional goals are met
    while remaining_goals['calories'] > 0 and not df[df['predicted_meal_type'] == 'snack'].empty:
        snack = select_meal('snack', remaining_goals)
        if snack.empty:  # Break if no more snacks are available
            break
        diet_plan = pd.concat([diet_plan, snack], ignore_index=True)

    return diet_plan
