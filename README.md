# Medical Diagnosis Assistant

An AI-powered medical diagnosis assistant built with Streamlit and AWS Bedrock. This application helps analyze patient symptoms and provides potential diagnoses with confidence scores, reasoning, and recommended actions.

## Features

- User-friendly form interface for patient information
- Integration with AWS Bedrock's Llama 3 model for medical analysis
- Interactive visualization of diagnosis confidence scores
- PDF export functionality for analysis results
- Comprehensive data collection including:
  - Basic patient information
  - Symptoms and medical history
  - Vital signs
  - Lifestyle factors

## Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd medical-ai-chat
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
  - `pdf_export.py` - PDF report generation
- `requirements.txt` - Project dependencies
- `.env.template` - Template for environment variables

## Usage

1. Fill out the patient information form with all required fields
2. Click "Analyze Symptoms" to process the information
3. Review the analysis results in the following tabs:
   - Diagnoses: View potential conditions with confidence scores and reasoning
   - Recommendations: See suggested actions, tests, and lifestyle changes
   - Export: Generate and download a PDF report of the analysis

## Important Note

This application is for informational purposes only and should not replace professional medical advice. Always consult with qualified healthcare professionals for medical diagnosis and treatment.

## License

[MIT License](LICENSE)
