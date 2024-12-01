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


# Initial configuration
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_DURATION = 5  # seconds
load_dotenv()
# Initialize models
openai.api_key = os.getenv("OPENAI_API_KEY")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen1.5-0.5B", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen1.5-0.5B", trust_remote_code=True)

# Queue for thread communication
audio_queue = queue.Queue()
class _prompts:
    def getClassificationPrompt(text):
        return """Classify the following text into one of these categories: 
                track, draw, question: '{text}'
                Respond only with the category."""
    def getDrawPrompt(text):
        return """System prompt: The drawing should represent '{text}'."""
    def getQuestionPrompt(text, question):
        return f"""System prompt: The text '{text}' is asking the following question: '{question}'."""

def audio_callback(indata, *_):
    """Callback for audio capture"""
    audio_queue.put(indata.copy())

def process_audio(data):
    router = QwenRouter()
    while True:
        audio_data = []
        start_time = time.time()
        
        while time.time() - start_time < CHUNK_DURATION:
            if not audio_queue.empty():
                audio_data.append(audio_queue.get())
        
        if audio_data:
            audio_array = np.concatenate(audio_data)
            # audio_buffer = io.BytesIO()
            # sf.write(audio_buffer, audio_array, SAMPLE_RATE, format='wav')
            # audio_buffer.seek(0)
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                sf.write(tmp_file.name, audio_array, SAMPLE_RATE)
                tmp_filename = tmp_file.name  

            
            try:
                # Use OpenAI API for transcription
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
                prompt = _prompts.getClassificationPrompt(text)
                
                inputs = tokenizer(prompt, return_tensors="pt")
                outputs = model.generate(**inputs, max_length=100)
                classification = tokenizer.decode(outputs[0], skip_special_tokens=True)  
                
                result = router.route(text,data, classification)
                if classification == "draw":
                    outputs = tokenizer(_prompts.getDrawPrompt(result), return_tensors="pt")
                    text_TS = model.generate(**outputs, max_length=100)
                    text = tokenizer.decode(text_TS[0], skip_special_tokens=True)
                elif classification == "question":  
                    outputs = tokenizer(_prompts.getQuestionPrompt(text, result), return_tensors="pt")
                    text_TS = model.generate(**outputs, max_length=100)
                    text = tokenizer.decode(text_TS[0], skip_special_tokens=True)
                
                if text:
                    try:
                        speech_response = openai.audio.speech.create(
                            model="tts-1",
                            voice="alloy",
                            input=text
                        )
                        # Save the audio to a temporary file and play it
                        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_file:
                            speech_response.stream_to_file(tmp_file.name)
                            data, samplerate = sf.read(tmp_file.name)
                            sd.play(data, samplerate)
                            sd.wait()
                            os.unlink(tmp_file.name)
                    except Exception as e:
                        print(f"TTS error: {str(e)}")

def main():
    """Main function"""
    # Configure audio stream
    stream = sd.InputStream(
        channels=CHANNELS,
        samplerate=SAMPLE_RATE,
        callback=audio_callback
    )
    
    # Start audio capture
    with stream:
        print("Listening... Press Ctrl+C to stop.")  
        
        # Start background processing
        processing_thread = threading.Thread(target=lambda: process_audio(data=None))
        processing_thread.daemon = True
        processing_thread.start()
        
        # Keep the program running
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            print("\nStopping...")

if __name__ == "__main__":
    main()
