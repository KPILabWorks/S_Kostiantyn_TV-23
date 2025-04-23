import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

MODEL_PATH = 'diabetes_model.pkl'

def train_model():
    data = pd.read_csv('diabetic.csv')

    X = data.drop('Outcome', axis=1)
    y = data['Outcome']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Точність моделі на тестових даних: {accuracy * 100:.2f}%")

    joblib.dump(model, MODEL_PATH)
    print(f"Модель збережено як '{MODEL_PATH}'")


def get_or_train_model():
    if os.path.exists(MODEL_PATH):
        print("Модель знайдена. Завантажується...")
        return joblib.load(MODEL_PATH)
    else:
        print("Модель не знайдена. Тренування нової моделі...")
        train_model()
        return joblib.load(MODEL_PATH)


def predict_user_data(user_input):
    model = get_or_train_model()

    columns = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness',
               'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age']

    input_df = pd.DataFrame([user_input], columns=columns)
    prediction = model.predict(input_df)

    result = "Має ймовірність діабету" if prediction[0] == 1 else "Немає ймовірності діабету"
    return result


example_inputs = [
    [5, 140, 85, 28, 100, 31.2, 0.45, 45],  # підвищена глюкоза, нормальний тиск
    [0, 95, 60, 20, 0, 22.5, 0.2, 23],      # молодий, низький ризик
    [10, 180, 90, 35, 200, 40.5, 0.8, 55],  # вік, глюкоза, інсулін
    [3, 130, 70, 15, 85, 27.0, 0.3, 35],    # все в нормі
    [7, 160, 100, 32, 150, 37.8, 1.2, 50]   # високий тиск, BMI, спадковість
]

for i, inp in enumerate(example_inputs, start=1):
    result = predict_user_data(inp)
    print(f"Приклад {i}: {result}")


