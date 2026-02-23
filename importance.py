import pandas as pd
import joblib
import matplotlib.pyplot as plt

# --- CONFIGURATION ---
MODEL_FILE = "fifo_area_predictor.pkl"
FEATURES = ["Width (Bits)", "Depth (Words)"]

def show_importance():
    print("--- CALCULATING FEATURE IMPORTANCE ---")
    
    try:
        model = joblib.load(MODEL_FILE)
    except:
        print("❌ Model not found.")
        return

    # Get the "Importance Score" (0 to 1)
    importance = model.feature_importances_
    
    print(f"Width Importance: {importance[0]:.4f}")
    print(f"Depth Importance: {importance[1]:.4f}")

    # Plot
    plt.figure(figsize=(8, 5))
    bars = plt.bar(FEATURES, importance, color=['#1f77b4', '#ff7f0e'])
    
    plt.title("What drives the Hardware Cost?", fontsize=14)
    plt.ylabel("Importance Score (0-1)", fontsize=12)
    plt.ylim(0, 1.1)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    
    # Add numbers on top of bars
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.02, f"{yval:.2f}", ha='center', fontsize=12, fontweight='bold')

    print("Opening Graph...")
    plt.show()

if __name__ == "__main__":
    show_importance()
