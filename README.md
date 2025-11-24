# 🥗 Diet Prediction System

A smart AI-powered Diet Prediction System that calculates your daily calorie needs and generates a personalized meal plan based on your health metrics and goals.

## 🚀 Features
- **Smart Health Calculation**: Automatically calculates BMI, BMR (Mifflin-St Jeor), and TDEE.
- **AI Calorie Prediction**: Uses a Random Forest Machine Learning model to predict optimal calorie intake.
- **Personalized Diet Plans**: Generates breakfast, lunch, dinner, and snack recommendations based on your preferences (Veg/Non-Veg).
- **Premium UI**: Beautiful, modern Glassmorphism design that is fully responsive.
- **Goal Oriented**: Supports Weight Loss, Maintenance, and Weight Gain goals.

## 🛠️ Tech Stack
- **Backend**: Python, Flask
- **Machine Learning**: Scikit-learn, Pandas, NumPy
- **Frontend**: HTML5, CSS3 (Glassmorphism), JavaScript
- **Data**: Custom Food Dataset

## 📦 Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/DeepakdevilB/Diet_Prediction_System.git
   cd Diet_Prediction_System
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**
   ```bash
   python app.py
   ```

4. **Access the App**
   Open your browser and visit: `http://127.0.0.1:5000`

## 🧠 How It Works
1. **Input Data**: Enter your age, gender, height, weight, activity level, and goal.
2. **Processing**: 
   - The system calculates your BMI and BMR.
   - The ML model predicts your exact daily calorie requirement.
3. **Output**: You get a dashboard with your health stats and a detailed 7-day diet plan (conceptually, currently shows a daily breakdown).

## 📂 Project Structure
```
DietPredictionSystem/
├── app.py                 # Main Flask Application
├── model.py               # ML Model Training & Prediction
├── diet_engine.py         # Core Logic (Calculators, Diet Generation)
├── data/
│   └── food_data.csv      # Food Database
├── static/                # CSS, JS, Images
└── templates/             # HTML Templates
```

## 🤝 Contributing
Feel free to fork this repository and submit pull requests!

## 📄 License
This project is open source and available under the [MIT License](LICENSE).
