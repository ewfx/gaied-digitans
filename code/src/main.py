from fastapi import FastAPI, Request, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from services.email_parser import parse_email
from services.classifier import classify_and_extract
from services.duplicate_checker import is_duplicate
from services.field_extractor import extract_fields
from services.document_reader import read_pdf, extract_text_from_docx
import uvicorn
import os
import shutil

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Serve static files (e.g., CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Enable CORS (optional, for frontend integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to restrict origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ClassificationResponse(BaseModel):
    filename: str
    content_summary: Optional[str] = None  # Summary of the file content
    request_type: Optional[str] = None  # Allow None
    sub_request_type: Optional[str] = None  # Allow None
    extracted_fields: dict = {}  # Default to an empty dictionary
    duplicate_detected: object
    confidence_score: Optional[float] = None  # Confidence score for classification
    error: Optional[str] = None  # Allow None

@app.get("/", response_class=HTMLResponse)
async def render_ui(request: Request):
    """
    Render the UI page for file or folder upload.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload_and_classify_file/", response_model=ClassificationResponse)
async def upload_and_classify_file(file: UploadFile = File(...)):
    try:
        # Save the uploaded file temporarily
        temp_file_path = f"temp/{file.filename}"
        os.makedirs("temp", exist_ok=True)
        with open(temp_file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Step 1: Parse file based on its type
        email_text = ""
        attachment_text = ""
        content_summary = ""

        if file.filename.endswith(".eml"):
            email_text, attachment_text = parse_email(temp_file_path)
            content_summary = email_text[:200]  # First 200 characters as a summary
        elif file.filename.endswith(".pdf"):
            email_text = read_pdf(temp_file_path)
            content_summary = email_text[:200]  # First 200 characters as a summary
        elif file.filename.endswith(".docx"):
            email_text = extract_text_from_docx(temp_file_path)
            content_summary = email_text[:200]  # First 200 characters as a summary
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file.filename}")

        # Step 2: Classify and extract fields
        classification_result = classify_and_extract(email_text, attachment_text)

        if "error" in classification_result:
            return ClassificationResponse(
                filename=file.filename,
                content_summary=content_summary,
                request_type=None,
                sub_request_type=None,
                extracted_fields={},  # Set to an empty dictionary
                duplicate_detected=None,
                confidence_score=None,
                error=classification_result["error"]
            )

        classification = classification_result.get("classification", {})
        request_type = classification.get("request_type")
        sub_request_type = classification.get("sub_request_type")
        confidence_score = classification_result.get("confidence_score")

        # Extract structured fields based on request type and sub-request type
        extracted_fields = {}
        if request_type and sub_request_type:
            extracted_fields = extract_fields(email_text, request_type, sub_request_type)

        # Step 3: Check for duplicates
        duplicate_detected = is_duplicate(email_text, extracted_fields)

        # Return the result for this file
        return ClassificationResponse(
            filename=file.filename,
            content_summary=content_summary,
            request_type=request_type,
            sub_request_type=sub_request_type,
            extracted_fields=extracted_fields,
            duplicate_detected=duplicate_detected,
            confidence_score=confidence_score,
            error=None
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the file: {str(e)}")

    finally:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.post("/upload_and_classify_folder/", response_model=List[ClassificationResponse])
async def upload_and_classify_folder(folder: UploadFile = File(...)):
    """
    API to process a folder of uploaded email files, classify them, extract fields, and check for duplicates.
    Supports .eml (email), .pdf, .docx, and .doc formats.
    """
    results = []

    # Save the uploaded folder temporarily
    temp_folder_path = "temp_folder"
    os.makedirs(temp_folder_path, exist_ok=True)

    try:
        # Save the uploaded folder as a zip file
        zip_file_path = f"{temp_folder_path}/uploaded_folder.zip"
        with open(zip_file_path, "wb") as buffer:
            buffer.write(await folder.read())

        # Extract the zip file
        shutil.unpack_archive(zip_file_path, temp_folder_path)

        # Process each file in the extracted folder
        for root, _, files in os.walk(temp_folder_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)

                try:
                    # Step 1: Parse file based on its type
                    email_text = ""
                    attachment_text = ""
                    content_summary = ""

                    if file_name.endswith(".eml"):
                        email_text, attachment_text = parse_email(file_path)
                        content_summary = email_text[:200]  # First 200 characters as a summary
                    elif file_name.endswith(".pdf"):
                        email_text = read_pdf(file_path)
                        content_summary = email_text[:200]  # First 200 characters as a summary
                    elif file_name.endswith(".docx"):
                        email_text = extract_text_from_docx(file_path)
                        content_summary = email_text[:200]  # First 200 characters as a summary
                    else:
                        results.append({
                            "filename": file_name,
                            "content_summary": None,
                            "request_type": None,
                            "sub_request_type": None,
                            "extracted_fields": {},  # Set to an empty dictionary
                            "duplicate_detected": None,
                            "confidence_score": None,
                            "error": f"Unsupported file type: {file_name}"
                        })
                        continue

                    # Step 2: Classify and extract fields
                    classification_result = classify_and_extract(email_text, attachment_text)

                    if "error" in classification_result:
                        results.append({
                            "filename": file_name,
                            "content_summary": content_summary,
                            "request_type": None,
                            "sub_request_type": None,
                            "extracted_fields": {},  # Set to an empty dictionary
                            "duplicate_detected": None,
                            "confidence_score": None,
                            "error": classification_result["error"]
                        })
                        continue

                    classification = classification_result.get("classification", {})
                    request_type = classification.get("request_type")
                    sub_request_type = classification.get("sub_request_type")
                    confidence_score = classification_result.get("confidence_score")

                    # Extract structured fields based on request type and sub-request type
                    extracted_fields = {}
                    if request_type and sub_request_type:
                        extracted_fields = extract_fields(email_text, request_type, sub_request_type)

                    # Step 3: Check for duplicates
                    duplicate_detected = is_duplicate(email_text, extracted_fields)

                    # Append the result for this file
                    results.append({
                        "filename": file_name,
                        "content_summary": content_summary,
                        "request_type": request_type,
                        "sub_request_type": sub_request_type,
                        "extracted_fields": extracted_fields,  # Ensure this is always a dictionary
                        "duplicate_detected": duplicate_detected,
                        "confidence_score": confidence_score,
                        "error": None
                    })

                except Exception as e:
                    # Handle errors for individual files
                    results.append({
                        "filename": file_name,
                        "content_summary": None,
                        "request_type": None,
                        "sub_request_type": None,
                        "extracted_fields": {},  # Set to an empty dictionary
                        "duplicate_detected": None,
                        "confidence_score": None,
                        "error": f"An error occurred while processing the file: {str(e)}"
                    })

    except Exception as e:
        # Log the general error but do not stop processing
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

    finally:
        # Clean up the temporary folder
        shutil.rmtree(temp_folder_path, ignore_errors=True)

    return results

# Start the server when running the script directly
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
