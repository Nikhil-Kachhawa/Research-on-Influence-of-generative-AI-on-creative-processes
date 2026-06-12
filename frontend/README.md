# Frontend

Frontend application for Research Lab AI.

## Tech Stack

* React
* Vite
* React Router
* Axios
* Tailwind CSS
* React Markdown

## Run Development Server

```bash
npm run dev
```

Frontend will be available at:

```text
http://localhost:5173
```


## Available Routes

```text
/
/idea-generator
/critical-evaluator
```

## Backend Dependency

The frontend requires the Django backend API to be running.

Configure the API URL using:

```env
VITE_API_URL=http://127.0.0.1:8000/api/
```
