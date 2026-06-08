# 🏛️ Polis

**Operational Intelligence for the Modern Organization**

Polis is a production-ready AI Operational Intelligence Assistant designed to analyze multi-source discussions and extract structured, actionable insights. Unlike generic chatbots, Polis focuses on identifying tasks, risks, contradictions, and feasibility to provide a clear picture of organizational health.

---

## 🚀 Key Features

- **Multi-Agent Analysis**: 7 specialized AI agents orchestrated via LangGraph.
- **Operational Intelligence**: Automatic extraction of Tasks, Decisions, Risks, and Contradictions.
- **Semantic Memory**: Long-term organizational memory using Qdrant vector storage.
- **Multi-Channel**: Seamless integration with Web, Slack, and WhatsApp.
- **Auto-Transcription**: High-fidelity transcription of meeting audio via OpenAI Whisper.
- **Premium UI**: Modern glassmorphic dashboard for visualizing intelligence findings.

## 🛠️ Architecture

Polis follows a modular, service-oriented architecture:
- **Frontend**: React 18, Tailwind CSS, Lucide Icons.
- **Backend**: FastAPI, LangChain, LangGraph.
- **Database**: PostgreSQL (Relational) + Qdrant (Vector).
- **Worker**: Celery + Redis for async processing.
- **Infrastructure**: Docker Compose + Nginx.

Check the [Architecture Walkthrough](./walkthrough.md) for more details.

## 🚦 Getting Started

### Prerequisites
- Docker & Docker Compose
- OpenAI API Key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ATripathi13/polis.git
   cd polis
   ```

2. **Configure Environment**
   Create a `.env` file in the root directory:
   ```env
   OPENAI_API_KEY=your_key_here
   DATABASE_URL=postgresql+asyncpg://polis:polis_secret@postgres/polis
   REDIS_URL=redis://redis:6379/0
   QDRANT_HOST=qdrant
   ```

3. **Launch Services**
   ```bash
   docker-compose up --build
   ```

4. **Access the App**
   - Dashboard: `http://localhost:3000`
   - API Docs: `http://localhost:8000/docs`

## 🧩 Project Structure

```text
polis/
├── backend/            # FastAPI Application & AI Agents
│   ├── app/
│   │   ├── agents/     # LangGraph & Specialized Agents
│   │   ├── api/        # REST Endpoints
│   │   ├── models/     # SQLAlchemy Models
│   │   └── services/   # Business Logic
├── frontend/           # React Dashboard
│   ├── src/
│   │   ├── components/ # Shared UI Components
│   │   └── pages/      # Application Screens
├── nginx/              # Reverse Proxy Config
└── docker-compose.yml  # Orchestration
```

## 📜 License
MIT License - see [LICENSE](LICENSE) for details.
