# Polis — AI Operational Intelligence Chatbot

Polis is an enterprise-grade AI Operational Intelligence Assistant that analyzes discussions to identify tasks, decisions, risks, contradictions, unrealistic commitments, and generates executive summaries.

## Features

- **Multi-Agent Analysis** — 7 specialized AI agents (Transcript, Task, Contradiction, Risk, Feasibility, Validator, Executive Summary)
- **LangGraph Orchestration** — Parallel agent execution with validation pipeline
- **Contradiction Detection** — Timeline, resource, technical, business, and dependency contradictions
- **Risk Assessment** — Technical, operational, business, delivery, and compliance risks
- **Feasibility Analysis** — Realistic, unrealistic, impossible, under-scoped, or missing-info determination
- **Multi-Channel** — Web Chat UI, Slack, WhatsApp
- **Organizational Memory** — Semantic retrieval with Qdrant vector database
- **File Processing** — Audio, PDFs, text documents

## Tech Stack

| Layer       | Technology                          |
|-------------|-------------------------------------|
| Backend     | FastAPI, Python 3.11                |
| Database    | PostgreSQL                          |
| Cache       | Redis                               |
| Queue       | Celery                              |
| Vector DB   | Qdrant                              |
| AI/LLM      | OpenAI GPT-4o, LangChain, LangGraph|
| Frontend    | React, Tailwind CSS, Vite           |
| Deployment  | Docker Compose, Nginx               |

## Quick Start

```bash
# 1. Clone and configure
cp .env.example .env
# Edit .env with your credentials

# 2. Start all services
docker compose up --build

# 3. Access
# Frontend: http://localhost
# API Docs: http://localhost/api/docs
```

## Project Structure

```
Polis/
├── backend/          # FastAPI + Agents + Services
├── frontend/         # React + Tailwind
├── nginx/            # Reverse proxy
├── docker-compose.yml
└── .env.example
```

## API Endpoints

| Method | Endpoint            | Description              |
|--------|---------------------|--------------------------|
| POST   | /api/upload         | Upload documents         |
| POST   | /api/analyze        | Trigger analysis         |
| POST   | /api/chat           | Chat with Polis          |
| GET    | /api/memory/search  | Search organizational memory |
| POST   | /api/slack/webhook  | Slack events             |
| POST   | /api/whatsapp/webhook | WhatsApp messages      |

## License

Proprietary — All rights reserved.
