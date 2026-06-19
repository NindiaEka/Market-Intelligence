# Market Intelligence AI

AI-powered company intelligence platform for automatically generating company reports from public sources.

## Features

* Company information extraction
* Multi-source web search and crawling
* Capability detection
* Financial intelligence (IDX integration)
* Markdown report generation
* Interactive report preview
* Download report as `.md`
* Sidebar recent reports
* Report caching
* Progress animation

---

## Project Structure

```
Market-Intelligence
│
├── backend
│   ├── src/
│   ├── cache/
│   ├── downloads/
│   ├── app.py
│   ├── Dockerfile
│   └── .env
│
├── frontend
│   ├── app/
│   ├── public/
│   ├── package.json
│   └── Dockerfile
│
├── docs/
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## Tech Stack

### Backend

* Python 3.12
* FastAPI
* Playwright
* Crawl4AI
* Tavily
* Google Gemini
* Anthropic Claude

### Frontend

* Next.js 16
* React
* TypeScript
* TailwindCSS
* React Markdown

### Deployment

* Docker
* Railway (Backend)
* Vercel (Frontend)

---

## Installation

### Clone Repository

```bash
git clone <repository-url>

cd Market-Intelligence
```

---

## Backend

```bash
cd backend

uv sync
```

Create `.env`

```env
GEMINI_API_KEY=
OPENAI_API_KEY=
ANTHROPIC_API_KEY=
TAVILY_API_KEY=
```

Run backend:

```bash
uv run uvicorn app:app --reload
```

Open:

```
http://localhost:8000/docs
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

Open:

```
http://localhost:3000
```

---

## Docker

Build image:

```bash
docker build -t market-intelligence-backend .
```

Run container:

```bash
docker run --env-file .env -p 8000:8000 market-intelligence-backend
```

---

## Docker Compose

Run entire stack:

```bash
docker compose up --build
```

---

## Workflow

```
Company Name
      ↓
Company Resolution
      ↓
Search Sources
      ↓
Website Crawling
      ↓
Fact Extraction
      ↓
Capability Detection
      ↓
Financial Intelligence
      ↓
Report Generation
      ↓
Markdown Preview
      ↓
Download .md
```

---

## Current Version

### v1.3

✅ Progress animation

✅ Sidebar recent reports

✅ Report cache

✅ Markdown preview

✅ Download report

---

## Author

Nindia Ekasuci Larasati

Geophysics × AI Engineer
