from mcp.firestore_mcp import FirestoreMCP
from datetime import datetime

db_mcp = FirestoreMCP()

class CalendarAgent:
    def execute(self, instruction: str, user_id: str) -> dict:
        from google.cloud import firestore
        client = firestore.Client()
        ref = client.collection("events").document()
        event = {
            "id": ref.id,
            "user_id": user_id,
            "title": instruction,
            "created_at": datetime.utcnow().isoformat(),
            "status": "scheduled"
        }
        ref.set(event)
        return {
            "agent": "calendar_agent",
            "action": "event_scheduled",
            "event": event
        }
