import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

class CaloriePredictor:
    def __init__(self, model_path='model.pkl'):
        self.model_path = model_path
        self.model = None

    def generate_synthetic_data(self, n_samples=1000):
        """
        Generates synthetic data for training.
        Features: Age, Gender (0:F, 1:M), Height, Weight, Activity Level (0-4)
        Target: Calories
        """
        np.random.seed(42)
        
        ages = np.random.randint(18, 80, n_samples)
        genders = np.random.randint(0, 2, n_samples) # 0: Female, 1: Male
        heights = np.random.normal(170, 10, n_samples) # cm
        weights = np.random.normal(70, 15, n_samples) # kg
        activity_levels = np.random.randint(0, 5, n_samples) # 0 to 4
        
        # Calculate BMR and TDEE for "ground truth" with some noise
        calories = []
        for i in range(n_samples):
            # Mifflin-St Jeor
            if genders[i] == 1: # Male
                bmr = (10 * weights[i]) + (6.25 * heights[i]) - (5 * ages[i]) + 5
            else: # Female
                bmr = (10 * weights[i]) + (6.25 * heights[i]) - (5 * ages[i]) - 161
            
            multipliers = [1.2, 1.375, 1.55, 1.725, 1.9]
            tdee = bmr * multipliers[activity_levels[i]]
            
            # Add some random noise to make it "realistic" / require ML
            noise = np.random.normal(0, 50) 
            calories.append(tdee + noise)
            
        data = pd.DataFrame({
            'Age': ages,
            'Gender': genders,
            'Height': heights,
            'Weight': weights,
            'Activity': activity_levels,
            'Calories': calories
        })
        
        return data

    def train(self):
        print("Generating synthetic data...")
        data = self.generate_synthetic_data()
        
        X = data[['Age', 'Gender', 'Height', 'Weight', 'Activity']]
        y = data['Calories']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        print("Training Random Forest Regressor...")
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        score = self.model.score(X_test, y_test)
        print(f"Model R^2 Score: {score:.4f}")
        
        try:
            joblib.dump(self.model, self.model_path)
            print(f"Model saved to {self.model_path}")
        except (OSError, IOError) as e:
            print(f"Could not save model (likely read-only filesystem): {e}")
            # Continue without saving - model is still in memory


    def load(self):
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
        else:
            print("Model not found. Training new model...")
            self.train()

    def predict(self, age, gender, height, weight, activity_level):
        if self.model is None:
            self.load()
        
        # Gender: Male=1, Female=0
        gender_val = 1 if gender.lower() == 'male' else 0
        
        # Activity map
        activity_map = {
            'sedentary': 0,
            'lightly_active': 1,
            'moderately_active': 2,
            'very_active': 3,
            'extra_active': 4
        }
        act_val = activity_map.get(activity_level.lower(), 0)
        
        input_data = pd.DataFrame([[age, gender_val, height, weight, act_val]], 
                                  columns=['Age', 'Gender', 'Height', 'Weight', 'Activity'])
        
        return self.model.predict(input_data)[0]

if __name__ == "__main__":
    predictor = CaloriePredictor()
    predictor.train()
