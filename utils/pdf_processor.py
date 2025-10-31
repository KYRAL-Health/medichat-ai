import pymupdf
import traceback


def extract_text_from_pdf(pdf_file) -> str:
    """
    Extract all text content from a PDF file.
    
    Args:
        pdf_file: File-like object or bytes from uploaded PDF
        
    Returns:
        str: Extracted text from all pages
    """
    try:
        # Open PDF from bytes
        pdf_document = pymupdf.open(stream=pdf_file.read(), filetype="pdf")
        
        # Extract text from all pages
        full_text = ""
        for page_num in range(pdf_document.page_count):
            page = pdf_document[page_num]
            full_text += page.get_text()
            full_text += "\n\n--- Page Break ---\n\n"
        
        pdf_document.close()
        return full_text
    except Exception as e:
        traceback.print_exc()
        raise Exception(f"Error extracting text from PDF: {str(e)}")
