# Kyral AI Health Companion (Pre-Alpha)

Kyral's AI-powered medical diagnosis assistant built with Streamlit and AWS Bedrock. This application helps analyze patient symptoms and provides potential diagnoses with confidence scores, reasoning, insights and recommended actions. MediChat is self-hosted on AWS, private and secure. 

## Features

- User-friendly form interface to provide patient symptoms, existing conditions, medications, and/or lab results.
- Integration with AWS Bedrock's Llama-3.3-70B model for medical analysis, insights and recommendations.
- Comprehensive data fields for analysis include:
  - Basic patient information
  - Symptoms and medical history
  - Vital signs (Optional)
  - Lifestyle factors (Optional)
 
## Privacy and Data Collection
- No data is stored following submission for analysis
- No data is used for model training or fine-tuning
- No user data is sold or used for any other purposes

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd medichat-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure AWS credentials:
   - Copy `.env.template` to `.env`
   - Add your AWS credentials and configuration:
     ```
     AWS_ACCESS_KEY_ID=your_access_key_here
     AWS_SECRET_ACCESS_KEY=your_secret_key_here
     AWS_REGION=your_region_here
     ```

4. Run the application:
```bash
streamlit run app.py
```

## Project Structure

- `app.py` - Main Streamlit application
- `utils/`
  - `bedrock.py` - AWS Bedrock integration
- `requirements.txt` - Project dependencies
- `.env.template` - Template for environment variables

## Usage

1. Fill out the patient information form with all required fields
2. Click "Analyze Symptoms" to process the information
3. Review the analysis results in the following tabs:
   - Diagnoses: View potential conditions with confidence scores and reasoning
   - Insights: See suggested actions, tests, and lifestyle changes

## Important Note

This application is for informational purposes only and should not replace professional medical advice. Always consult with qualified healthcare professionals for medical diagnosis and treatment.

## License

[Apache 2.0 License](LICENSE)
