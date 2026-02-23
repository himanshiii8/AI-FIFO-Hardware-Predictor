import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# --- CONFIGURATION ---
DATA_FILE = "dataset_clean.csv"
MODEL_FILE = "fifo_area_predictor.pkl"

def train_and_test():
    print(f"--- TRAINING AI MODEL (Random Forest) ---")
    
    # 1. Load Data
    try:
        df = pd.read_csv(DATA_FILE)
    except:
        print(" Error: Could not find dataset_clean.csv.")
        return

    # 2. Split Data (The 'Train-Test Split' Concept)
    # X = The questions (Width, Depth)
    # y = The answers (Area)
    X = df[['Width', 'Depth']]
    y = df['Area']
    
    # We hide 20% of data to test the AI later
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print(f"Training on {len(X_train)} samples...")
    print(f"Testing on {len(X_test)} samples (The 'Exam')...")

    # 3. Train the Brain (The 'Ensemble' Concept)
    # n_estimators=100 means we create 100 Decision Trees
    print("Building Random Forest...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    print("Model Trained!")

    # 4. Evaluate (The 'R2 Score' Concept)
    predictions = model.predict(X_test)
    
    # Accuracy Score (1.0 = Perfect, 0.0 = Fail)
    accuracy = r2_score(y_test, predictions) * 100
    avg_error = mean_absolute_error(y_test, predictions)
    
    print("-" * 30)
    print(f" ACCURACY SCORE (R2): {accuracy:.2f}%")
    print(f"Average Error (MAE): +/- {int(avg_error)} cells")
    print("-" * 30)
    
    # 5. Save the Brain
    joblib.dump(model, MODEL_FILE)
    print(f" AI Model saved to: {MODEL_FILE}")

    # 6. Interactive Mode
    print("\n--- TEST IT YOURSELF (Type 'exit' to stop) ---")
    while True:
        try:
            user_input = input("\nEnter Width,Depth (e.g. 32,512): ")
            if user_input.lower() == 'exit': break
            
            parts = user_input.split(',')
            w = int(parts[0])
            d = int(parts[1])
            
            # Predict
            pred_area = model.predict([[w, d]])[0]
            print(f" AI Prediction: {int(pred_area)} Logic Cells")
            
        except Exception:
            print("Invalid format. Try: 32,512")

if __name__ == "__main__":
    train_and_test()
