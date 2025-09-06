from decouple import config
from typing import Union, BinaryIO
from fastapi import UploadFile
from openai import OpenAI

# Import custom functions 
from functions.database import get_recent_messages

# Retrieve environment variables safely
_OPENAI_ORG = config("OPEN_AI_ORG", default=None)
_OPENAI_KEY = config("OPEN_AI_KEY", default=None)

# Initialize OpenAI client with proper configuration
client = OpenAI(
    api_key=_OPENAI_KEY,
    organization=_OPENAI_ORG if _OPENAI_ORG else None
)

if not _OPENAI_KEY:
    print("Warning: OPEN_AI_KEY not set. OpenAI requests will fail until the key is provided.")


def _get_file_obj(audio_file: Union[str, BinaryIO, UploadFile]):
    """Return a file-like object for the given input.

    Accepts a filesystem path (str), a binary file-like object, or FastAPI UploadFile.
    If a path is provided, the caller is responsible for closing the returned object.
    """
    if isinstance(audio_file, UploadFile):
        return audio_file.file
    if isinstance(audio_file, str):
        return open(audio_file, "rb")
    # assume it's already a file-like object
    return audio_file


def convert_audio_to_text(audio_file: Union[str, BinaryIO, UploadFile]):
    """Convert audio to text using OpenAI Whisper.

    Returns the transcribed text on success, or None on failure.
    """
    file_obj = None
    opened_here = False
    try:
        file_obj = _get_file_obj(audio_file)
        opened_here = isinstance(audio_file, str)

        # Fixed: Use file_obj instead of audio_file
        response = client.audio.transcriptions.create(
            model="whisper-1", 
            file=file_obj
        )

        # The new API returns an object with a .text attribute
        return response.text

    except Exception as e:
        print("Error in convert_audio_to_text:", e)
        return None
    finally:
        if opened_here and file_obj:
            try:
                file_obj.close()
            except Exception:
                pass


def get_chat_response(message_input):
    """Get chat response from OpenAI GPT using the new API."""
    
    messages = get_recent_messages()
    user_message = {"role": "user", "content": message_input}
    messages.append(user_message)
    print(messages)

    try:
        # Updated to use new OpenAI API syntax
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            max_tokens=500,
            n=1,
            stop=None,
            temperature=0.7,
        )

        print(response)
        # Updated to use new response structure
        message_text = response.choices[0].message.content
        return message_text
        
    except Exception as e:
        print("Error in get_chat_response:", e)
        return "Sorry, I am unable to process your request at the moment."