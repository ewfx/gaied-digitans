import io
import filetype
import pdfplumber
from docx import Document
import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes


def extract_text_from_bytes(file_bytes, filename):
    """
    Extracts text from file content (without saving).
    Supports PDF, DOCX, and images.
    """
    kind = filetype.guess(file_bytes)
    
    if kind is None:
        return "Unknown file type"
    
    if kind.mime == "application/pdf":
        return extract_text_from_pdf(file_bytes)
    elif kind.mime == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return extract_text_from_docx(file_bytes)
    elif "image" in kind.mime:
        return extract_text_from_image(file_bytes)
    else:
        return "Unsupported file format"

def extract_text_from_pdf(file_bytes):
    text = ""
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text.strip()

def extract_text_from_docx(file_bytes):
    text = ""
    doc = Document(io.BytesIO(file_bytes))
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text.strip()

def extract_text_from_image(file_bytes):
    image = Image.open(io.BytesIO(file_bytes))
    text = pytesseract.image_to_string(image)
    return text.strip()
