from mcp.firestore_mcp import FirestoreMCP

class NotesAgent:
    def __init__(self):
        self.mcp = FirestoreMCP()

    def execute(self, instruction: str, user_id: str) -> dict:
        note = self.mcp.create_note(
            user_id=user_id,
            title="FlowMind Note",
            content=instruction
        )
        return {
            "agent": "notes_agent",
            "action": "note_created",
            "note": note
        }
