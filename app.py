import streamlit as st
import joblib
import numpy as np

# Load model dan scaler
model = joblib.load('./rdf_model.joblib')
scaler = joblib.load('./scaler.pkl')

def predict_status(inputs):
    input_array = np.array(inputs).reshape(1, -1)
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
    admission_grade = st.slider('Admission Grade', min_value=0.0, max_value=200.0, value=170.0, step=0.1)
    curricular_units_1st_sem_approved = st.number_input('Curricular Units 1st Sem (Approved)', 0, 30, 7)
    curricular_units_2nd_sem_grade = st.number_input('Curricular Units 2nd Sem (Grade)', 0, 20, 17)
    curricular_units_1st_sem_grade = st.number_input('Curricular Units 1st Sem (Grade)', 0, 20, 17)

with col2:
    tuition_fees_up_to_date = st.selectbox('Tuition Fees Up To Date?', [0, 1], format_func=lambda x: 'No' if x == 0 else 'Yes')
    curricular_units_1st_sem_enrolled = st.number_input('Curricular Units 1st Semester Enrolled', min_value=0, max_value=30, value=20)
    curricular_units_2nd_sem_enrolled = st.number_input('Curricular Units 2nd Semester Enrolled', min_value=0, max_value=30, value=20)
    displaced = st.selectbox('Displaced', [0, 1], format_func=lambda x: 'Yes' if x == 1 else 'No')
    scholarship_holder = st.selectbox('Scholarship Holder', [0, 1], format_func=lambda x: 'Yes' if x == 1 else 'No')

# Prepare input
input_data = [
    curricular_units_2nd_sem_approved,
    admission_grade,
    curricular_units_1st_sem_approved,
    curricular_units_2nd_sem_grade,
    curricular_units_1st_sem_grade,
    tuition_fees_up_to_date,
    curricular_units_1st_sem_enrolled,
    curricular_units_2nd_sem_enrolled,
    displaced,
    scholarship_holder
]

if st.button('Predict'):
    prediction = predict_status(input_data)

    status_dict = {
        0: ('Dropout', 'red'),
        1: ('Enrolled', 'orange'),
        2: ('Graduate', 'green')
    }
    
    predicted_status_index = np.argmax(prediction, axis=1)[0]
    predicted_status,color = status_dict[predicted_status_index]

    st.markdown(
        f"<h5>The model predicts that the student is likely to be: "
        f"<span style='color:{color}'>{predicted_status}</span></h5>",
        unsafe_allow_html=True
    )