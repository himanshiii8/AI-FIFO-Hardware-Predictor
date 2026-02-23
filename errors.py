import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split

# --- CONFIGURATION ---
DATA_FILE = "dataset_clean.csv"
MODEL_FILE = "fifo_area_predictor.pkl"

def analyze_errors():
    print("--- GENERATING ERROR DISTRIBUTION GRAPH ---")
    
    # 1. Load Data and Model
    try:
        df = pd.read_csv(DATA_FILE)
        model = joblib.load(MODEL_FILE)
    except:
        print("❌ Error: Missing data or model file.")
        return

    # 2. Prepare the "Exam" (Test Set)
    # We must use the Test set (unseen data) to be honest
    X = df[['Width', 'Depth']]
    y = df['Area']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 3. Predict
    predictions = model.predict(X_test)
    
    # 4. Calculate Residuals (The "Mistakes")
    # Error = Real Value - Predicted Value
    errors = y_test - predictions
    
    # 5. The Statistics (for your paper text)
    mean_error = errors.mean()
    std_dev = errors.std()
    
    print("\nSTATS FOR PAPER:")
    print(f"   Mean Error (Bias): {mean_error:.2f} cells (Should be close to 0)")
    print(f"   Standard Deviation: {std_dev:.2f} cells")
    print("-" * 30)

    # 6. The Graph (Histogram + Bell Curve)
    plt.figure(figsize=(10, 6))
    
    # Create a Histogram with a Kernel Density Estimate (KDE) curve
    sns.histplot(errors, kde=True, bins=30, color='purple', alpha=0.6)
    
    # Add a vertical line at 0 (The Perfect Prediction line)
    plt.axvline(x=0, color='black', linestyle='--', label='Perfect Prediction')
    
    plt.title("Error Distribution Analysis (Residuals)")
    plt.xlabel("Prediction Error (Logic Cells)")
    plt.ylabel("Number of Samples")
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    print("Opening Graph... Check the popup window.")
    plt.show()

if __name__ == "__main__":
    analyze_errors()
