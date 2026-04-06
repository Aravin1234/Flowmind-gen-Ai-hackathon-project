import os
from google.cloud import secretmanager

def load_gemini_key():
    """Fetch Gemini API key from Secret Manager if not already in env."""
    if os.environ.get("GEMINI_API_KEY"):
        return
    try:
        client = secretmanager.SecretManagerServiceClient()
        project_id = os.environ.get("PROJECT_ID", "flowmind-hackathon")
        name = f"projects/{project_id}/secrets/gemini-api-key/versions/latest"
        response = client.access_secret_version(request={"name": name})
        os.environ["GEMINI_API_KEY"] = response.payload.data.decode("UTF-8")
        print("Gemini API key loaded from Secret Manager")
    except Exception as e:
        print(f"Warning: Could not load Gemini key from Secret Manager: {e}")

load_gemini_key()

from fastapi import FastAPI, HTTPException
from models.schemas import WorkflowRequest
from agents.orchestrator import OrchestratorAgent
import json

app = FastAPI(title="FlowMind API", version="1.0.0")
orchestrator = OrchestratorAgent()

@app.get("/health")
def health():
    return {"status": "ok", "service": "FlowMind", "version": "1.0.0"}

@app.post("/workflow")
def run_workflow(req: WorkflowRequest):
    try:
        result = orchestrator.run(req.message, req.user_id)
        return result
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=422, detail=f"Orchestrator returned invalid JSON: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tasks/{user_id}")
def get_tasks(user_id: str):
    from mcp.firestore_mcp import FirestoreMCP
    return {"tasks": FirestoreMCP().get_tasks(user_id)}

@app.get("/notes/{user_id}")
def get_notes(user_id: str):
    from mcp.firestore_mcp import FirestoreMCP
    return {"notes": FirestoreMCP().get_notes(user_id)}

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def dashboard():
    return FileResponse("static/index.html")
