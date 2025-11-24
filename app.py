from flask import Flask, render_template, request
from model import CaloriePredictor
from diet_engine import Calculator, DietRecommender
import os

app = Flask(__name__)

# Initialize model and diet engine
predictor = CaloriePredictor()
# Ensure model is trained/loaded
if not os.path.exists('model.pkl'):
    predictor.train()
else:
    predictor.load()

recommender = DietRecommender()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            # Get form data
            age = int(request.form['age'])
            gender = request.form['gender']
            height = float(request.form['height'])
            weight = float(request.form['weight'])
            activity = request.form['activity']
            goal = request.form['goal']
            preference = request.form['preference']

            # 1. Calculate BMI & Category
            bmi = Calculator.calculate_bmi(weight, height)
            bmi_category = Calculator.get_bmi_category(bmi)

            # 2. Calculate BMR & TDEE (Formula)
            bmr = Calculator.calculate_bmr(weight, height, age, gender)
            tdee_formula = Calculator.calculate_tdee(bmr, activity)

            # 3. Predict Calories using ML Model
            predicted_calories = predictor.predict(age, gender, height, weight, activity)
            
            # Adjust for Goal
            # Weight Loss: -500, Gain: +500, Maintain: +0
            goal_adjustment = 0
            if goal == 'loss':
                goal_adjustment = -500
            elif goal == 'gain':
                goal_adjustment = 500
            
            final_calories = int(predicted_calories + goal_adjustment)
            
            # Safety check: Don't go below 1200
            if final_calories < 1200:
                final_calories = 1200

            # 4. Generate Diet Plan
            diet_plan = recommender.recommend_diet(final_calories, preference)

            return render_template('result.html', 
                                   bmi=bmi, 
                                   bmi_category=bmi_category,
                                   calories=final_calories,
                                   diet_plan=diet_plan,
                                   tdee=int(tdee_formula),
                                   goal=goal.capitalize())

        except Exception as e:
            return render_template('index.html', error=str(e))

if __name__ == '__main__':
    app.run(debug=True)
