cat > README.md << 'EOF'
# FlowMind — Multi-Agent Productivity OS

> Google Gen AI APAC Hackathon Project

## Live Demo
🚀 https://flowmind-api-808655269303.asia-south1.run.app

## What is FlowMind?
FlowMind is a multi-agent AI system that helps users manage tasks, schedules, and notes using natural language. A single instruction like *"Plan my product launch Friday"* automatically creates tasks, blocks calendar time, and saves a checklist — all coordinated by a Gemini-powered orchestrator.

## Architecture
## Tech Stack
| Layer | Technology |
|-------|-----------|
| AI Orchestrator | Gemini 2.5 Flash (Google AI) |
| Backend API | FastAPI + Python |
| Database | Google Cloud Firestore |
| Deployment | Google Cloud Run |
| Secret Management | Google Secret Manager |

## Features
- Natural language multi-step workflow execution
- Autonomous agent coordination and delegation
- Real-time task, event, and notes management
- REST API with interactive docs
- Fully deployed on Google Cloud

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Live dashboard UI |
| GET | `/health` | Health check |
| POST | `/workflow` | Run a multi-agent workflow |
| GET | `/tasks/{user_id}` | Get all tasks |
| GET | `/notes/{user_id}` | Get all notes |
| GET | `/docs` | Interactive API explorer |

## Try It Live
Send a POST request to `/workflow`:
```json
{
  "user_id": "demo-user",
  "message": "I have a product launch on Friday. Create 3 tasks for it, block 2 hours Thursday morning to prep, and save a note with the checklist."
}
```

## Project Structure
flowmind/
├── main.py                  # FastAPI entry point
├── agents/
│   ├── orchestrator.py      # Primary Gemini agent
│   ├── task_agent.py        # Task management agent
│   ├── calendar_agent.py    # Calendar scheduling agent
│   └── notes_agent.py       # Notes management agent
├── mcp/
│   └── firestore_mcp.py     # Firestore MCP tool
├── models/
│   └── schemas.py           # Pydantic models
├── static/
│   └── index.html           # Dashboard UI
└── Dockerfile
## Setup & Deployment
```bash
# Clone the repo
git clone https://github.com/Aravin1234/Flowmind-gen-Ai-hackathon-project.git
cd Flowmind-gen-Ai-hackathon-project

# Deploy to Google Cloud Run
gcloud builds submit --tag gcr.io/YOUR_PROJECT/flowmind-api .
gcloud run deploy flowmind-api --image gcr.io/YOUR_PROJECT/flowmind-api --platform managed --region asia-south1 --allow-unauthenticated
```

## Built With
- [Google Cloud Run](https://cloud.google.com/run)
- [Google Cloud Firestore](https://cloud.google.com/firestore)
- [Gemini API](https://ai.google.dev)
- [FastAPI](https://fastapi.tiangolo.com)
EOF
