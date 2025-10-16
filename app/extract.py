"""
Text extraction module for PDFs and plain text
"""

import io
from typing import Union
import PyPDF2


def extract_from_pdf(file_content: bytes) -> str:
    """
    Extract text from PDF file using PyPDF2.
    
    Args:
        file_content: PDF file content as bytes
        
    Returns:
        Extracted text as string
        
    Raises:
        Exception: If PDF extraction fails
    """
    try:
        pdf_file = io.BytesIO(file_content)
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        
        if not text.strip():
            raise Exception("No text could be extracted from PDF")
        
        return text
    
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")


def extract_from_text(text: str) -> str:
    """
    Handle plain text input.
    
    Args:
        text: Plain text string
        
    Returns:
        The input text (for consistency)
    """
    if not text or not text.strip():
        raise ValueError("Text is empty")
    
    return text


def extract_text(content: Union[bytes, str], is_pdf: bool = False) -> str:
    """
    Universal text extraction function.
    
    Args:
        content: File content (bytes) or text (str)
        is_pdf: Whether the content is a PDF file
        
    Returns:
        Extracted text
        
    Raises:
        Exception: If extraction fails
    """
    if is_pdf:
        if not isinstance(content, bytes):
            raise ValueError("PDF content must be bytes")
        return extract_from_pdf(content)
    else:
        if isinstance(content, bytes):
            text_content = content.decode('utf-8', errors='ignore')
            return extract_from_text(text_content)
        elif isinstance(content, str):
            return extract_from_text(content)
        else:
            raise ValueError("Content must be bytes or str")
