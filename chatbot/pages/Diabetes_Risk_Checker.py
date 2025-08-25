import streamlit as st
import pandas as pd
import pickle

def load_pickle(filename, label):
    try:
        return pickle.load(open(filename, 'rb'))
    except FileNotFoundError:
        st.error(f"{label} not found. Run training first.")
        return None

scaler_db = load_pickle('diabetes_scaler.pkl', "Diabetes Scaler")
model_db = load_pickle('diabetes_model.pkl', "Diabetes Model")
feature_order_db = load_pickle('diabetes_feature_order.pkl', "Diabetes Features")

st.title("🩸 Diabetes Prediction")

age = st.number_input('Age', 1, 110, 30)

col1, col2 = st.columns(2)
with col1:
    pregnancies = st.number_input('Pregnancies', 0, 20, 0)
    glucose = st.number_input('Glucose', 0, 300, 0)
    bp = st.number_input('Blood Pressure (mm Hg)', 0, 200, 0)
    skin = st.number_input('Skin Thickness', 0, 100, 0)
with col2:
    insulin = st.number_input('Insulin', 0, 1000, 0)
    bmi = st.number_input('BMI', 0.0, 70.0, 0.0, format="%.1f")
    dpf = st.number_input('Diabetes Pedigree Function', 0.0, 5.0, 0.0, format="%.2f")

if st.button("🔮 Predict Diabetes"):
    if scaler_db and model_db and feature_order_db:
        user_input_db = {
            'Pregnancies': pregnancies, 'Glucose': glucose, 'BloodPressure': bp,
            'SkinThickness': skin, 'Insulin': insulin, 'BMI': bmi,
            'DiabetesPedigreeFunction': dpf, 'Age': age
        }

        missing = [k for k, v in user_input_db.items() if v in [None, 0, 0.0]]
        if missing:
            st.error(f"Please enter: {missing}")
        else:
            df = pd.DataFrame([user_input_db])[feature_order_db]
            X = scaler_db.transform(df)
            risk = model_db.predict_proba(X)[0][1] * 100
            st.metric("Risk of Diabetes", f"{risk:.2f}%")
            st.warning("⚠️ High Risk!" if risk > 50 else "✅ Low Risk")
