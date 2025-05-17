import boto3
import json
from typing import Dict, Any
import os
import traceback

def get_bedrock_client():
    """Initialize and return the AWS Bedrock client."""
    return boto3.client(
        service_name='bedrock-runtime',
        region_name=os.getenv('AWS_REGION')  # Update this based on your .env configuration
    )

def format_medical_prompt(patient_data: Dict[str, Any]) -> str:
    """Format the medical data into a prompt for the LLM."""
    prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
As a medical diagnostic AI assistant, analyze the following patient information and provide potential diagnoses with confidence scores, reasoning, and recommended actions. Please format your response in JSON. Do not include markdown tags.<|eot_id|><|start_header_id|>user<|end_header_id|>

Patient Information:
- Age: {patient_data.get('age')}
- Gender: {patient_data.get('gender')}
- Primary Symptoms: {patient_data.get('primary_symptoms')}
- Symptom Duration: {patient_data.get('symptom_duration')}
- Existing Conditions: {patient_data.get('existing_conditions')}
- Current Medications: {patient_data.get('current_medications')}
- Lab Results: {patient_data.get('lab_results')}
- Vital Signs: {patient_data.get('vital_signs')}
- Lifestyle Factors: {patient_data.get('lifestyle_factors')}

Analyze this information and provide:
1. Multiple possible diagnoses with confidence scores
2. Detailed reasoning for each diagnosis
3. Recommended next steps (tests, lifestyle changes, or medical care)

Format the response as JSON with the following structure:
{{
    "diagnoses": [
        {{
            "condition": "string",
            "confidence": number,
            "reasoning": "string",
            "urgency_level": "string"
        }}
    ],
    "recommendations": {{
        "immediate_actions": ["string"],
        "tests": ["string"],
        "lifestyle_changes": ["string"]
    }},
    "general_notes": "string"
}}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
    return prompt

def get_medical_analysis(patient_data: Dict[str, Any]) -> Dict[str, Any]:
    """Send request to AWS Bedrock and get medical analysis."""
    client = get_bedrock_client()
    
    prompt = format_medical_prompt(patient_data)
    
    # Write prompt to file for debugging
    debug_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'debug')
    os.makedirs(debug_dir, exist_ok=True)
    debug_file = os.path.join(debug_dir, 'latest_prompt.txt')
    with open(debug_file, 'w', encoding='utf-8') as f:
        f.write(prompt)
    print(f"Prompt written to {debug_file} for debugging")
    
    body = json.dumps({
        "prompt": prompt,
        "max_gen_len": 1000,
        "temperature": 0.5,
    })
    
    accept = 'application/json'
    content_type = 'application/json'
    
    # debug_body_file = os.path.join(debug_dir, 'latest_body.json')
    # with open(debug_body_file, 'w', encoding='utf-8') as f:
    #     json.dump(body, f, indent=2)
    # print(f"Body written to {debug_body_file} for debugging")
    
    try:
        response = client.invoke_model(
            modelId='arn:aws:bedrock:us-east-1:597953171030:inference-profile/us.meta.llama3-3-70b-instruct-v1:0',
            body=body,
            accept=accept,
            contentType=content_type,
        )
        response_body_raw = response.get('body').read()
        # print(response_body_raw)
        
        response_body = json.loads(response_body_raw)
        # Write response_body to file for debugging
        debug_response_file = os.path.join(debug_dir, 'latest_response.json')
        with open(debug_response_file, 'w', encoding='utf-8') as f:
            json.dump(response_body, f, indent=2)
        print(f"Response written to {debug_response_file} for debugging")
        generation = json.loads(response_body.get('generation', '{}'))
        return generation
    except Exception as e:
        # print(f"Error in medical analysis: {str(e)}")
        traceback.print_exc()
        return {}
