import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error

# --- CONFIGURATION ---
DATA_FILE = "dataset_clean.csv"

def compare_models():
    print(f"--- THE SHOWDOWN: LINEAR vs. RANDOM FOREST ---")
    
    # 1. Load Data
    try:
        df = pd.read_csv(DATA_FILE)
    except:
        print("❌ Error: Could not find dataset_clean.csv")
        return

    X = df[['Width', 'Depth']]
    y = df['Area']
    
    # Split Data (Same for both models)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 2. Train Model A: Linear Regression (The "Old School" way)
    print("Training Linear Regression...")
    linear_model = LinearRegression()
    linear_model.fit(X_train, y_train)
    y_pred_linear = linear_model.predict(X_test)
    
    # 3. Train Model B: Random Forest (The "AI" way)
    print("Training Random Forest...")
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    
    # 4. Compare Scores
    acc_linear = r2_score(y_test, y_pred_linear) * 100
    err_linear = mean_absolute_error(y_test, y_pred_linear)
    
    acc_rf = r2_score(y_test, y_pred_rf) * 100
    err_rf = mean_absolute_error(y_test, y_pred_rf)
    
    print("\n" + "="*40)
    print("    FINAL RESULTS ")
    print("="*40)
    
    print(f" Model A (Linear Regression):")
    print(f"   Accuracy: {acc_linear:.2f}%")
    print(f"   Avg Error: +/- {int(err_linear)} cells")
    
    
    print(f"\n Model B (Random Forest):")
    print(f"   Accuracy: {acc_rf:.2f}%")
    print(f"   Avg Error: +/- {int(err_rf)} cells")
    
    print("="*40)

    # 5. Visualization of the Fight
    # We will pick 50 random test samples and show how close each model got
    plt.figure(figsize=(10, 6))
    plt.plot(y_test.values[:50], label='Real Truth', marker='o', color='black')
    plt.plot(y_pred_linear[:50], label='Linear Prediction', linestyle='--', color='red')
    plt.plot(y_pred_rf[:50], label='Random Forest Prediction', linestyle='-', color='green')
    
    plt.title("Model Comparison: First 50 Test Samples")
    plt.ylabel("Area (Logic Cells)")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    compare_models()
