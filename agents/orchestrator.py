from google import genai
from google.genai import types
import json, re, os

SYSTEM_PROMPT = """You are FlowMind's orchestrator agent. When a user sends a request:
1. Analyse it and decide which agents are needed: task_agent, calendar_agent, notes_agent
2. Respond ONLY with a valid JSON object like this:
{
  "plan": "short explanation of what you will do",
  "actions": [
    {"agent": "task_agent", "instruction": "create tasks: Design mockup, Write tests, Deploy app"},
    {"agent": "calendar_agent", "instruction": "Block 2 hours Thursday morning for product launch prep"},
    {"agent": "notes_agent", "instruction": "Save a note titled Launch Checklist with: Design, Tests, Deploy"}
  ],
  "summary": "What you did for the user"
}
Only include agents that are actually needed. No markdown, no explanation outside JSON."""

class OrchestratorAgent:
    def __init__(self):
        self.client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", ""))

    def run(self, user_input: str, user_id: str) -> dict:
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_input,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.3,
            )
        )
        raw = response.text.strip()

        # Strip markdown fences if Gemini wraps in ```json
        raw = re.sub(r"^```json\s*", "", raw)
        raw = re.sub(r"^```\s*", "", raw)
        raw = re.sub(r"\s*```$", "", raw)

        plan = json.loads(raw)
        results = []

        for action in plan.get("actions", []):
            result = self._dispatch(action["agent"], action["instruction"], user_id)
            results.append(result)

        return {
            "plan": plan.get("plan", ""),
            "summary": plan.get("summary", ""),
            "actions_taken": results
        }

    def _dispatch(self, agent_name: str, instruction: str, user_id: str) -> dict:
        from agents.task_agent import TaskAgent
        from agents.calendar_agent import CalendarAgent
        from agents.notes_agent import NotesAgent

        agents = {
            "task_agent": TaskAgent(),
            "calendar_agent": CalendarAgent(),
            "notes_agent": NotesAgent(),
        }
        agent = agents.get(agent_name)
        if not agent:
            return {"error": f"Unknown agent: {agent_name}"}
        return agent.execute(instruction, user_id)
