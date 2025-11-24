import pandas as pd
import random

class Calculator:
    @staticmethod
    def calculate_bmi(weight, height):
        """
        Calculate BMI.
        Weight in kg, Height in cm.
        """
        try:
            height_m = height / 100
            bmi = weight / (height_m ** 2)
            return round(bmi, 2)
        except ZeroDivisionError:
            return 0

    @staticmethod
    def get_bmi_category(bmi):
        if bmi < 18.5:
            return "Underweight"
        elif 18.5 <= bmi < 24.9:
            return "Normal weight"
        elif 25 <= bmi < 29.9:
            return "Overweight"
        else:
            return "Obesity"

    @staticmethod
    def calculate_bmr(weight, height, age, gender):
        """
        Calculate BMR using Mifflin-St Jeor Equation.
        """
        if gender.lower() == 'male':
            bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
        else:
            bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
        return round(bmr, 2)

    @staticmethod
    def calculate_tdee(bmr, activity_level):
        """
        Calculate TDEE based on activity level.
        """
        activity_multipliers = {
            'sedentary': 1.2,
            'lightly_active': 1.375,
            'moderately_active': 1.55,
            'very_active': 1.725,
            'extra_active': 1.9
        }
        multiplier = activity_multipliers.get(activity_level.lower(), 1.2)
        return round(bmr * multiplier, 2)

class DietRecommender:
    def __init__(self, food_data_path='data/food_data.csv'):
        try:
            self.food_data = pd.read_csv(food_data_path)
        except FileNotFoundError:
            self.food_data = pd.DataFrame(columns=['Food', 'Type', 'Calories', 'Protein', 'Carbs', 'Fat', 'Meal'])

    def recommend_diet(self, calories, preference='veg'):
        """
        Generate a simple diet plan based on calorie needs and preference.
        """
        # Filter by preference
        if preference.lower() == 'veg':
            df = self.food_data[self.food_data['Type'] == 'Veg']
        elif preference.lower() == 'non-veg':
            df = self.food_data # Non-veg eats everything usually, or filter specifically if needed
        else:
            df = self.food_data

        if df.empty:
            return {}

        # Simple distribution: 25% Breakfast, 35% Lunch, 10% Snack, 30% Dinner
        targets = {
            'Breakfast': calories * 0.25,
            'Lunch': calories * 0.35,
            'Snacks': calories * 0.10,
            'Dinner': calories * 0.30
        }

        plan = {}
        for meal, target_cal in targets.items():
            meal_options = df[df['Meal'] == meal]
            if meal_options.empty:
                 # Fallback to any food if specific meal type not found
                 meal_options = df
            
            # Simple logic: pick random items that sum up close to target
            # For this MVP, we just pick one or two items to show the concept
            if not meal_options.empty:
                selected = meal_options.sample(n=min(len(meal_options), 2))
                plan[meal] = selected.to_dict('records')
            else:
                plan[meal] = []
        
        return plan
