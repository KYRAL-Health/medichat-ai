import streamlit as st
import plotly.graph_objects as go
from utils.bedrock import get_medical_analysis
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def create_confidence_chart(diagnoses):
    """Create a bar chart for diagnosis confidence scores."""
    conditions = [d['condition'] for d in diagnoses]
    confidences = [d['confidence'] * 100 for d in diagnoses]
    
    fig = go.Figure(data=[
        go.Bar(
            x=confidences,
            y=conditions,
            orientation='h',
            marker_color='rgb(26, 118, 255)'
        )
    ])
    
    fig.update_layout(
        title='Diagnosis Confidence Scores',
        xaxis_title='Confidence (%)',
        yaxis_title='Condition',
        height=400
    )
    
    return fig

def main():
    st.set_page_config(
        page_title="Medical Diagnosis Assistant",
        page_icon="🏥",
        layout="wide"
    )
    
    st.title("Medical Diagnosis Assistant")
    st.markdown("""
    This application uses AI to assist in medical diagnosis. Please note that this tool is for 
    informational purposes only and should not replace professional medical advice.
    """)
    
    # Create form for patient information
    with st.form("patient_info_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age", min_value=0, max_value=120, value=None)
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], index=None)
            primary_symptoms = st.text_area("Primary Symptoms", height=100)
            symptom_duration = st.text_input("Symptom Onset and Duration")
            existing_conditions = st.text_area("Existing Medical Conditions", height=100)
        
        with col2:
            current_medications = st.text_area("Current Medications", height=100)
            lab_results = st.text_area("Recent Lab Test Results", height=100)
            
            # Vital Signs (Optional)
            st.subheader("Vital Signs (Optional)")
            blood_pressure = st.text_input("Blood Pressure (e.g., 120/80)")
            heart_rate = st.number_input("Heart Rate (bpm)", min_value=0, max_value=250, value=None)
            temperature = st.number_input("Temperature (°F)", min_value=90.0, max_value=116.0, value=None)
            
            # Lifestyle Factors (Optional)
            st.subheader("Lifestyle Factors (Optional)")
            smoking = st.selectbox("Smoking Status", ["Non-smoker", "Former smoker", "Current smoker"], index=None)
            alcohol = st.selectbox("Alcohol Consumption", ["None", "Occasional", "Moderate", "Heavy"], index=None)
            physical_activity = st.selectbox(
                "Physical Activity Level",
                ["Sedentary", "Light", "Moderate", "Very active"],
                index=None
            )
        
        submit_button = st.form_submit_button("Analyze Symptoms")
        
    if submit_button:
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
            analysis_results = get_medical_analysis(patient_data)
        
        if analysis_results:
            st.success("Analysis complete!")
            
            # Display results in tabs
            tab1, tab2 = st.tabs(["Diagnoses", "Recommendations"])
            
            with tab1:
                # Display confidence chart
                if 'diagnoses' in analysis_results:
                    st.plotly_chart(create_confidence_chart(analysis_results['diagnoses']))
                    
                    # Display detailed diagnosis information
                    for diagnosis in analysis_results['diagnoses']:
                        with st.expander(f"{diagnosis['condition']} ({diagnosis['confidence'] * 100:.1f}% confidence)"):
                            st.write("**Reasoning:**", diagnosis['reasoning'])
                            st.write("**Urgency Level:**", diagnosis['urgency_level'])
            
            with tab2:
                if 'recommendations' in analysis_results:
                    recommendations = analysis_results['recommendations']
                    
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
                    
                    if 'general_notes' in analysis_results:
                        st.subheader("Additional Notes")
                        st.write(analysis_results['general_notes'])
        else:
            st.error("An error occurred during analysis. Please try again.")

if __name__ == "__main__":
    main()
