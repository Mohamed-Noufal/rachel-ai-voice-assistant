# groq_api.py - Groq API integration with local Whisper

from decouple import config
from typing import Union, BinaryIO
from fastapi import UploadFile
import requests
import whisper
import os

# Groq API setup
GROQ_API_KEY = config("GROQ_API_KEY", default=None)
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

# Load local Whisper model (one time at startup)
whisper_model = None

def load_whisper_model():
    """Load Whisper model with better error handling"""
    global whisper_model
    try:
        print("Loading Whisper model...")
        whisper_model = whisper.load_model("base")  # or "tiny" for faster
        print("Whisper model loaded successfully!")
        return True
    except Exception as e:
        print(f"Error loading Whisper model: {e}")
        whisper_model = None
        return False

# Load model at startup
load_whisper_model()

if not GROQ_API_KEY:
    print("Warning: GROQ_API_KEY not set. Add it to your .env file")


def _get_file_obj(audio_file: Union[str, BinaryIO, UploadFile]):
    """Return a file-like object for the given input."""
    if isinstance(audio_file, UploadFile):
        return audio_file.file
    if isinstance(audio_file, str):
        return open(audio_file, "rb")
    return audio_file


def convert_audio_to_text(audio_file: Union[str, BinaryIO, UploadFile]):
    """Convert audio to text using the preloaded Whisper model"""
    temp_path = None
    try:
        if not whisper_model:
            print("❌ Whisper model not loaded.")
            return None

        # Prepare file (absolute path or temp)
        if isinstance(audio_file, str):
            audio_path = os.path.abspath(audio_file)
            if not os.path.exists(audio_path):
                print(f"Audio file not found: {audio_path}")
                return None
        else:
            temp_path = os.path.abspath("whisper_temp.wav")
            with open(temp_path, "wb") as f:
                if hasattr(audio_file, "seek"):
                    audio_file.seek(0)
                f.write(audio_file.read())
            audio_path = temp_path

        print(f"Transcribing: {audio_path}")
        result = whisper_model.transcribe(audio_path, fp16=False)

        return result["text"].strip()

    except Exception as e:
        print(f"Error in convert_audio_to_text: {e}")
        return None
    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


def get_chat_response(message_input):
    """Get chat response from Groq API - FAST and generous free tier!"""
    if not GROQ_API_KEY:
        return "Error: GROQ_API_KEY not configured"

    # Import the get_recent_messages function from database.py
    from functions.database import get_recent_messages

    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        }

        # Get messages from database including system instructions
        messages = get_recent_messages()

        # Add the current user message
        messages.append({"role": "user", "content": message_input})

        data = {
            "model": "llama-3.1-8b-instant",  # Fast model
            "messages": messages,
            "max_tokens": 500,
            "temperature": 0.7,
        }

        print("Sending request to Groq API...")
        response = requests.post(
            f"{GROQ_BASE_URL}/chat/completions",
            headers=headers,
            json=data,
            timeout=30,
        )

        print(f"Groq API response status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        elif response.status_code == 429:
            return "Rate limit exceeded. Please wait a moment and try again."
        else:
            print(f"Groq API error: {response.status_code} - {response.text}")
            return "Sorry, I'm having trouble connecting right now."

    except Exception as e:
        print("Error in get_chat_response:", e)
        return "Sorry, I encountered an error while processing your request."


def check_groq_limits():
    """Dummy function for main.py import (extend if you add usage limits)."""
    return {"status": "ok"}
