import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

DATA_PATH = os.path.join("data", "student_exam_data.csv")

def main():
    df = pd.read_csv(DATA_PATH)
    print(f"[INFO] Loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns")

    features = ["daily_study_hours", "daily_screen_hours", "study_consistency_days", "past_exam_avg", "syllabus_mastery_pct", "sleep_hours", "practice_tests_completed"]
    X = df[features]
    y = df["final_exam_score"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    models = {
        "Linear Regression": LinearRegression(),
        "Ridge Regression": Ridge(alpha=1.0),
        "Random Forest Regressor": RandomForestRegressor(n_estimators=100, max_depth=6, random_state=42),
    }

    print("\n=======================================================")
    print("      EXAM SCORE PREDICTION - MODEL BENCHMARKS         ")
    print("=======================================================")

    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        r2 = r2_score(y_test, preds)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        mae = mean_absolute_error(y_test, preds)
        results[name] = {"R2_Score": round(r2, 4), "RMSE": round(rmse, 4), "MAE": round(mae, 4)}
        print(f"{name:25s} | R2: {r2:.4f} | RMSE: {rmse:.4f} | MAE: {mae:.4f}")

    print("=======================================================\n")

if __name__ == "__main__":
    main()
