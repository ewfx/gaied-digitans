import os
import email
import chardet
from email import policy
from email.parser import BytesParser
from services.document_reader import read_document

def parse_email(file_path):
    """
    Parses an email file (.eml) to extract the email body and attachments.
    
    Returns:
        email_text (str): Extracted text from the email body.
        attachment_text (str): Extracted text from all readable attachments.
    """
    email_text = ""
    attachment_text = ""

    try:
        # Read email file
        with open(file_path, "rb") as f:
            raw_data = f.read()
        
        # Detect encoding and decode
        encoding = chardet.detect(raw_data)['encoding']
        encoding = encoding if encoding else 'utf-8'

        # Parse email using BytesParser
        msg = BytesParser(policy=policy.default).parsebytes(raw_data)

        # Extract email body (supports plain text and HTML fallback)
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                # Extract text/plain content
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    email_text += part.get_payload(decode=True).decode(encoding, errors="ignore") + "\n"
        else:
            email_text = msg.get_payload(decode=True).decode(encoding, errors="ignore")

        # Extract attachments and process readable documents
        for part in msg.walk():
            content_disposition = str(part.get("Content-Disposition"))
            if "attachment" in content_disposition:
                filename = part.get_filename()
                if filename:
                    temp_file_path = os.path.join("temp", filename)
                    os.makedirs("temp", exist_ok=True)

                    # Save attachment temporarily
                    with open(temp_file_path, "wb") as f:
                        f.write(part.get_payload(decode=True))

                    # Read document content (PDF, DOCX, etc.)
                    extracted_text = read_document(temp_file_path)
                    attachment_text += extracted_text + "\n"

                    # Cleanup temporary file
                    os.remove(temp_file_path)

    except Exception as e:
        print(f"Error parsing email: {e}")

    return email_text.strip(), attachment_text.strip()
