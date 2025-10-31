# Kyral MediChat AI Assistant (Beta)

Kyral's AI-powered medical diagnosis assistant built with Streamlit and AWS Bedrock. This application helps analyze patient symptoms and provides potential diagnoses with confidence scores, reasoning, insights and recommended actions. MediChat is self-hosted on AWS, private and secure. 

## Features

- **Multiple Input Methods:**
  - Manual form entry for patient symptoms, existing conditions, medications, and lab results
  - **PDF Upload:** Upload single or multiple patient medical record PDFs - AI analyzes documents directly for comprehensive diagnosis
- Integration with AWS Bedrock's Llama-3.3-70B model for medical analysis, insights and recommendations
- Comprehensive data fields for analysis include:
  - Basic patient information
  - Symptoms and medical history
  - Vital signs (Optional)
  - Lifestyle factors (Optional)
- Direct PDF-to-diagnosis workflow for faster analysis
 
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

- `app.py` - Main Streamlit application with manual and PDF input options
- `utils/`
  - `bedrock.py` - AWS Bedrock integration for medical analysis
  - `pdf_processor.py` - PDF text extraction and patient data parsing utilities
- `requirements.txt` - Project dependencies
- `.env.template` - Template for environment variables

## Usage

### Manual Entry
1. Select "📝 Manual Entry (Fill Form)" option
2. Fill out the patient information form with all required fields
3. Click "Analyze Symptoms" to process the information
4. Review the analysis results in the following tabs:
   - Diagnoses: View potential conditions with confidence scores and reasoning
   - Insights: See suggested actions, tests, and lifestyle changes

### PDF Upload
1. Select "📄 Upload PDF (Patient Records)" option
2. Upload one or more PDF files containing patient medical records
   - Multiple files can be selected simultaneously
   - All files will be processed together for comprehensive analysis
3. Click "🔍 Extract & Analyze PDF(s)" to process the documents
4. The AI will automatically:
   - Extract text from all uploaded PDFs
   - Add clear file separators between multiple documents
   - Analyze the complete medical records directly with AI
   - Generate diagnoses, insights, and recommendations based on all files
5. Review the comprehensive analysis results

## Important Note

This application is for informational purposes only and should not replace professional medical advice. Always consult with qualified healthcare professionals for medical diagnosis and treatment.

## License

[Apache 2.0 License](LICENSE)
