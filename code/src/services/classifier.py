import os
import json
import requests
import re
from utils.config_loader import get_valid_request_types
from services.field_extractor import extract_fields
from services.duplicate_checker import is_duplicate

# Load Hugging Face API Key from Environment Variable
HUGGINGFACE_API_KEY = "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"
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

HEADERS = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
    "Content-Type": "application/json"
}

def extract_json_from_response(response_text):
    """
    Extracts and parses a valid JSON object from the response text using regex.
    Handles cases where extra text exists before or after the JSON.
    """
    try:
        # Use regex to find all JSON-like objects
        matches = re.findall(r"\{.*?\}", response_text, re.DOTALL)

        if not matches:
            raise ValueError("No valid JSON found in response.")

        # Try parsing the last JSON block (assuming it's the actual structured output)
        for match in reversed(matches):
            try:
                return json.loads(match)
            except json.JSONDecodeError:
                continue  # Skip invalid matches

        raise ValueError("Failed to parse extracted JSON.")

    except Exception as e:
        raise ValueError(f"Error extracting JSON: {str(e)}")


def extract_classification_from_response(response_text):
    """
    Extracts classification details (request_type, sub_request_type, confidence_score, reasoning)
    from the plain text response.
    Handles cases where the response contains plain text key-value pairs or additional explanatory text.
    """
    try:
        # Define possible markers
        markers = [
            "Based on the given email content, the correct JSON response is:",
            "Do not include any additional text, explanation, or formatting outside the JSON block."
        ]

        # Locate the specific phrase and extract the JSON block that follows it
        for marker in markers:
            if marker in response_text:
                response_text = response_text.split(marker, 1)[1].strip()  # Extract text after the marker
                break

        # Use regex to find the first valid JSON block
        json_match = re.search(r"(\{.*?\})", response_text, re.DOTALL)
        if json_match:
            json_text = json_match.group(0).strip()  # Extract the JSON substring
            print("Extracted JSON text:", json_text)  # Debugging log
            try:
                classification_result = json.loads(json_text)  # Parse the JSON
                return classification_result
            except json.JSONDecodeError as e:
                raise ValueError(f"Error parsing JSON: {str(e)}")

        # If no valid JSON block is found, raise an error
        raise ValueError("No valid JSON block found in response.")

    except Exception as e:
        raise ValueError(f"Error extracting classification details: {str(e)}")


def classify_and_extract(email_text: str, attachment_text: str = ""):
    """
    Accurately extracts, interprets the context, and categorizes emails into predefined request types
    and sub-request types based on the sender's intent along with reasoning.
    """
    valid_request_types = get_valid_request_types()

    # Construct the prompt for classification
    classification_prompt = f"""
    You are an AI assistant for commercial loans bank servicing team automation. 
    Your task is to classify the given email into a predefined request type and sub-request type.

    Email Content:
    {email_text}

    Attachments Content:
    {attachment_text}

    Based on the above content, determine the correct 'Request Type' and 'Sub Request Type' from this predefined list:
    {json.dumps(valid_request_types, indent=2)}

    Output Format:
    Provide the output strictly in the following JSON format:
    {{
        "request_type": "string",
        "sub_request_type": "string",
        "confidence_score": integer,
        "reasoning": "string"
    }}

    Do not include any additional text, explanation, or formatting outside the JSON block.
    """

    try:
        # Send the request to the Hugging Face API
        response = requests.post(API_URL, headers=HEADERS, json={"inputs": classification_prompt}, timeout=30)

        # Handle HTTP errors
        if response.status_code != 200:
            return {
                "error": "API request failed",
                "status_code": response.status_code,
                "response": response.text
            }

        # Parse JSON response from Hugging Face API
        result = response.json()

        print("response from model::", result)

        # Ensure the response contains 'generated_text'
        if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
            generated_text = result[0]["generated_text"]
            print("Generated text:", generated_text)
            try:
                classification_result = extract_classification_from_response(generated_text)

                # Handle case where classification_result is a list
                if isinstance(classification_result, list):
                    # Use the first valid result from the list
                    classification_result = classification_result[0]

            except ValueError as e:
                return {
                    "error": str(e),
                    "raw_response": generated_text
                }
        else:
            return {
                "error": "Unexpected response format from API",
                "response": result
            }

        # Get the classified request type and sub-request type
        request_type = classification_result.get("request_type", None)
        sub_request_type = classification_result.get("sub_request_type", None)
        confidence_score = classification_result.get("confidence_score", None)
        reasoning = classification_result.get("reasoning", None)

        print("Request Type:", request_type)
        print("Sub Request Type:", sub_request_type)
        print("Confidence Score:", confidence_score)
        print("Reasoning:", reasoning)

        # Extract structured fields based on request type and sub-request type
        extracted_fields = {}
        if request_type and sub_request_type:
            extracted_fields = extract_fields(email_text, request_type, sub_request_type)

        print("Extracted Fields:", extracted_fields)

        # Final response structure
        final_result = {
            "classification": {
                "request_type": request_type,
                "sub_request_type": sub_request_type,
                "confidence_score": confidence_score,
                "reasoning": reasoning
            },
            "extracted_fields": extracted_fields
        }

        return final_result

    except requests.exceptions.RequestException as e:
        return {"error": "Request to Hugging Face API failed", "details": str(e)}

    except Exception as e:
        return {"error": "Unexpected error occurred", "details": str(e)}
