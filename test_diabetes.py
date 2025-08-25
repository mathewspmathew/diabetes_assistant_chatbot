import streamlit as st
import pandas as pd
import pickle
import numpy as np

# --- 1. LOAD THE SAVED ARTIFACTS ---
# We load the scaler, model, and feature order that we saved during training
try:
    scaler = pickle.load(open('heart_disease_scaler.pkl', 'rb'))
    model = pickle.load(open('heart_disease_model.pkl', 'rb'))
    feature_order = pickle.load(open('heart_disease_feature_order.pkl', 'rb'))
except FileNotFoundError:
    st.error("Model artifacts not found. Please run the training script first.")
    st.stop()

# --- 2. BUILD THE USER INTERFACE ---
st.title('🩺 Disease Risk Prediction')
st.header('Enter Patient Health Data')

# ['age',
#  'sex',
#  'cp',
#  'trestbps',
#  'chol',
#  'fbs',
#  'restecg',
#  'thalach',
#  'exang',
#  'oldpeak',
#  'slope',
#  'ca',
#  'thal']


# Use st.columns for cleaner layout
col1, col2 = st.columns(2)

with col1:
    age = st.number_input('Age', min_value=1, max_value=110, value=30)
    # Sex as dropdown
    sex = st.selectbox('Sex', options=['Male', 'Female'])
    sex = 1 if sex == 'Male' else 0
    cp = st.selectbox('Chest Pain Type (cp)', options=[0, 1, 2, 3])
    trestbps = st.number_input('Resting Blood Pressure (mm Hg)', min_value=80, max_value=200, value=120)
    chol = st.number_input('Cholesterol (mg/dl)', min_value=100, max_value=600, value=200)
    fbs = st.selectbox('Fasting Blood Sugar > 120 mg/dl (fbs)', options=[0, 1])
with col2:
    restecg = st.selectbox('Resting ECG Results (restecg)', options=[0, 1, 2])
    thalach = st.number_input('Max Heart Rate Achieved (thalach)', min_value=60, max_value=220, value=150)
    exang = st.selectbox('Exercise Induced Angina (exang)', options=[0, 1])
    oldpeak = st.number_input('ST Depression Induced by Exercise (oldpeak)', min_value=0.0, max_value=10.0, value=1.0, format="%.1f")
    slope = st.selectbox('Slope of Peak Exercise ST Segment (slope)', options=[0, 1, 2])
    ca = st.selectbox('Number of Major Vessels (ca)', options=[0, 1, 2, 3])
    thal = st.selectbox('Thalassemia (thal)', options=[0, 1, 2, 3])

# --- Prepare Input for Model ---
if st.button('Predict Heart Disease Risk'):
    user_input = {
        'age': age,
        'sex': sex,
        'cp': cp,
        'trestbps': trestbps,
        'chol': chol,
        'fbs': fbs,
        'restecg': restecg,
        'thalach': thalach,
        'exang': exang,
        'oldpeak': oldpeak,
        'slope': slope,
        'ca': ca,
        'thal': thal
    }

    # Create a DataFrame from the dictionary
    # Important: Ensure the column order matches the training data using feature_order
    input_df = pd.DataFrame([user_input])[feature_order]
    
    st.subheader("User Input:")
    st.write(input_df)

    # --- 4. SCALE THE INPUT AND PREDICT ---
    # Scale the user input using the loaded scaler
    input_scaled = scaler.transform(input_df)

    # Make the prediction
    # .predict_proba gives the probability for each class (0 and 1)
    prediction_proba = model.predict_proba(input_scaled)
    
    # Get the probability of the positive class (diabetes = 1)
    risk_probability = prediction_proba[0][1] 
    risk_percentage = risk_probability * 100

    # --- 5. DISPLAY THE RESULT ---
    st.subheader("Prediction Result:")
    st.metric(label="Risk of Diabetes", value=f"{risk_percentage:.2f}%")

    if risk_percentage > 50:
        st.warning("The patient is at a high risk of diabetes.")
        # Here you can trigger other phases: RAG, Recommendations, etc.
    else:
        st.success("The patient is at a low risk of diabetes.")