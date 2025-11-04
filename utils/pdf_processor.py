import PyPDF2
from typing import List
import io

def extract_text_from_pdf(pdf_file) -> str:
    """
    Extract text from a single PDF file.
    
    Args:
        pdf_file: A file-like object (from Streamlit's file_uploader)
        
    Returns:
        str: Extracted text from the PDF
    """
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text() + "\n"
        
        return text.strip()
    except Exception as e:
        return f"Error extracting text from PDF: {str(e)}"

def extract_text_from_multiple_pdfs(pdf_files: List) -> str:
    """
    Extract text from multiple PDF files.
    
    Args:
        pdf_files: List of file-like objects (from Streamlit's file_uploader)
        
    Returns:
        str: Combined extracted text from all PDFs
    """
    combined_text = []
    
    for idx, pdf_file in enumerate(pdf_files, 1):
        file_text = extract_text_from_pdf(pdf_file)
        combined_text.append(f"=== Document {idx}: {pdf_file.name} ===\n{file_text}\n")
    
    return "\n".join(combined_text)
