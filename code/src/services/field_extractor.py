import re
import json
import requests
import os
from dotenv import load_dotenv


# Load the field extraction configuration
with open("config/field_extraction_config.json", "r") as file:
    field_extraction_config = json.load(file)
load_dotenv()

# Hugging Face API Configuration
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
HEADERS = {
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
    "Content-Type": "application/json"
}

def extract_fields(email_text, request_type, sub_type):
    """
    Extract fields from the email text based on the request_type and sub_type.
    Uses regex for static fields and integrates LLM for dynamic field extraction.
    """
    # Determine the fields to extract based on request_type and sub_type
    key = f"{request_type} - {sub_type}"
    fields_to_extract = field_extraction_config.get(key, [])
    if not fields_to_extract:
        return {"error": f"No field extraction configuration found for {key}"}

    # Static field extraction using regex
    extracted_fields = {}
    if "deal_name" in fields_to_extract:
        deal_name = re.search(r"deal ID (\w+)", email_text)
        extracted_fields["deal_name"] = deal_name.group(1) if deal_name else None
    if "amount" in fields_to_extract:
        amount = re.search(r"\$(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)", email_text)
        extracted_fields["amount"] = float(amount.group(1).replace(',', '')) if amount else None

    # Dynamic field extraction using LLM
    dynamic_fields = [field for field in fields_to_extract if field not in extracted_fields]
    if dynamic_fields:
        llm_result = extract_dynamic_fields(email_text, dynamic_fields, request_type, sub_type)
        if "error" in llm_result:
            return llm_result
        extracted_fields.update(llm_result)

    return extracted_fields

def extract_dynamic_fields(email_text, fields, request_type, sub_type):
    """
    Use an LLM to dynamically extract fields from the email text.
    """
    # Construct the prompt for the LLM
    prompt = f"""
    You are an AI assistant for banking service automation.
    Your task is to extract the following fields from the given email content:

    Email Content:
    {email_text}

    Request Type: {request_type}
    Sub Request Type: {sub_type}

    Fields to extract: {fields}

    Provide the extracted fields in JSON format.
    """
    try:
        # Send the request to the Hugging Face API
        response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt}, timeout=30)

        # Handle API errors
        if response.status_code != 200:
            return {
                "error": "Failed to fetch results from LLM",
                "status_code": response.status_code,
                "response": response.text
            }

        # Parse the response
        result = response.json()
        if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
            generated_text = result[0]["generated_text"]
            print("Generated text from LLM:", generated_text)  # Debugging log

            # Extract the JSON block from the generated text
            try:
                # Use regex to extract the first valid JSON block
                json_match = re.search(r"\{.*?\}", generated_text, re.DOTALL)
                if json_match:
                    json_text = json_match.group(0)  # Extract the JSON substring

                    # Preprocess the JSON to replace single quotes with double quotes
                    json_text = json_text.replace("'", '"')

                    # Attempt to fix common JSON issues (e.g., missing closing braces)
                    if json_text.count("{") > json_text.count("}"):
                        json_text += "}" * (json_text.count("{") - json_text.count("}"))

                    # Parse the JSON
                    extracted_fields = json.loads(json_text)
                    return extracted_fields
                else:
                    return {"error": "No valid JSON block found in LLM response", "raw_response": generated_text}
            except json.JSONDecodeError as e:
                return {
                    "error": "Failed to parse JSON from LLM response",
                    "raw_json": json_text,
                    "exception": str(e)
                }

        else:
            return {"error": "Unexpected response format from LLM", "response": result}

    except requests.exceptions.RequestException as e:
        return {"error": "Request to LLM API failed", "details": str(e)}
