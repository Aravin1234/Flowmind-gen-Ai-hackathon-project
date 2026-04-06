from mcp.firestore_mcp import FirestoreMCP
import json

class TaskAgent:
    def __init__(self):
        self.mcp = FirestoreMCP()

    def execute(self, instruction: str, user_id: str) -> dict:
        instruction_lower = instruction.lower()
        
        if "create" in instruction_lower or "add" in instruction_lower:
            # Extract task details from instruction
            tasks_created = []
            lines = instruction.split("\n")
            for line in lines:
                line = line.strip().lstrip("-•123456789. ")
                if len(line) > 3:
                    task = self.mcp.create_task(
                        user_id=user_id,
                        title=line,
                        priority="high" if "urgent" in line.lower() else "medium"
                    )
                    tasks_created.append(task)
            
            if not tasks_created:
                task = self.mcp.create_task(user_id=user_id, title=instruction)
                tasks_created.append(task)

            return {
                "agent": "task_agent",
                "action": "created_tasks",
                "count": len(tasks_created),
                "tasks": tasks_created
            }

        elif "list" in instruction_lower or "get" in instruction_lower or "show" in instruction_lower:
            tasks = self.mcp.get_tasks(user_id=user_id)
            return {
                "agent": "task_agent",
                "action": "retrieved_tasks",
                "count": len(tasks),
                "tasks": tasks
            }

        return {"agent": "task_agent", "action": "no_op", "instruction": instruction}
