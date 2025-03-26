# 🚀 Generative AI Email Classification and OCR Solution

## 📌 Table of Contents
- [Introduction](#introduction)
- [Demo](#demo)
- [Inspiration](#inspiration)
- [What It Does](#what-it-does)
- [How We Built It](#how-we-built-it)
- [Challenges We Faced](#challenges-we-faced)
- [How to Run](#how-to-run)
- [Tech Stack](#tech-stack)
- [Team](#team)

---

## 🎯 Introduction
Commercial Bank Lending service teams receive a high volume of servicing requests via email. These emails often contain diverse requests and attachments, which are ingested into the loan servicing platform to create service requests (SRs). These SRs then go through workflow processing.

The challenge is to automate email classification and data extraction using Generative AI (LLMs), improving efficiency, accuracy, and turnaround time while minimizing manual intervention. 
## 🎥 Demo
🔗 [Live Demo](#) (if applicable)  
📹 [Video Demo](#) (if applicable)  
🖼️ Screenshots:

![Screenshot 2025-03-26 at 3 35 21 PM](https://github.com/user-attachments/assets/3e0da19b-ad98-4dc3-b3c5-0235326b27a9)


1. Single Email/pdf File Classification

![Screenshot 2025-03-26 at 5 49 09 PM](https://github.com/user-attachments/assets/12fbe4b9-de96-41e7-9cb4-02f71dd46aa9)



2. Bulk File/Folder Classification

![Screenshot 2025-03-26 at 3 39 02 PM](https://github.com/user-attachments/assets/9e4e70ce-2fa3-4be8-98ed-a2ac749b8905)


![Screenshot 2025-03-26 at 5 51 11 PM](https://github.com/user-attachments/assets/fb724cc6-b89e-4d44-86ef-e5ad3b4c15eb)



## 💡 Inspiration
Manual email triage is time-consuming, inefficient, and prone to errors. Automating this process with AI can drastically improve accuracy and reduce turnaround time.

## ⚙️ What It Does

- Classifies emails into predefined request types and sub-request types based on sender intent.

- Extracts contextual data like deal name, amount, expiration date, etc.

- Handles multi-intent emails, determining the primary request type.

- Implements priority-based extraction, prioritizing email content over attachments.

- Detects duplicate emails, preventing redundant service requests.

## 🛠️ How We Built It


- LLM-Based Email Classification

   1. Using Mistral-7B-Instruct for request type classification.

   2. Handling multi-intent emails with primary request detection.

   Why Mistral-7B:

   ✅ Balanced performance & cost (open-source, no API fees).
   
   ✅ Great instruction following (handles structured classification well).
   
   ✅ Fast inference (low-latency, suitable for batch processing).
   
   ✅ Handles complex email reasoning (multi-intent detection + primary intent extraction).
   
   ✅ Can be fine-tuned/customized for banking request types.
   

- Context-Based Data Extraction

   1. Using DistilBERT/Mistral-7B for extracting fields like deal name, amount, expiration date.

   2. Implementing priority-based extraction (email body first, numerical values from attachments).

- OCR for Document Processing

   1. Using PaddleOCR for text extraction from attachments.

- Duplicate Detection

   1. Using **hash-based exact matching** and **similarity-based soft matching**.

- RAG for Dynamic Learning ( Future State)

   1. Storing request type definitions, past examples, and extraction rules in a vector database (FAISS/ChromaDB).

   2. Using hybrid retrieval + LLM classification to refine request types dynamically.

- Scalability & Explainability

   1. Batch processing for efficiency.

   2. Confidence scoring for classification reliability.


## 🚧 Challenges We Faced

- Handling multi-intent emails accurately.

- Ensuring scalability for large datasets.

- Fine-tuning confidence scoring for classification accuracy.

- Optimizing processing time for real-time response.

## 🏃 How to Run
1. Clone the repository  
   ```sh
    git clone https://github.com/ewfx/gaied-digitans.git
    cd gaied-digitans
     ```
2. Update Hugging Face api key as below. At this moment, I added acces key of mine. Pls generate one by following below instructions
   ```sh
   https://huggingface.co/docs/hub/en/security-tokens
   export HUGGINGFACE_API_KEY=your_hugging_face_api_key_here #macOS
   set HUGGINGFACE_API_KEY=your_hugging_face_api_key_here  # Windows OS
     ```
  
3. Navigate to src folder
   ```sh
   cd code/src
   ```
4. Create a Virtual Environment
   Set up a virtual environment to isolate dependencies:
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```
5. Install dependencies  
   ```sh
   pip install -r requirements.txt (for Python)
   ```
6. Run the project
   Start the FastAPI application using uvicorn:
   ```sh
    uvicorn main:app --reload
   ```
7. Test the Application
   You can test the application by navigating to the FastAPI interactive docs at:
   ```sh
   http://127.0.0.1:8000/docs - Swagger Docs
   http://127.0.0.1:8000  -- UI Testing
   ```
## 🏗️ Tech Stack
- 🔹 Frontend: React, BootStrap, HTML, CSS
- 🔹 Backend: Python Fast API 
- 🔹 Database: In memory, Chroma DB
- 🔹 AI & NLP : Mistral-7B
- 🔹 Document Processing  : eml-parser, paddleocr ,pdfplumber,python-docx
- 

## 👥 Team
- **Tejavardhan Reddy Meedimale** - [GitHub](#tejamvreddy) | [LinkedIn](#)
- **Raghavendra Pabbisetty** - [GitHub](#praghu1980) | [LinkedIn](#)
