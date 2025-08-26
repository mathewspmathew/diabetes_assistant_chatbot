# import streamlit as st
# import pandas as pd
# import pickle

# # --- Load Pickle ---
# def load_pickle(filename, label):
#     try:
#         return pickle.load(open(filename, 'rb'))
#     except FileNotFoundError:
#         st.error(f"{label} not found. Run training first.")
#         return None

# scaler_hd = load_pickle('heart_disease_scaler.pkl', "Heart Disease Scaler")
# model_hd = load_pickle('heart_disease_model.pkl', "Heart Disease Model")
# feature_order_hd = load_pickle('heart_disease_feature_order.pkl', "Heart Disease Features")

# st.title("❤️ Heart Disease Prediction")

# age = st.number_input('Age', min_value=1, max_value=110, value=30)

# col1, col2 = st.columns(2)
# with col1:
#     sex = st.selectbox('Sex', ["", "Male", "Female"])
#     sex = 1 if sex == 'Male' else (0 if sex == 'Female' else None)
#     cp = st.selectbox('Chest Pain Type', ["", 0, 1, 2, 3])
#     trestbps = st.number_input('Resting BP (mm Hg)', 0, 200, 0)
#     chol = st.number_input('Cholesterol (mg/dl)', 0, 600, 0)
#     fbs = st.selectbox('Fasting Blood Sugar > 120', ["", 0, 1])
# with col2:
#     restecg = st.selectbox('Resting ECG', ["", 0, 1, 2])
#     thalach = st.number_input('Max Heart Rate', 0, 220, 0)
#     exang = st.selectbox('Exercise Angina', ["", 0, 1])
#     oldpeak = st.number_input('ST Depression', 0.0, 10.0, 0.0, format="%.1f")
#     slope = st.selectbox('Slope of ST Segment', ["", 0, 1, 2])
#     ca = st.selectbox('Major Vessels', ["", 0, 1, 2, 3])
#     thal = st.selectbox('Thalassemia', ["", 0, 1, 2, 3])

# if st.button("🔮 Predict Heart Disease"):
#     if scaler_hd and model_hd and feature_order_hd:
#         user_input_hd = {
#             'age': age, 'sex': sex, 'cp': cp, 'trestbps': trestbps,
#             'chol': chol, 'fbs': fbs, 'restecg': restecg, 'thalach': thalach,
#             'exang': exang, 'oldpeak': oldpeak, 'slope': slope,
#             'ca': ca, 'thal': thal
#         }

#         missing = [k for k, v in user_input_hd.items() if v in [None, 0]]
#         if missing:
#             st.error(f"Please enter: {missing}")
#         else:
#             df = pd.DataFrame([user_input_hd])[feature_order_hd]
#             X = scaler_hd.transform(df)
#             risk = model_hd.predict_proba(X)[0][1] * 100
#             st.metric("Risk of Heart Disease", f"{risk:.2f}%")
#             st.warning("⚠️ High Risk!" if risk > 50 else "✅ Low Risk")
