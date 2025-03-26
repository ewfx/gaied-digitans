import os
import pdfplumber
import docx
import chardet
import mimetypes
from fastapi import HTTPException
from docx import Document
from docx.opc.exceptions import PackageNotFoundError

def read_pdf(file_path):
    """Extracts text from a PDF file."""
    text = ""
    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n" if page.extract_text() else ""
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text.strip()

def is_valid_docx(file_path: str) -> bool:
    """
    Validates if the file is a valid DOCX based on its MIME type.
    """
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"

def extract_text_from_docx(file_path: str) -> str:
    """
    Extracts text from a DOCX file.
    """
    try:
        doc = Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    except PackageNotFoundError as e:
        print(f"Corrupted DOCX file: {e}")
        raise HTTPException(status_code=400, detail="The uploaded DOCX file is corrupted or invalid.")
    except Exception as e:
        print(f"Error extracting text from DOCX: {e}")
        raise HTTPException(status_code=400, detail="Failed to extract text from DOCX.")

def read_txt(file_path):
    """Reads text from a plain text file (handles encoding detection)."""
    text = ""
    try:
        with open(file_path, "rb") as f:
            raw_data = f.read()
            encoding = chardet.detect(raw_data)['encoding']
            encoding = encoding if encoding else 'utf-8'
            text = raw_data.decode(encoding, errors="ignore")
    except Exception as e:
        print(f"Error reading TXT: {e}")
    return text.strip()

def read_document(file_path):
    """
    Detects file type and extracts text accordingly.
    
    Supported formats: PDF, DOCX, TXT
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return ""

    file_extension = os.path.splitext(file_path)[1].lower()

    if file_extension == ".pdf":
        return read_pdf(file_path)
    elif file_extension == ".docx":
        return extract_text_from_docx(file_path)
    elif file_extension == ".txt":
        return read_txt(file_path)
    else:
        print(f"Unsupported file format: {file_extension}")
        return ""
