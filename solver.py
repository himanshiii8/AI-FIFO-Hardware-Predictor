import pandas as pd
import joblib
import numpy as np

# --- CONFIGURATION ---
MODEL_FILE = "fifo_area_predictor.pkl"

def reverse_solver():
    print("--- DESIGN EXPLORER (REVERSE SOLVER) ---")
    
    # 1. Load the AI Brain
    try:
        model = joblib.load(MODEL_FILE)
        print(" AI Brain Loaded successfully!")
    except:
        print("❌ Error: Model file not found. Run Step 2 first.")
        return

    print("\nThis tool finds the best FIFO configuration for your Area Budget.")
    
    while True:
        try:
            user_input = input("\nEnter Max Area Budget (or 'exit'): ")
            if user_input.lower() == 'exit': break
            
            budget = int(user_input)
            
            print(f" Scanning for designs under {budget} cells...")
            
            # 2. The Smart Search
            # Instead of guessing, we generate a grid of "Valid Options"
            # We scan typical Widths (8 to 128) and Depths (2 to 1024)
            possible_widths = np.arange(8, 129, 8)   # 8, 16, 24... 128
            possible_depths = [16, 32, 64, 128, 256, 512, 1024] # Powers of 2
            
            best_design = None
            max_capacity = 0 # We want to maximize (Width * Depth)
            
            # Create a list of all candidates to ask the AI
            candidates = []
            for w in possible_widths:
                for d in possible_depths:
                    candidates.append([w, d])
            
            # Ask the AI to predict Area for ALL candidates at once
            predictions = model.predict(candidates)
            
            # Find the winner
            found_any = False
            for i, area in enumerate(predictions):
                w = candidates[i][0]
                d = candidates[i][1]
                
                # Check if it fits in budget
                if area <= budget:
                    found_any = True
                    capacity = w * d # Total bits stored
                    
                    # We pick the one that stores the MOST bits
                    if capacity > max_capacity:
                        max_capacity = capacity
                        best_design = (w, d, area)

            # 3. Report the Winner
            if found_any:
                w, d, a = best_design
                print("-" * 30)
                print(f" BEST DESIGN FOUND:")
                print(f"   Width: {w} bits")
                print(f"   Depth: {d} words")
                print(f"   Predicted Area: {int(a)} cells")
                print(f"   (This uses {int((a/budget)*100)}% of your budget)")
                print("-" * 30)
            else:
                print("⚠️ No design fits this tiny budget! Try increasing it.")

        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    reverse_solver()
