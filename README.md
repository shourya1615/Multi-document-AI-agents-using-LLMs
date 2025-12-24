# AI Multi-Agent Document Intelligence System

A Flask-based multi-agent AI system that intelligently processes PDF and DOCX documents to provide summarization, contextual question answering, research explanations, and coding assistance using Groq-powered Llama models.

---

## 📌 Project Overview

Large documents such as research papers, technical manuals, and academic notes are difficult to navigate manually. Traditional PDF tools offer only basic text extraction and keyword search, lacking contextual understanding and reasoning.

This project addresses that gap by implementing a **multi-agent AI architecture**, where each agent is specialized for a specific task—summarization, research explanation, or code assistance. The system enables users to upload documents and interact with them through natural language queries.

The backend is built using **Flask**, with **Groq Llama models** providing ultra-fast inference and high-quality responses.

---

## 🚀 Key Features

- 📄 Upload and process **PDF** and **DOCX** files  
- 🧠 Multi-agent architecture with specialized roles  
- ✂️ Intelligent document summarization  
- ❓ Context-aware question answering  
- 📚 Research-style explanations  
- 💻 Coding help and explanations  
- 🔁 Multi-turn conversation with session memory  
- ⚡ Ultra-low latency responses using Groq Llama models  

---

## 🧩 System Architecture

The system follows a **modular multi-agent design**:

- **Flask Backend**  
  Handles routing, request handling, session management, and agent orchestration.

- **Document Processing Module**  
  Extracts text from PDF (PyPDF2) and DOCX (python-docx) files.

- **Summarizer Agent**  
  Generates structured summaries from uploaded documents.

- **Research Agent**  
  Provides conceptual explanations and deeper insights.

- **Code Agent**  
  Handles programming-related queries, explanations, and debugging.

- **Groq API (Llama Models)**  
  Powers all agents with fast and accurate language model inference.

- **Session Memory**  
  Maintains conversation context across multiple user interactions.

---

## 🛠️ Tech Stack

- **Backend:** Python, Flask  
- **LLM Provider:** Groq API (Llama-3.x models)  
- **Document Processing:** PyPDF2, python-docx  
- **Session Management:** Flask-Session  
- **Frontend:** HTML templates (Flask render)  
- **API Client:** Groq Python SDK  
---

⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

2️⃣ Create Virtual Environment (Recommended)
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Set Up Environment Variables

Create a .env file or export your Groq API key:

GROQ_API_KEY=your_api_key_here

▶️ Running the Application
python app.py


The application will start on:

http://localhost:5000
