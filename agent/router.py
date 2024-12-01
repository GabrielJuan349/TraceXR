from typing import Callable, Dict
import subprocess
import onnx
from dotenv import load_dotenv
import os
import onnxruntime as ort
import numpy as np
from image_prepros import ImageClassifier 

class QwenRouter:
    _classes = []
    def __init__(self):
        load_dotenv()
        self.actions: Dict[str, Callable] = {
            "track": self.handle_tracking,
            "draw": self.handle_draw,
            "question": self.handle_question,
        }
        onnx_model = onnx.load(os.getenv("ONNX_MODEL_PATH"))
        onnx.checker.check_model(onnx_model)

    def route(self, text: str, classification: str) -> str:
        for action_type, handler in self.actions.items():
            if action_type in classification.lower():
                return handler(text)
        return "The action is not working properly"

    def handle_tracking(self, query: str) -> np.array:
        return f"Tracking Objects..."

    def handle_draw(self,image_url ) -> str:
        try:
            ort_sess = ort.InferenceSession(os.getenv("ONNX_MODEL_PATH"))
            ic = ImageClassifier(ort_sess, os.getenv("LABEL_MAPPING_FILE"))
            return ic.classify_image(image_url)
        except Exception as e:
            return f"Error ejecutando comando: {str(e)}"

    def handle_question(self, question: str) -> str:
        return f"Procesando pregunta: {question}"