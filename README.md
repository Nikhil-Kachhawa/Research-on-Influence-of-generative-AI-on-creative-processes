# Gen-AI-for-Creative-Tasks-Roles-Research-Internship

Research Internship: Influence of Generative AI on Creative Processes

Deployed Link : [Project Link](https://nikhil-research-genai.vercel.app/)

## Overview

Research Lab AI is a web application that evaluates the influence of different AI roles on creative tasks.

Current AI Roles:

* 💡 Idea Generator
* 🔍 Critical Evaluator

Tech Stack:

* Frontend: React + Vite + Tailwind CSS
* Backend: Django + Django REST Framework
* LLM: Llama 3.1 via Hugging Face Inference API
* Database: SQLite
* Deployment:

  * Frontend: Vercel
  * Backend: Render

---

## Prerequisites

Before running the project locally, install:

### Python

Recommended Version:

```bash
Python 3.13+
```

Verify installation:

```bash
python --version
```

### Node.js

Recommended Version:

```bash
Node.js 22+
```

Verify installation:

```bash
node --version
npm --version
```

### Git

Verify installation:

```bash
git --version
```

---

## Clone or Download this Repository

---

# Backend Setup

Navigate to backend folder:

```bash
cd backend
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

Windows:

```bash
venv\Scripts\activate
```

Alternatively for Linux / macOS:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file inside the `backend` directory.

Example:

```env
HF_TOKEN=your_huggingface_api_token
```

---

## Database Setup

Apply migrations:

```bash
python manage.py migrate
```

Run backend server:

```bash
python manage.py runserver
```

Backend will run on:

```text
http://127.0.0.1:8000
```

---

# Frontend Setup

Navigate to frontend folder:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run development server:

```bash
npm run dev
```

Frontend will run on:

```text
http://localhost:5173
```

---

# Available Routes

Frontend:

```text
/
/idea-generator
/critical-evaluator
```

Backend:

```text
/
/api/health/
/api/chat/
/admin/
```

---

# Project Structure

```text
backend/
├── chatbot/
│   ├── services/
│   │   └── llm.py
│   ├── prompts.py
│   ├── views.py
│   └── urls.py
│
├── config/
├── manage.py
└── requirements.txt

frontend/
├── src/
├── public/
├── package.json
└── vite.config.js
```

---

# Deployed Link

[Project Link](https://nikhil-research-genai.vercel.app/)
