# 🛡️ Secure AI Vault - Enterprise Cloud System

![Python](https://img.shields.io/badge/Python-3.9-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.95-009688?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-1.22-FF4B4B?style=for-the-badge&logo=streamlit)
![Hugging Face](https://img.shields.io/badge/AI-Hugging%20Face-yellow?style=for-the-badge&logo=huggingface)
![Render](https://img.shields.io/badge/Deployment-Render-black?style=for-the-badge&logo=render)

## 🚀 Project Overview
**Secure AI Vault** is a full-stack cloud application designed to demonstrate secure integration of Artificial Intelligence APIs within an enterprise environment. It allows users to perform **Text Summarization** and **Sentiment Analysis** using state-of-the-art Hugging Face models, all protected by a robust **JWT Authentication** system.

This project was built to practice **DevSecOps principles**, focusing on secure API key management, Role-Based Access Control (RBAC), and cloud deployment.

## ✨ Key Features

### 🔐 Security & Authentication
* **JWT Authentication:** Secure Login and Signup system using JSON Web Tokens.
* **Password Hashing:** User passwords are encrypted using `bcrypt` before storage.
* **Secure Environment:** API keys are managed via Environment Variables (not hardcoded), preventing exposure.

### 🧠 AI Capabilities (Powered by Hugging Face)
* **📝 Smart Summarization:** Condenses long paragraphs into concise summaries using the `facebook/bart-large-cnn` model.
* **🎭 Mood Analysis:** Detects emotions (Positive/Negative) from text using the `distilbert-base-uncased` model.
* **Fault Tolerance:** Implemented a multi-URL fallback mechanism to ensure AI uptime even if primary API endpoints fail.

### 👮‍♂️ Admin & User Management
* **Admin Dashboard:** Dedicated panel for administrators to view all registered users.
* **User Control:** Ability to delete unauthorized or inactive users directly from the UI.
* **Scan History:** Automatically saves all AI analysis results to a database for audit trails.

## 🛠️ Tech Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend** | Streamlit | Interactive web UI for easy user interaction. |
| **Backend** | FastAPI | High-performance API for logic and security. |
| **Database** | SQLite + SQLModel | Lightweight database for user & history storage. |
| **AI Engine** | Hugging Face API | External AI models for text processing. |
| **Cloud** | Render | Cloud platform for hosting the application. |

## ⚙️ How to Run Locally

If you want to run this project on your local machine:

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/RDilshan2000/Secure-AI-Cloud-System.git](https://github.com/RDilshan2000/Secure-AI-Cloud-System.git)
    cd Secure-AI-Cloud-System
    ```

2.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Up Environment Variables**
    * Create a `.env` file.
    * Add your Hugging Face Token: `HF_TOKEN=your_token_here`

4.  **Run the Backend (Terminal 1)**
    ```bash
    uvicorn main:app --reload
    ```

5.  **Run the Frontend (Terminal 2)**
    ```bash
    streamlit run frontend.py
    ```

## 📸 Screenshots

*(Screenshots will be added here to showcase the UI)*

## 👨‍💻 Author

**Ramesh Dilshan Dissanayaka**
*Software Engineering Student | DevSecOps Enthusiast*

* [LinkedIn Profile](https://www.linkedin.com/in/ramesh-dilshan-b21878252)
* [GitHub Profile](https://github.com/RDilshan2000)