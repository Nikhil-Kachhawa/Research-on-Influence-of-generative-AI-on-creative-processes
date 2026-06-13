# Research Lab AI

Research platform for studying the influence of different Generative AI roles on creative and decision-making tasks.

## Live Demo

🚀 https://nikhil-research-genai.vercel.app/

---

## Overview

Research Lab AI is a full-stack web application designed to evaluate how different AI personas influence user thinking, idea generation, and evaluation processes.

The platform allows participants to interact with specialized AI roles under controlled experimental conditions of master thesis topics while capturing conversation data for research analysis.

### Current AI Roles

- 💡 Idea Generator
- 🔍 Critical Evaluator
---

## Architecture

```text
Frontend (React)
        │
        ▼
Django REST API
        │
        ▼
Prompt Builder
        │
        ▼
Llama 3.1 (Hugging Face)
        │
        ▼
PostgreSQL
```

---

## Tech Stack

### Frontend

- React
- Vite
- React Router
- Axios
- Tailwind CSS
- React Markdown

### Backend

- Django
- Django REST Framework
- Django Admin
- WhiteNoise

### AI & Data

- Llama 3.1 8B Instruct
- Hugging Face Inference API
- PostgreSQL (Neon)

### Deployment

- Frontend: Vercel
- Backend: Render
- Database: Neon PostgreSQL

---

## Project Structure

```text
Gen-AI-for-Creative-Tasks-Roles-Research-Internship/
│
├── backend/
│   ├── chatbot/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── prompts.py
│   │   └── services/
│   │       └── llm.py
│   │
│   ├── config/
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── utils/
│   │
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## Prerequisites

### Backend

- Python 3.13+
- PostgreSQL 16+

### Frontend

- Node.js 22+
- npm 10+

### Tools

- Git

---

## Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Backend Environment Variables

Create a `.env` file inside the backend directory:

```env
HF_TOKEN=your_huggingface_token

DEBUG=True

DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432
```

Apply migrations:

```bash
python manage.py migrate
```

Run the development server:

```bash
python manage.py runserver
```

Backend URL:

```text
http://127.0.0.1:8000
```

---

## Frontend Setup

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Create a `.env` file:

```env
VITE_API_URL=http://127.0.0.1:8000/api/
```

Start the development server:

```bash
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

---

## Available Routes

### Frontend

```text
/
/idea-generator
/critical-evaluator
```

### Backend

```text
/
/api/health/
/api/chat/
```

---

## Research Objectives

The project investigates:

- Human-AI collaboration
- AI-assisted creativity
- Prompt engineering strategies
- Role-based AI behavior
- User interaction patterns
- Influence of AI personas on decision-making

---

## Deployment

### Frontend

Hosted on Vercel.

### Backend

Hosted on Render.

### Database

Hosted on Neon PostgreSQL.

---

## Author

**Nikhil Kachhawa**

Master's Student – Web and Data Science  
University of Koblenz

LinkedIn: https://www.linkedin.com/in/nikhil-kachhawa/

---

## License

This project was developed as part of a Generative AI Research Internship focused on studying the impact of AI roles on creative processes.