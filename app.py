import streamlit as st
from utils.bedrock import get_medical_analysis
from dotenv import load_dotenv
import bcrypt
import os

# Load environment variables
load_dotenv()

def initialize_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'current_step' not in st.session_state:
        st.session_state.current_step = "Patient Information"
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False
    if 'processing' not in st.session_state:
        st.session_state.processing = False

def check_password(password):
    stored_hash = os.getenv('APP_PASSWORD_HASH')
    if not stored_hash:
        st.error("Password hash not found in environment variables!")
        return False
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))

def login_page():
    st.title("MediChat AI Assistant - Login")
    st.markdown("Please enter your password to access the application.")
    
    with st.form("login_form"):
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if check_password(password):
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Incorrect password. Please try again.")
        
def disable_submit_button():
    st.session_state.processing = True

def render_sidebar():
    st.sidebar.title("Steps")
    steps = ["Patient Information", "Results"]
    
    for step in steps:
        if step == "Results" and not st.session_state.form_submitted:
            # Grey out Results step if form not submitted
            st.sidebar.markdown(
                f'<div style="opacity: 0.5; color: gray;">⚪ {step}</div>',
                unsafe_allow_html=True
            )
        elif step == st.session_state.current_step:
            # Highlight current step
            st.sidebar.markdown(f'🔵 **{step}**')
        else:
            # Show completed or available steps as clickable
            if st.sidebar.button(f'⚪ {step}', key=f'btn_{step}'):
                # Only allow navigation to Results if form is submitted
                if step != "Results" or st.session_state.form_submitted:
                    st.session_state.current_step = step
                    st.session_state.form_submitted = False
                    st.session_state.analysis_results = None
                    st.session_state.processing = False
                    st.rerun()

def render_patient_form():
    st.title("MediChat AI Assistant")
    st.markdown("""
    This application uses AI to assist in medical diagnosis. Please note that this tool is for 
    informational purposes only and should not replace professional medical advice.
    """)
    
    with st.form("patient_info_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Primary Information")
            age = st.number_input("Age", min_value=0, max_value=120, value=None)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=None)
            primary_symptoms = st.text_area("Primary Symptoms", height=100)
            symptom_duration = st.text_input("Symptom Onset and Duration")
            existing_conditions = st.text_area("Existing Medical Conditions", height=100)
            current_medications = st.text_area("Current Medications", height=100)
            lab_results = st.text_area("Recent Lab Test Results", height=100)
        
        with col2:
            # Vital Signs Section
            st.subheader("Vital Signs (Optional)")
            blood_pressure = st.text_input("Blood Pressure (e.g., 120/80)")
            heart_rate = st.number_input("Heart Rate (bpm)", min_value=0, max_value=250, value=None)
            temperature = st.number_input("Temperature (°F)", min_value=90.0, max_value=116.0, value=None)
            
            st.markdown("---")
            
            # Lifestyle Factors Section
            st.subheader("Lifestyle Factors (Optional)")
            smoking = st.selectbox("Smoking Status", ["Non-smoker", "Former smoker", "Current smoker"], index=None)
            alcohol = st.selectbox("Alcohol Consumption", ["None", "Occasional", "Moderate", "Heavy"], index=None)
            physical_activity = st.selectbox(
                "Physical Activity Level",
                ["Sedentary", "Light", "Moderate", "Very active"],
                index=None
            )
        
        st.markdown("---")
        submit_button = st.form_submit_button("Submit and View Results", on_click=disable_submit_button, disabled=st.session_state.processing)

    if submit_button:
        try:
            # Validate required fields
            if not all([age, gender, primary_symptoms, symptom_duration]):
                st.error("Please fill in all required fields (Age, Gender, Primary Symptoms, and Symptom Duration)")
                return

            # Prepare patient data
            patient_data = {
                "age": age,
                "gender": gender,
                "primary_symptoms": primary_symptoms,
                "symptom_duration": symptom_duration,
                "existing_conditions": existing_conditions,
                "current_medications": current_medications,
                "lab_results": lab_results,
                "vital_signs": {
                    "blood_pressure": blood_pressure,
                    "heart_rate": heart_rate,
                    "temperature": temperature
                },
                "lifestyle_factors": {
                    "smoking": smoking,
                    "alcohol": alcohol,
                    "physical_activity": physical_activity
                }
            }

            with st.spinner("Analyzing patient information..."):
                st.session_state.analysis_results = get_medical_analysis(patient_data)
                st.session_state.form_submitted = True
                st.session_state.current_step = "Results"
                st.session_state.processing = False
                st.rerun()
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.session_state.processing = False

def render_results():
    st.title("Analysis Results")
    
    if not st.session_state.form_submitted:
        st.warning("Please complete the patient information form first.")
        if st.button("Go to Patient Information"):
            st.session_state.current_step = "Patient Information"
        return
    
    if st.session_state.analysis_results:
            st.success("Analysis complete!")
            
            # Display results in tabs
            tab1, tab2 = st.tabs(["Diagnoses", "Recommendations"])
            
            with tab1:
                # Display confidence chart
                if 'diagnoses' in st.session_state.analysis_results:                    
                    # Display detailed diagnosis information
                    for diagnosis in st.session_state.analysis_results['diagnoses']:
                        with st.expander(f"{diagnosis['condition']} ({diagnosis['confidence'] * 100:.1f}% confidence)", expanded=True):
                            st.write("**Reasoning:**", diagnosis['reasoning'])
                            st.write("**Urgency Level:**", diagnosis['urgency_level'])
            
            with tab2:
                if 'recommendations' in st.session_state.analysis_results:
                    recommendations = st.session_state.analysis_results['recommendations']
                    
                    if 'immediate_actions' in recommendations:
                        st.subheader("Immediate Actions")
                        for action in recommendations['immediate_actions']:
                            st.write(f"• {action}")
                    
                    if 'tests' in recommendations:
                        st.subheader("Recommended Tests")
                        for test in recommendations['tests']:
                            st.write(f"• {test}")
                    
                    if 'lifestyle_changes' in recommendations:
                        st.subheader("Lifestyle Recommendations")
                        for change in recommendations['lifestyle_changes']:
                            st.write(f"• {change}")
                    
                if 'general_notes' in st.session_state.analysis_results:
                    st.subheader("Additional Notes")
                    st.write(st.session_state.analysis_results['general_notes'])

def main():
    st.set_page_config(
        page_title="MediChat AI Assistant",
        page_icon="🏥",
        layout="wide"
    )
    
    initialize_session_state()

    if not st.session_state.logged_in:
        login_page()
    else:
        # Add logout button in sidebar
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()
        
        render_sidebar()
        
        if st.session_state.current_step == "Patient Information":
            render_patient_form()
        else:  # Results page
            render_results()

if __name__ == "__main__":
    main()
