import streamlit as st
from streamlit.components.v1 import html
from utils.bedrock import get_medical_analysis
from utils.db import create_tables, generate_access_key, add_user, validate_key, deactivate_user, reactivate_user, get_all_users, increment_submission_count
from dotenv import load_dotenv
import bcrypt
import os

# Load environment variables
load_dotenv()

VERSION = "0.1.1"  # Application version

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
    if 'error_message' not in st.session_state:
        st.session_state.error_message = None
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'access_key' not in st.session_state:
        st.session_state.access_key = None

def login_page():
    st.title("Kyral MediChat AI Assistant - Login")
    st.markdown("Please enter your access key to access the application.")
    
    with st.form("login_form"):
        access_key = st.text_input("Access Key", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            user = validate_key(access_key)
            if user:
                st.session_state.logged_in = True
                st.session_state.user = user
                st.session_state.access_key = access_key  # Store access key for submission tracking
                st.rerun()
            else:
                st.error("Invalid or inactive access key. Please try again.")

def disable_submit_button():
    st.session_state.processing = True

def render_sidebar():
    st.sidebar.title("Steps")
    steps = ["Patient Information", "Results"]
    
    if st.session_state.user and st.session_state.user['role'] == 'admin':
        steps.append("Admin")
    
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
                    if step != "Admin":
                        st.session_state.form_submitted = False
                        st.session_state.analysis_results = None
                        st.session_state.processing = False
                    st.rerun()

    # Add version display at bottom of sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"v{VERSION}", help="Kyral MediChat AI Assistant Version")

def render_patient_form():
    st.title("Kyral MediChat AI Assistant")
    st.markdown("""
    This application uses AI to assist in medical diagnosis. Please note that this tool is for 
    informational purposes only and should not replace professional medical advice.
    """)
    
    with st.form("patient_info_form"):
        if st.session_state.error_message:
            st.error(st.session_state.error_message)
            st.session_state.error_message = None
            
        st.subheader("Primary Information") 
        
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        
        with col1:
            age = st.number_input("Age", min_value=0, max_value=120, value=None)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=None)
            primary_symptoms = st.text_area("Primary Symptoms", height=100)
            symptom_duration = st.text_input("Symptom Onset and Duration")
            
        with col2:
            existing_conditions = st.text_area("Existing Medical Conditions", height=100)
            current_medications = st.text_area("Current Medications", height=100)
            lab_results = st.text_area("Recent Lab Test Results", height=100)
        
        with col3:
            # Vital Signs Section
            st.subheader("Vital Signs (Optional)")
            blood_pressure = st.text_input("Blood Pressure (e.g., 120/80)")
            heart_rate = st.number_input("Heart Rate (bpm)", min_value=0, max_value=250, value=None)
            temperature = st.number_input("Temperature (°F)", min_value=90.0, max_value=116.0, value=None)
            
        with col4:
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
                st.session_state.error_message = "Please fill in all required fields (Age, Gender, Primary Symptoms, and Symptom Duration)"    
                st.session_state.processing = False
                st.rerun()
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
                html("""
                 <script>
                        setTimeout(() => {
                            const spinner = document.getElementById("analysis_spinner");
                            console.log("Spinner element:", spinner);
                            if (spinner) {
                                spinner.scrollIntoView({ behavior: 'smooth', block: 'center' });
                            }
                        }, 100);
                    </script>
                 <div id="analysis_spinner" style="height:0"></div>
                 """.encode(), height=0)                
                
                st.session_state.analysis_results = get_medical_analysis(patient_data)
                st.session_state.form_submitted = True
                st.session_state.current_step = "Results"
                st.session_state.processing = False
                
                # Increment submission count for the user
                if 'access_key' in st.session_state:
                    increment_submission_count(st.session_state.access_key)
                
                st.rerun()
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.session_state.processing = False

def render_results():
    st.title("Analysis & Insights")
    
    if not st.session_state.form_submitted:
        st.warning("Please complete the patient information form first.")
        if st.button("Go to Patient Information"):
            st.session_state.current_step = "Patient Information"
        return
    
    if st.session_state.analysis_results:
            st.success("Analysis complete!")
            
            # Display results in tabs
            tab1, tab2 = st.tabs(["Diagnoses", "Insights"])
            
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
                    st.subheader("Summary")
                    st.write(st.session_state.analysis_results['general_notes'])

def render_admin():
    st.title("Admin Panel - User Management")
    
    if not st.session_state.user or st.session_state.user['role'] != 'admin':
        st.error("Access denied. Admin privileges required.")
        return
    
    st.subheader("Generate New Access Key")
    with st.form("generate_key_form"):
        email = st.text_input("Email (optional, for reference)")
        role = st.selectbox("Role", ["user", "admin"], index=0)
        submit_generate = st.form_submit_button("Generate Key")
        
        if submit_generate:
            new_key = generate_access_key()
            if add_user(new_key, role=role, email=email if email else None):
                st.success(f"New access key generated successfully!")
                st.code(new_key, language=None)
                st.info("Share this key with the user to grant access.")
                if email:
                    st.info(f"Key associated with: {email}")
            else:
                st.error("Failed to generate key. Please try again.")
    
    st.subheader("Manage Users")
    users = get_all_users()
    if users:
        for user in users:
            email_display = f" | Email: {user['email']}" if user['email'] else ""
            submission_display = f" | Submissions: {user['submission_count']}"
            with st.expander(f"Key: {user['access_key'][:10]}... | Role: {user['role']} | Active: {user['is_active']}{email_display}{submission_display}"):
                col1, col2 = st.columns(2)
                with col1:
                    if user['is_active']:
                        if st.button("Deactivate", key=f"deactivate_{user['id']}"):
                            if deactivate_user(user['access_key']):
                                st.success("User deactivated.")
                                st.rerun()
                            else:
                                st.error("Failed to deactivate user.")
                    else:
                        if st.button("Reactivate", key=f"reactivate_{user['id']}"):
                            if reactivate_user(user['access_key']):
                                st.success("User reactivated.")
                                st.rerun()
                            else:
                                st.error("Failed to reactivate user.")
                with col2:
                    st.write(f"Created: {user['created_at']}")
    else:
        st.info("No users found.")

def main():
    st.set_page_config(
        page_title="Kyral MediChat AI Assistant",
        page_icon="🏥",
        layout="wide"
    )
    
    # Initialize database
    try:
        create_tables()
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return
    
    initialize_session_state()

    if not st.session_state.logged_in:
        login_page()
    else:
        # Add logout button in sidebar
        if st.sidebar.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.access_key = None  # Clear access key on logout
            st.rerun()
        
        # Add admin link if admin
        if st.session_state.user and st.session_state.user['role'] == 'admin':
            if st.sidebar.button("Admin Panel"):
                st.session_state.current_step = "Admin"
                st.rerun()
        
        render_sidebar()
        
        if st.session_state.current_step == "Patient Information":
            render_patient_form()
        elif st.session_state.current_step == "Results":
            render_results()
        elif st.session_state.current_step == "Admin":
            render_admin()

if __name__ == "__main__":
    main()
