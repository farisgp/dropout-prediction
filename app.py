import streamlit as st
import joblib
import numpy as np

# Load model dan scaler
model = joblib.load('./rdf_model.joblib')
scaler = joblib.load('./scaler.pkl')

def predict_status(inputs):
    dummy_features = [0] * (36 - len(inputs))
    final_input = inputs + dummy_features

    input_array = np.array(final_input).reshape(1, -1)
    input_array_scaled = scaler.transform(input_array)
    prediction = model.predict(input_array_scaled)
    return prediction

st.sidebar.title("About App")
st.sidebar.info("""
**Jaya Jaya Institut**

Jaya Jaya Institut adalah perguruan tinggi yang berdiri sejak tahun 2000 dan telah menghasilkan banyak lulusan unggulan di berbagai bidang.

Namun, tingginya angka dropout menjadi masalah serius karena menurunkan angka kelulusan dan citra kampus di mata calon mahasiswa.

Melalui aplikasi ini, Jaya Jaya Institut berupaya memberikan solusi berbasis data untuk memprediksi risiko dropout, agar mahasiswa memiliki peluang lebih besar untuk menyelesaikan studi.
""")

st.markdown("<h3 style='text-align: center;'>Student Dropout Prediction (Prototype)</h3>", unsafe_allow_html=True)
st.write("---")


col1, col2 = st.columns(2)

with col1:
    curricular_units_2nd_sem_approved = st.number_input('Curricular Units 2nd Sem (Approved)', 0, 30, 8)
    curricular_units_2nd_sem_grade = st.number_input('Curricular Units 2nd Sem (Grade)', 0, 20, 17)
    curricular_units_1st_sem_approved = st.number_input('Curricular Units 1st Sem (Approved)', 0, 30, 7)
    curricular_units_1st_sem_grade = st.number_input('Curricular Units 1st Sem (Grade)', 0, 20, 17)
    curricular_units_2nd_sem_evaluations = st.number_input('Curricular Units 2nd Sem (Evaluations)', 0, 20, 9)

with col2:
    admission_grade = st.slider('Admission Grade', min_value=0.0, max_value=200.0, value=170.0, step=0.1)
    tuition_fees_up_to_date = st.selectbox('Tuition Fees Up To Date?', [0, 1], format_func=lambda x: 'No' if x == 0 else 'Yes')
    age_at_enrollment = st.number_input('Age At Enrollment', min_value=0, max_value=30, value=19)
    previous_qualification_grade = st.slider('Previous Qualification Grade', min_value=0.0, max_value=200.0, value=160.0, step=0.1)
    curricular_units_1st_sem_evaluations = st.number_input('Curricular Units 1st Sem (Evaluations)', 0, 20, 8)

# Prepare input
input_data = [
    curricular_units_2nd_sem_approved,
    curricular_units_2nd_sem_grade,
    curricular_units_1st_sem_approved,
    curricular_units_1st_sem_grade,
    tuition_fees_up_to_date,
    curricular_units_2nd_sem_evaluations,
    age_at_enrollment,
    previous_qualification_grade,
    admission_grade,
    curricular_units_1st_sem_evaluations
]

if st.button(' Prediction '):
    prediction = predict_status(input_data)
    if prediction[0] == 0:
        st.error(f"The model predicts that the student is likely to be:  **Dropout**")
    elif prediction[0] == 1:
        st.info(f"The model predicts that the student is likely to be:  **Enrolled**")
    else:
        st.success(f"The model predicts that the student is likely to be:  **Graduate**")