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


Single Email/pdf File Classification

![Screenshot 2025-03-26 at 3 35 51 PM](https://github.com/user-attachments/assets/6385a10b-bea8-4eb3-a0de-c3865a43eeaa)


Bulk File/Folder Classification

![Screenshot 2025-03-26 at 3 39 02 PM](https://github.com/user-attachments/assets/9e4e70ce-2fa3-4be8-98ed-a2ac749b8905)


## 💡 Inspiration
Manual email triage is time-consuming, inefficient, and prone to errors. Automating this process with AI can drastically improve accuracy and reduce turnaround time.

## ⚙️ What It Does

- Classifies emails into predefined request types and sub-request types based on sender intent.

- Extracts contextual data like deal name, amount, expiration date, etc.

- Handles multi-intent emails, determining the primary request type.

- mplements priority-based extraction, prioritizing email content over attachments.

- Detects duplicate emails, preventing redundant service requests.

## 🛠️ How We Built It

- LLMs (Mistral-7B, GPT, LLaMA, Gemini) for request classification.

- DistilBERT & PaddleOCR for structured field extraction and OCR.

- FastAPI & React for backend and frontend development.

- Scikit-learn, Pandas, LangChain for data processing.

- In Memory Database for duplicate detection



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
2. Navigate to src folder
   ```sh
   cd code/src
   ```
3. Create a Virtual Environment
   Set up a virtual environment to isolate dependencies:
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```
4. Install dependencies  
   ```sh
   pip install -r requirements.txt (for Python)
   ```
5. Run the project
   Start the FastAPI application using uvicorn:
   ```sh
    uvicorn main:app --reload
   ```
6. Test the Application
   You can test the application by navigating to the FastAPI interactive docs at:
   ```sh
   http://127.0.0.1:8000/docs - Swagger Docs
   http://127.0.0.1:8000  -- UI Testing
   ```
## 🏗️ Tech Stack
- 🔹 Frontend: React, BootStrap, HTML, CSS
- 🔹 Backend: Python Fast API 
- 🔹 Database: In memory, Chroma DB
- 🔹 AI & NLP : Mistral-7B by Hugging Face, scikit-learn , fuzzywuzzy
- 🔹 Document Processing  : eml-parser, paddleocr ,pdfplumber,python-docx
- 

## 👥 Team
- **Tejavardhan Reddy Meedimale** - [GitHub](#tejamvreddy) | [LinkedIn](#)
- **Raghavendra Pabbisetty** - [GitHub](#praghu1980) | [LinkedIn](#)
