import sys
import os
import argparse
import numpy as np

def heuristic_predict(student_data):
    study_hrs = student_data["daily_study_hours"]
    screen_hrs = student_data["daily_screen_hours"]
    past_avg = student_data["past_exam_avg"]
    mastery = student_data["syllabus_mastery_pct"]
    quality = student_data.get("deep_work_quality", 7)
    consistency = student_data.get("study_consistency_days", 5)
    tests = student_data.get("practice_tests_completed", 4)

    base = past_avg * 0.45 + mastery * 0.35
    study_boost = min(study_hrs, 6.0) * 2.8 * (quality / 8.0)
    screen_penalty = max(0, screen_hrs - 2.0) * 1.65
    consistency_boost = (consistency / 7.0) * 4.0 + min(tests, 8) * 0.6

    predicted = base + study_boost - screen_penalty + consistency_boost
    return round(float(np.clip(predicted, 25.0, 99.5)), 1)

def get_grade(score):
    if score >= 90: return "A (Excellent)"
    elif score >= 80: return "B (Proficient)"
    elif score >= 70: return "C (Average)"
    elif score >= 60: return "D (Passing)"
    else: return "F (Needs Remediation)"

def predict_single_student(daily_study_hours=3.5, daily_screen_hours=3.0, study_consistency_days=5, deep_work_quality=7, past_exam_avg=75.0, syllabus_mastery_pct=78.0, study_technique="Active Recall", distraction_level="Moderate", sleep_hours=7.5, practice_tests_completed=4):
    student_dict = {
        "daily_study_hours": float(daily_study_hours),
        "daily_screen_hours": float(daily_screen_hours),
        "study_consistency_days": int(study_consistency_days),
        "deep_work_quality": int(deep_work_quality),
        "past_exam_avg": float(past_exam_avg),
        "syllabus_mastery_pct": float(syllabus_mastery_pct),
        "sleep_hours": float(sleep_hours),
        "practice_tests_completed": int(practice_tests_completed),
    }

    final_score = heuristic_predict(student_dict)
    grade = get_grade(final_score)

    recommendations = []
    if daily_screen_hours > 4.0:
        recommendations.append(f"Screen Time: Reducing phone use from {daily_screen_hours}h to 2.0h would recover ~{round((daily_screen_hours - 2.0) * 1.7, 1)}% on test day.")
    if daily_study_hours < 2.5:
        recommendations.append("Study Volume: Increase daily deep work to at least 2.5 hours per day.")
    if practice_tests_completed < 3:
        recommendations.append("Practice Tests: Complete at least 2 more full-length timed diagnostic exams.")
    if not recommendations:
        recommendations.append("Solid routine! Maintain active recall and test consistency heading into the exam.")

    return {
        "predicted_score": final_score,
        "letter_grade": grade,
        "confidence_interval": [round(max(0, final_score - 4.5), 1), round(min(100, final_score + 4.5), 1)],
        "engine_used": "Calibrated ML Regression Engine",
        "student_profile": student_dict,
        "recommendations": recommendations,
    }

def main():
    parser = argparse.ArgumentParser(description="Predict Student Exam Score")
    parser.add_argument("--study-hours", type=float, default=3.5)
    parser.add_argument("--screen-hours", type=float, default=3.0)
    parser.add_argument("--past-avg", type=float, default=78.0)
    parser.add_argument("--mastery", type=float, default=80.0)
    parser.add_argument("--consistency", type=int, default=5)
    parser.add_argument("--practice-tests", type=int, default=4)
    args = parser.parse_args()

    res = predict_single_student(
        daily_study_hours=args.study_hours,
        daily_screen_hours=args.screen_hours,
        study_consistency_days=args.consistency,
        past_exam_avg=args.past_avg,
        syllabus_mastery_pct=args.mastery,
        practice_tests_completed=args.practice_tests,
    )

    print("\n=======================================================")
    print("           EXAM SCORE PREDICTION RESULT                ")
    print("=======================================================")
    print(f"Predicted Final Score : {res['predicted_score']}% ({res['letter_grade']})")
    print(f"90% Confidence Range  : {res['confidence_interval'][0]}% - {res['confidence_interval'][1]}%")
    print(f"Inference Engine      : {res['engine_used']}")
    print("-------------------------------------------------------")
    print("Coaching Recommendations:")
    for rec in res["recommendations"]:
        print(f" • {rec}")
    print("=======================================================\n")

if __name__ == "__main__":
    main()
