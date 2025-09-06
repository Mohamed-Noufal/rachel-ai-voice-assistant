import requests
from decouple import config
import traceback

ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY", default=None)

def convert_text_to_speech(message):
    """Convert text to speech using Eleven Labs API"""
    
    if not ELEVEN_LABS_API_KEY:
        print("❌ ELEVEN_LABS_API_KEY not configured")
        return None
    
    if not message or message.strip() == "":
        print("❌ Empty message provided for TTS")
        return None

    print(f"🔊 Converting text to speech: '{message[:50]}...'")

    # Define Data
    body = {
        "text": message,
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0,
        }
    }

    # Define voice ID - Rachel
    voice_rachel = "UgBBYS2sOqTuMpoF3BR0"  #NOpBlnGInO9m6vDvFkFC Rachel voice ID

    # Construct headers and endpoint
    headers = {
        "xi-api-key": ELEVEN_LABS_API_KEY,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg"
    }
    endpoint = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_rachel}"

    # Send request
    try:
        print(f"📡 Sending request to Eleven Labs API...")
        response = requests.post(endpoint, json=body, headers=headers, timeout=30)
        print(f"📡 Eleven Labs response status: {response.status_code}")
        
        if response.status_code == 200:
            # Save audio content to file
            output_filename = "voice.mp3"
            with open(output_filename, "wb") as f:
                f.write(response.content)
            print(f"✅ Audio content written to file '{output_filename}' ({len(response.content)} bytes)")
            return output_filename
        else:
            print(f"❌ Eleven Labs API Error: {response.status_code}")
            print(f"❌ Response: {response.text}")
            return None
            
    except requests.exceptions.Timeout:
        print("❌ Timeout error: Eleven Labs API took too long to respond")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {str(e)}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error in convert_text_to_speech: {str(e)}")
        print(traceback.format_exc())
        return None