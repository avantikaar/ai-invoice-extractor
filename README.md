# 🤖 Enterprise AI Invoice & Document Extractor  Live demo link : https://ai-invoice-extractor-jfsdcssqxj9pqnhrrrrvb3.streamlit.app/

An enterprise-grade Accounts Payable (AP) automation MVP that leverages Large Language Models (LLMs) to extract structured data from unstructured invoice PDFs. The system features a REST API backend, relational database, Role-Based Access Control (RBAC), and an analytics dashboard for approval workflows.

## 📌 Overview
Manual invoice data entry is a bottleneck for enterprise finance teams. This project serves as a proof-of-concept for an AI-driven document processing pipeline. It ingests raw invoice PDFs, uses AI to extract key fields, stores the structured data in a normalized SQL database, and provides a secure dashboard for administrators to approve or reject invoices.

## 🚀 Key Features
- **AI Document Extraction:** Utilizes Google Gemini 2.5 Flash and advanced prompt engineering to extract Vendor Name, Invoice Number, Date, and Total Amount from PDF files.
- **REST API Layer:** FastAPI backend exposes endpoints for invoice CRUD operations, enabling decoupled frontend/backend architecture.
- **Role-Based Access Control (RBAC):** Secure enterprise workflow with distinct `Admin` and `Viewer` roles.
- **Relational Database Architecture:** Normalized SQL schema with dynamic SQL queries for filtering, reporting, and audit trails.
- **KPI & Analytics Dashboard:** Real-time metrics and vendor spend analytics using Altair.
- **Dockerized Deployment:** Containerized with Docker and Docker Compose for consistent environments.
- **CI/CD Pipeline:** GitHub Actions workflow for automated syntax and dependency checks.

## 🛠️ Tech Stack
- **Frontend:** Streamlit, Altair
- **Backend:** Python, FastAPI, REST APIs
- **Database:** SQLite (Relational), SQL (Joins, Aggregations, Filtering)
- **AI / LLM:** Google Gemini API (`google-genai` SDK), Prompt Engineering
- **Data Processing:** Pandas, PyPDF
- **DevOps:** Docker, Docker Compose, GitHub Actions (CI/CD)
- **Version Control:** Git, GitHub

## ⚙️ Local Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/avantikaar/ai-invoice-extractor.git
   cd ai-invoice-extractor
