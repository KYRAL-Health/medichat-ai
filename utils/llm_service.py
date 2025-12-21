import json
from typing import Dict, Any
import os
import traceback
from openai import OpenAI

def get_llm_client():
    """Initialize and return the OpenAI client for vLLM."""
    return OpenAI(
        base_url="http://vllm:8000/v1",
        api_key="vllm-key",
    )

def format_medical_messages(patient_data: Dict[str, Any]) -> list:
    """Format the medical data into messages for the LLM."""
    
    # Build the uploaded documents section if available
    uploaded_docs_section = ""
    if patient_data.get('uploaded_medical_documents'):
        uploaded_docs_section = f"\n- Uploaded Medical Documents:\n{patient_data.get('uploaded_medical_documents')}\n"
    
    system_content = "As a medical diagnostic AI assistant, analyze the following patient information and provide potential diagnoses with confidence scores, reasoning, and recommended actions. Please format your response in JSON. Do not include markdown tags."

    user_content = f"""Patient Information:
- Age: {patient_data.get('age')}
- Gender: {patient_data.get('gender')}
- History of Present Illness: {patient_data.get('history_of_present_illness')}
- Symptom Duration: {patient_data.get('symptom_duration')}
- Existing Conditions: {patient_data.get('existing_conditions')}
- Current Medications: {patient_data.get('current_medications')}
- Lab Results: {patient_data.get('lab_results')}
- Vital Signs: {patient_data.get('vital_signs')}
- Lifestyle Factors: {patient_data.get('lifestyle_factors')}{uploaded_docs_section}

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
}}"""

    return [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_content}
    ]

def get_medical_analysis(patient_data: Dict[str, Any]) -> Dict[str, Any]:
    """Send request to vLLM and get medical analysis."""
    client = get_llm_client()
    
    messages = format_medical_messages(patient_data)
    
    try:
        response = client.chat.completions.create(
            model="medichat-finetuned",
            messages=messages,
            max_tokens=1000,
            temperature=0.5,
        )
        
        content = response.choices[0].message.content
        # Parse JSON from content
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Fallback if it contains markdown code blocks
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
                return json.loads(content)
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
                return json.loads(content)
            return {"error": "Failed to parse JSON response", "raw_content": content}
            
    except Exception as e:
        traceback.print_exc()
        return {}