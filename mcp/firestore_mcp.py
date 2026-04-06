from google.cloud import firestore
from datetime import datetime

db = firestore.Client()

class FirestoreMCP:
    def create_task(self, user_id: str, title: str, due_date: str = None, priority: str = "medium") -> dict:
        ref = db.collection("tasks").document()
        task = {
            "id": ref.id,
            "user_id": user_id,
            "title": title,
            "due_date": due_date,
            "priority": priority,
            "status": "pending",
            "created_at": datetime.utcnow().isoformat()
        }
        ref.set(task)
        return task

    def get_tasks(self, user_id: str, status: str = None) -> list:
        query = db.collection("tasks").where("user_id", "==", user_id)
        if status:
            query = query.where("status", "==", status)
        docs = query.get()
        return [d.to_dict() for d in docs]

    def create_note(self, user_id: str, title: str, content: str) -> dict:
        ref = db.collection("notes").document()
        note = {
            "id": ref.id,
            "user_id": user_id,
            "title": title,
            "content": content,
            "created_at": datetime.utcnow().isoformat()
        }
        ref.set(note)
        return note

    def get_notes(self, user_id: str) -> list:
        docs = db.collection("notes").where("user_id", "==", user_id).get()
        return [d.to_dict() for d in docs]
