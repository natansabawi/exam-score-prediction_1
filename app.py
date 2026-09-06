import streamlit as st
import numpy as np
from predict_student import predict_single_student

st.set_page_config(page_title='ExamPredict ML', page_icon='🎓', layout='wide')
st.title('🎓 ExamPredict • ML Exam Score Predictor & Coach')
st.write('Predictive score modeling, phone distraction friction, and study habit analysis.')

col_in, col_res = st.columns([1, 1])

with col_in:
    st.subheader('Student Habit Inputs')
    study_hours = st.slider('Daily Study Hours', 0.5, 8.0, 3.5, 0.5)
    screen_hours = st.slider('Daily Recreational Screen Time (Hours)', 0.5, 9.0, 3.0, 0.5)
    past_avg = st.slider('Past Exams / Quizzes Average (%)', 40, 100, 78)
    mastery = st.slider('Syllabus Mastery (%)', 30, 100, 80)
    consistency = st.slider('Study Days per Week', 1, 7, 5)

pred = predict_single_student(
    daily_study_hours=study_hours,
    daily_screen_hours=screen_hours,
    study_consistency_days=consistency,
    past_exam_avg=past_avg,
    syllabus_mastery_pct=mastery
)

with col_res:
    st.subheader('Prediction Results')
    st.metric('Predicted Exam Score', f'{pred[\"predicted_score\"]}%')
    st.metric('Predicted Grade', pred['letter_grade'])
    st.write(f'**90% Confidence Interval:** {pred[\"confidence_interval\"][0]}% - {pred[\"confidence_interval\"][1]}%')
    
    st.subheader('💡 Coaching Advice')
    for rec in pred['recommendations']:
        st.info(rec)
