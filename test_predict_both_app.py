import streamlit as st
import pandas as pd
import pickle
import numpy as np

# --- Load Artifacts ---
def load_pickle(filename, label):
    try:
        return pickle.load(open(filename, 'rb'))
    except FileNotFoundError:
        st.error(f"{label} model artifacts not found. Please run the training script first.")
        return None

# Heart Disease files
scaler_hd = load_pickle('heart_disease_scaler.pkl', "Heart Disease Scaler")
model_hd = load_pickle('heart_disease_model.pkl', "Heart Disease Model")
feature_order_hd = load_pickle('heart_disease_feature_order.pkl', "Heart Disease Features")

# Diabetes files
scaler_db = load_pickle('diabetes_scaler.pkl', "Diabetes Scaler")
model_db = load_pickle('diabetes_model.pkl', "Diabetes Model")
feature_order_db = load_pickle('diabetes_feature_order.pkl', "Diabetes Features")

# --- UI ---
st.title("🩺 Disease Risk Prediction")

st.markdown("### Common Patient Info")
age = st.number_input('Age (common)', min_value=1, max_value=110, value=30)

# ---------------- HEART DISEASE ----------------
st.markdown("---")
st.header("❤️ Heart Disease Parameters")
col1, col2 = st.columns(2)
with col1:
    sex = st.selectbox('Sex (Heart)', options=["", "Male", "Female"])
    sex = 1 if sex == 'Male' else (0 if sex == 'Female' else None)
    cp = st.selector('Chest Pain Type (Heart)', options=["", 0, 1, 2, 3])
    trestbps = st.number_input('Resting Blood Pressure (Heart, mm Hg)', min_value=0, max_value=200, value=0)
    chol = st.number_input('Cholesterol (Heart, mg/dl)', min_value=0, max_value=600, value=0)
    fbs = st.selectbox('Fasting Blood Sugar > 120 mg/dl (Heart)', options=["", 0, 1])
with col2:
    restecg = st.selectbox('Resting ECG Results (Heart)', options=["", 0, 1, 2])
    thalach = st.number_input('Max Heart Rate Achieved (Heart)', min_value=0, max_value=220, value=0)
    exang = st.selectbox('Exercise Induced Angina (Heart)', options=["", 0, 1])
    oldpeak = st.number_input('ST Depression by Exercise (Heart)', min_value=0.0, max_value=10.0, value=0.0, format="%.1f")
    slope = st.selectbox('Slope of Peak Exercise ST Segment (Heart)', options=["", 0, 1, 2])
    ca = st.selectbox('Number of Major Vessels (Heart)', options=["", 0, 1, 2, 3])
    thal = st.selectbox('Thalassemia (Heart)', options=["", 0, 1, 2, 3])

if st.button("🔮 Predict Heart Disease"):
    if scaler_hd and model_hd and feature_order_hd:
        user_input_hd = {
            'age': age, 'sex': sex, 'cp': cp, 'trestbps': trestbps,
            'chol': chol, 'fbs': fbs, 'restecg': restecg, 'thalach': thalach,
            'exang': exang, 'oldpeak': oldpeak, 'slope': slope,
            'ca': ca, 'thal': thal
        }
        # Check missing
        missing = [k for k, v in user_input_hd.items() if v in [None, 0]]
        if missing:
            st.error(f"Please enter values for these parameters before prediction: {missing}")
        else:
            input_df_hd = pd.DataFrame([user_input_hd])[feature_order_hd]
            input_scaled_hd = scaler_hd.transform(input_df_hd)
            risk_proba_hd = model_hd.predict_proba(input_scaled_hd)[0][1] * 100
            st.subheader("Heart Disease Prediction:")
            st.metric("Risk of Heart Disease", f"{risk_proba_hd:.2f}%")
            if risk_proba_hd > 50:
                st.warning("⚠️ High risk of Heart Disease.")
            else:
                st.success("✅ Low risk of Heart Disease.")

# ---------------- DIABETES ----------------
st.markdown("---")
st.header("🩸 Diabetes Parameters")
col3, col4 = st.columns(2)
with col3:
    pregnancies = st.number_input('Pregnancies (Diabetes)', min_value=0, max_value=20, value=0)
    glucose = st.number_input('Glucose (Diabetes)', min_value=0, max_value=300, value=0)
    bp = st.number_input('Blood Pressure (Diabetes, mm Hg)', min_value=0, max_value=200, value=0)
    skin = st.number_input('Skin Thickness (Diabetes)', min_value=0, max_value=100, value=0)
with col4:
    insulin = st.number_input('Insulin (Diabetes)', min_value=0, max_value=1000, value=0)
    bmi = st.number_input('BMI (Diabetes)', min_value=0.0, max_value=70.0, value=0.0, format="%.1f")
    dpf = st.number_input('Diabetes Pedigree Function (Diabetes)', min_value=0.0, max_value=5.0, value=0.0, format="%.2f")

if st.button("🔮 Predict Diabetes"):
    if scaler_db and model_db and feature_order_db:
        user_input_db = {
            'Pregnancies': pregnancies,
            'Glucose': glucose,
            'BloodPressure': bp,
            'SkinThickness': skin,
            'Insulin': insulin,
            'BMI': bmi,
            'DiabetesPedigreeFunction': dpf,
            'Age': age
        }
        # Check missing
        missing = [k for k, v in user_input_db.items() if v in [None, 0, 0.0]]
        if missing:
            st.error(f"Please enter values for these parameters before prediction: {missing}")
        else:
            input_df_db = pd.DataFrame([user_input_db])[feature_order_db]
            input_scaled_db = scaler_db.transform(input_df_db)
            risk_proba_db = model_db.predict_proba(input_scaled_db)[0][1] * 100
            st.subheader("Diabetes Prediction:")
            st.metric("Risk of Diabetes", f"{risk_proba_db:.2f}%")
            if risk_proba_db > 50:
                st.warning("⚠️ High risk of Diabetes.")
            else:
                st.success("✅ Low risk of Diabetes.")
