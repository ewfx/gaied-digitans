import hashlib
import json
from difflib import SequenceMatcher

# Store past emails in a simple in-memory dictionary (can be replaced with a DB)
past_emails = {}

def generate_hash(email_text, extracted_fields):
    """
    Generates a hash based on email content and extracted structured fields.
    """
    hash_input = email_text + json.dumps(extracted_fields, sort_keys=True)
    email_hash = hashlib.sha256(hash_input.encode()).hexdigest()
    return email_hash

def is_duplicate(email_text, extracted_fields):
    """
    Checks if the given email is a duplicate based on hash and similarity.
    """
    email_hash = generate_hash(email_text, extracted_fields)

    # Direct duplicate check
    if email_hash in past_emails:
        return {
            "is_duplicate": True,
            "reason": "Exact duplicate detected based on hash.",
            "duplicate_of": past_emails[email_hash]
        }

    # Check for soft duplicates using similarity
    for past_email, past_hash in past_emails.items():
        similarity = SequenceMatcher(None, email_text, past_email).ratio()
        if similarity > 0.90:  # 90% similarity threshold
            return {
                "is_duplicate": True,
                "reason": f"Soft duplicate detected with {similarity * 100:.2f}% similarity.",
                "duplicate_of": past_hash
            }

    # If not duplicate, store and return false
    past_emails[email_text] = email_hash
    return {"is_duplicate": False}
