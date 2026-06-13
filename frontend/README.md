# Research Lab AI - Frontend

Frontend application for the Research Lab AI platform.

## Overview

This application provides the user interface for interacting with AI-powered research assistants. It communicates with the Django REST API backend and supports multiple research experiment conditions.

## Tech Stack

- React
- Vite
- React Router
- Axios
- Tailwind CSS
- React Markdown

## Project Structure

```text
src/
├── components/
│   ├── ChatHeader.jsx
│   ├── ChatInput.jsx
│   └── ChatMessages.jsx
│
├── pages/
│   ├── HomePage.jsx
│   └── ChatPage.jsx
│
├── services/
│   └── api.js
│
├── utils/
│   └── session.js
│
└── main.jsx
```

## Prerequisites

- Node.js 18+
- npm

## Installation

```bash
npm install
```

## Environment Variables

Create a `.env` file in the frontend root directory:

```env
VITE_API_URL=http://127.0.0.1:8000/api/
```

For production:

```env
VITE_API_URL=https://your-backend-domain/api/
```

## Running the Application

Start the development server:

```bash
npm run dev
```

The application will be available at:

```text
http://localhost:5173
```

## Available Routes

| Route | Description |
|---------|-------------|
| `/` | Landing page |
| `/idea-generator` | Idea generation assistant |
| `/critical-evaluator` | Critical evaluation assistant |

## Backend Integration

The frontend depends on the Django REST API backend.

Ensure the backend service is running and accessible through the configured `VITE_API_URL`.

## Build for Production

```bash
npm run build
```

Preview the production build locally:

```bash
npm run preview
```

## Deployment

The frontend is deployed on:

- Vercel

Ensure the production API URL is configured through environment variables before deployment.

## License

This project is developed as part of the Research Lab AI platform.