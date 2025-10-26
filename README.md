# Kyral MediChat AI Assistant

Kyral's AI-powered medical diagnosis assistant built with Streamlit and AWS Bedrock. This application helps analyze patient symptoms and provides potential diagnoses with confidence scores, reasoning, and recommended actions.

## Features

- User-friendly form interface for patient information
- Integration with AWS Bedrock's Llama 3 model for medical analysis
- Access control via unique access keys with usage tracking
- Admin panel for managing user access and viewing submission statistics
- Comprehensive data collection including:
  - Basic patient information
  - Symptoms and medical history
  - Vital signs
  - Lifestyle factors

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

3. Configure environment variables:
   - Copy `.env.template` to `.env`
   - Add your AWS credentials and MySQL RDS configuration:
     ```
     AWS_ACCESS_KEY_ID=your_access_key_here
     AWS_SECRET_ACCESS_KEY=your_secret_key_here
     AWS_REGION=your_region_here
     
     DB_HOST=your_rds_endpoint_here
     DB_USER=your_db_username_here
     DB_PASSWORD=your_db_password_here
     DB_NAME=medichat_db
     DB_PORT=3306
     ```

4. Set up MySQL database:
   - Create a MySQL database on RDS named `medichat_db`
   - The application will automatically create the required tables on first run using SQLAlchemy ORM

5. Create initial admin user:
   - Run the seed script to create your first admin user:
     ```bash
     python seed_admin.py [your-email@domain.com]
     ```
   - The email parameter is optional but recommended for reference
   - This will generate and display an admin access key
   - Keep this key safe as it's needed to access the admin panel

6. Run the application:
```bash
streamlit run app.py
```

## Access Control

- Users access the application using unique access keys
- Admins can generate new keys and manage user access through the Admin panel
- Access can be revoked by deactivating keys
- Optional email association for tracking which users have been granted access

## Database Migration

If you have existing users in the database, the new `submission_count` column will be added automatically when the app starts. Existing users will start with a submission count of 0.

## Project Structure

- `app.py` - Main Streamlit application
- `utils/`
  - `bedrock.py` - AWS Bedrock integration
  - `db.py` - SQLAlchemy ORM database functions
- `requirements.txt` - Project dependencies
- `.env.template` - Template for environment variables

## Usage

1. Enter your access key to log in
2. Fill out the patient information form with all required fields
3. Click "Submit and View Results" to process the information
4. Review the analysis results in the following tabs:
   - Diagnoses: View potential conditions with confidence scores and reasoning
   - Recommendations: See suggested actions, tests, and lifestyle changes
5. Admins can access the Admin panel to manage users:
   - Generate new access keys with optional email association
   - View all users with their email, role, status, and submission count
   - Deactivate/reactivate user access instantly

## Important Note

This application is for informational purposes only and should not replace professional medical advice. Always consult with qualified healthcare professionals for medical diagnosis and treatment.

## License

[Apache 2.0 License](LICENSE)
