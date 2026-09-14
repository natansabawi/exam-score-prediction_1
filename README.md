# Intelligent Student Exam Performance Prediction and Early Intervention System

A machine learning pipeline that predicts exam outcomes from academic and behavioral factors.

## Project Structure
```text
exam-score-prediction/
├── data/
│   └── StudentPerformanceFactors.csv
├── notebooks/
│   └── exam_score_prediction.ipynb
├── models/
│   └── exam_score_prediction_pipeline.joblib
├── app/
│   └── app.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Performance Summary
- 5-Fold Cross-Validation R²: 0.7156
- Model: Linear Regression with Scikit-Learn Preprocessing Pipeline

## How to Run the App
1. `pip install -r requirements.txt`
2. `streamlit run app/app.py`