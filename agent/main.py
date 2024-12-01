import openai
import sounddevice as sd
import numpy as np
from transformers import AutoTokenizer, AutoModelForCausalLM
import queue
import threading
import time
from dotenv import load_dotenv
import os
import soundfile as sf
import tempfile
from router import QwenRouter

class AudioProcessor:
    def __init__(self):
        # Initial configuration
        self.SAMPLE_RATE = 16000
        self.CHANNELS = 1
        self.CHUNK_DURATION = 5  # seconds
        
        # Load environment variables
        load_dotenv()
        
        # Initialize OpenAI
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.route_model = os.getenv("ROUTE_MODEL")
        
        # Initialize models
        self.tokenizer = AutoTokenizer.from_pretrained(self.route_model, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(self.route_model, trust_remote_code=True)
        
        # Initialize queue
        self.audio_queue = queue.Queue()
        
        # Initialize router
        self.router = QwenRouter()

    class Prompts:
        @staticmethod
        def getClassificationPrompt(text):
            return """Classify the following text into one of these categories: 
                    track, draw, question: '{text}'
                    Respond only with the category."""
        
        @staticmethod
        def getDrawPrompt(text):
            return """System prompt: The drawing should represent '{text}'."""
        
        @staticmethod
        def getQuestionPrompt(text, question):
            return f"""System prompt: The text '{text}' is asking the following question: '{question}'."""

    def audio_callback(self, indata, *_):
        """Callback for audio capture"""
        self.audio_queue.put(indata.copy())

    def process_audio(self, data):
        while True:
            audio_data = []
            start_time = time.time()
            
            while time.time() - start_time < self.CHUNK_DURATION:
                if not self.audio_queue.empty():
                    audio_data.append(self.audio_queue.get())
            
            if audio_data:
                audio_array = np.concatenate(audio_data)
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                    sf.write(tmp_file.name, audio_array, self.SAMPLE_RATE)
                    tmp_filename = tmp_file.name

                try:
                    with open(tmp_filename, "rb") as audio_file:
                        response = openai.Audio.transcribe(
                            model="whisper-1",
                            file=audio_file,
                            language="en"
                        )
                    text = response.text
                    
                except Exception as e:
                    print(f"Transcription error: {str(e)}")
                    text = ""
                finally:
                    if os.path.exists(tmp_filename):
                        os.unlink(tmp_filename)
                
                if text.strip():
                    prompt = self.Prompts.getClassificationPrompt(text)
                    inputs = self.tokenizer(prompt, return_tensors="pt")
                    outputs = self.model.generate(**inputs, max_length=100)
                    classification = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
                    
                    result = self.router.route(text, data, classification)
                    if classification == "draw":
                        outputs = self.tokenizer(self.Prompts.getDrawPrompt(result), return_tensors="pt")
                        text_TS = self.model.generate(**outputs, max_length=100)
                        text = self.tokenizer.decode(text_TS[0], skip_special_tokens=True)
                    elif classification == "question":
                        outputs = self.tokenizer(self.Prompts.getQuestionPrompt(text, result), return_tensors="pt")
                        text_TS = self.model.generate(**outputs, max_length=100)
                        text = self.tokenizer.decode(text_TS[0], skip_special_tokens=True)
                    
                    if text:
                        try:
                            speech_response = openai.audio.speech.create(
                                model="tts-1",
                                voice="alloy",
                                input=text
                            )
                            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
                                speech_response.stream_to_file(tmp_file.name)
                                data, samplerate = sf.read(tmp_file.name)
                                sd.play(data, samplerate)
                                sd.wait()
                                os.unlink(tmp_file.name)
                        except Exception as e:
                            print(f"TTS error: {str(e)}")

    def run(self):
        """Main execution method"""
        stream = sd.InputStream(
            channels=self.CHANNELS,
            samplerate=self.SAMPLE_RATE,
            callback=self.audio_callback
        )
        
        with stream:
            print("Listening... Press Ctrl+C to stop.")
            
            processing_thread = threading.Thread(target=lambda: self.process_audio(data=None))
            processing_thread.daemon = True
            processing_thread.start()
            
            try:
                while True:
                    time.sleep(0.1)
            except KeyboardInterrupt:
                print("\nStopping...")

def main():
    processor = AudioProcessor()
    processor.run()

if __name__ == "__main__":
    main()
