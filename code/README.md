# 🚀 AI-Based Email Classification and OCR

## 📌 Project Overview
This project automates email classification and OCR-based text extraction for banking service requests. The AI model processes emails, classifies them into predefined request types, and extracts key information from email bodies and attachments.

## 📂 Folder Structure
📂 email_classifier
│── 📂 src
│   │── 📜 main.py                # Main entry point
│   │── 📜 universal_reader.py     # Reads .pdf, .docx, and .eml files
│   │── 📜 pdf_doc_reader.py       # Handles .pdf and .docx files
│   │── 📜 eml_reader.py           # Handles .eml files
│   │── 📜 classifier.py           # Uses Mistral-7B for classification
│   │── 📜 ocr_extractor.py        # Extracts text using PaddleOCR
│   │── 📜 duplicate_checker.py    # Checks for duplicate emails
│   │── 📜 config_loader.py        # Loads request types from JSON
│── 📂 data
│   │── 📂 emails                  # Store .eml files here
│   │── 📂 documents               # Store .pdf and .docx files here
│── 📂 config
│   │── 📜 request_types.json       # Request type mappings
│── 📜 requirements.txt
│── 📜 README.md
