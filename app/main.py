from chains import Chain
from prompts import Prompts
from utils import clean_text
import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Load the stress prediction model
model = joblib.load("/Users/surjith/Desktop/LegacyAssesment/MentalHealthCounsellor/app/stress_prediction_model.pkl")


# Stress Level Prediction Function
def stress_prediction():
    st.markdown("## Stress Level Prediction")
    st.write("Fill in the details below to predict your stress level.")

    # Input fields with structured layout
    col1, col2 = st.columns(2)

    with col1:
        gender = st.radio("Gender", options=["Male", "Female"])
        age = st.number_input("Age", min_value=1, max_value=100, value=25)
        occupation = st.selectbox("Occupation", options=[
            "Scientist", "Doctor", "Accountant", "Teacher", "Manager",
            "Engineer", "Sales Representative", "Salesperson",
            "Lawyer", "Software Engineer", "Nurse"
        ])
        sleep_duration = st.number_input("Sleep Duration (hours)", min_value=0.0, max_value=24.0, value=7.0)
        quality_of_sleep = st.slider("Quality of Sleep (1-10)", min_value=1, max_value=10, value=5)

    with col2:
        bmi_category = st.radio("BMI Category", options=["Underweight", "Normal", "Overweight"])
        heart_rate = st.number_input("Heart Rate (bpm)", min_value=50, max_value=150, value=70)
        daily_steps = st.number_input("Daily Steps", min_value=0, value=10000)
        systolic_bp = st.number_input("Systolic Blood Pressure", min_value=50, max_value=200, value=120)
        diastolic_bp = st.number_input("Diastolic Blood Pressure", min_value=30, max_value=150, value=80)

    # Encode inputs for prediction
    gender_encoded = 1 if gender == "Male" else 0
    occupation_encoded = [
        "Scientist", "Doctor", "Accountant", "Teacher", "Manager",
        "Engineer", "Sales Representative", "Salesperson",
        "Lawyer", "Software Engineer", "Nurse"
    ].index(occupation)
    bmi_category_encoded = ["Underweight", "Normal", "Overweight"].index(bmi_category) + 1

    if st.button("Predict Stress Level"):
        user_input = np.array([[gender_encoded, age, occupation_encoded, sleep_duration,
                                quality_of_sleep, bmi_category_encoded, heart_rate,
                                daily_steps, systolic_bp, diastolic_bp]])
        columns = ['Gender', 'Age', 'Occupation', 'Sleep Duration', 'Quality of Sleep',
                   'BMI Category', 'Heart Rate', 'Daily Steps', 'Systolic BP', 'Diastolic BP']
        user_input_df = pd.DataFrame(user_input, columns=columns)

        # Model prediction
        try:
            prediction = model.predict(user_input_df)
            st.success(f"Predicted Stress Level: {prediction[0]}")
        except Exception as e:
            st.error("Error occurred during prediction. Please try again.")


def create_streamlit_app(prompts, clean_text):
    st.title("Llama Mental Health Counsellor")
    input_text = st.text_area("Enter your question here", value=st.session_state.input_text, key="user_input")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            question = clean_text(input_text)
            prompts.load_prompts()
            responses = prompts.query_responses(question)

            # result = chain.response_generator(question, responses)
            result = chain.response_generator(question, responses)

            # Store the user's question and model's response in session state
            st.session_state.chat_history.append({"role": "User", "text": input_text})
            st.session_state.chat_history.append({"role": "Model", "text": result})

            # Clear the input box after submission
            st.session_state.input_text = ""

            # Display chat history
            for message in st.session_state.chat_history:
                with st.chat_message(message["role"]):
                    st.write(message["text"])
        except Exception as e:
            st.error(f"Error in processing the question: {e}")


# Streamlit App Configuration
if __name__ == "__main__":
    # Initialize objects
    chain = Chain()
    prompts = Prompts()

    # Set session states
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "input_text" not in st.session_state:
        st.session_state.input_text = ""

    # Set page config
    st.set_page_config(page_title="Llama Mental Health Counsellor", layout="wide")

    # Sidebar for navigation
    st.sidebar.header("Features")
    page = st.sidebar.radio("Select Feature", ["Mental Health Counsellor", "Stress Prediction"])

    # Page content
    if page == "Mental Health Counsellor":
        create_streamlit_app(prompts, clean_text)
    elif page == "Stress Prediction":
        stress_prediction()