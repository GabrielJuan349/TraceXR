from typing import Callable, Dict
import subprocess

class QwenRouter:
    def __init__(self):
        self.actions: Dict[str, Callable] = {
            "track": self.handle_tracking,
            "draw": self.handle_draw,
            "question": self.handle_question,
        }

    def route(self, text: str, classification: str) -> str:
        for action_type, handler in self.actions.items():
            if action_type in classification.lower():
                return handler(text)
        return "The action is not working properly"

    def handle_tracking(self, query: str) -> str:
        return f"Tracking Objects..."

    def handle_draw(self, cmd: str) -> str:
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return f"Ejecutado comando: {result.stdout}"
        except Exception as e:
            return f"Error ejecutando comando: {str(e)}"

    def handle_question(self, question: str) -> str:
        return f"Procesando pregunta: {question}"