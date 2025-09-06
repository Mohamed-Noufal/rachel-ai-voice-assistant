#install requirements.txt & activate venv
#cd D:\LLM\React\project\chat-with-Rachel\backend; .\venv\Scripts\Activate
#uvicorn main:app
#uvicorn main:app --reload

#Main Imports
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import json
import os
import traceback

print("🔥 Starting server initialization...")

#Custom Function Imports with detailed error handling
try:
    from functions.grouq_api import convert_audio_to_text, get_chat_response, check_groq_limits
    print("✅ Successfully imported groq_api functions")
except Exception as e:
    print(f"❌ Error importing groq_api functions: {str(e)}")
    print(traceback.format_exc())

try:
    from functions.database import store_messages, reset_messages, get_recent_messages
    print("✅ Successfully imported database functions")
except Exception as e:
    print(f"❌ Error importing database functions: {str(e)}")
    print(traceback.format_exc())

try:
    from functions.text_to_speech import convert_text_to_speech
    print("✅ Successfully imported text_to_speech functions")
except Exception as e:
    print(f"❌ Error importing text_to_speech functions: {str(e)}")
    print(traceback.format_exc())

# Test environment variables
try:
    groq_key = config("GROQ_API_KEY", default=None)
    eleven_key = config("ELEVEN_LABS_API_KEY", default=None)
    print(f"🔑 GROQ_API_KEY: {'✅ Set' if groq_key else '❌ Missing'}")
    print(f"🔑 ELEVEN_LABS_API_KEY: {'✅ Set' if eleven_key else '❌ Missing'}")
except Exception as e:
    print(f"❌ Error loading environment variables: {str(e)}")

# Function to save conversation history
def save_conversation(user_message, assistant_response):
    """Save conversation to stored_data.json"""
    try:
        # Use absolute path to ensure file is found
        file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "stored_data.json")
        
        # Load existing data
        try:
            with open(file_name, "r") as user_file:
                data = json.load(user_file)
        except:
            data = []
        
        # Add new messages
        data.append({"role": "user", "content": user_message})
        data.append({"role": "assistant", "content": assistant_response})
        
        # Save updated data
        with open(file_name, "w") as user_file:
            json.dump(data, user_file)
        print(f"✅ Conversation saved to {file_name}")
        return True
    except Exception as e:
        print(f"❌ Error saving conversation: {str(e)}")
        print(traceback.format_exc())
        return False

#Initialize app
app = FastAPI()

#CORS - Origins
origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:4174",
    "http://localhost:3000",
]

#CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("🚀 FastAPI app initialized with CORS")

# Root endpoint
@app.get("/")
async def root():
    print("🏠 Root endpoint accessed")
    return {
        "message": "Welcome to the Chat with Rachel API", 
        "version": "2.0",
        "features": ["Local Whisper", "Groq API", "Fast responses"]
    }

#Reset Messages endpoint
@app.get("/reset")
async def reset_conversation():
    print("🔄 Reset endpoint accessed")
    try:
        reset_messages()
        print("✅ Messages reset successfully")
        return {"message": "conversation reset"}
    except Exception as e:
        print(f"❌ Error resetting messages: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Reset failed: {str(e)}")

#get audio endpoint
@app.get("/post-audio-get/")
async def get_audio():
    """Process audio file and return chat response"""
    print("\n" + "="*50)
    print("🎯 GET /post-audio-get/ endpoint accessed")
    print("="*50)
    
    try:
        # Try both relative and absolute paths
        audio_file_path = "voice.mp3"
        if not os.path.exists(audio_file_path):
            # Try absolute path
            audio_file_path = os.path.join(os.path.dirname(__file__), "voice.mp3")
            
        if not os.path.exists(audio_file_path):
            print(f"❌ Audio file not found: {audio_file_path}")
            print(f"📁 Current directory: {os.getcwd()}")
            print(f"📁 Files in current directory: {os.listdir('.')}")
            raise HTTPException(status_code=404, detail=f"Audio file not found in current directory: {os.getcwd()}")
        
        # Get file size for debugging
        file_size = os.path.getsize(audio_file_path)
        print(f"🎤 Found audio file: {audio_file_path} ({file_size} bytes)")
        
        # Decode audio using local Whisper (pass file path directly)
        print("🎤 Transcribing audio with local Whisper...")
        try:
            message_decoded = convert_audio_to_text(audio_file_path)
            print(f"📝 Transcription result: '{message_decoded}'")
        except Exception as e:
            print(f"❌ Error in convert_audio_to_text: {str(e)}")
            print(traceback.format_exc())
            raise HTTPException(status_code=400, detail=f"Audio transcription failed: {str(e)}")
        
        if not message_decoded or message_decoded.strip() == "":
            print("❌ Empty or None transcription result")
            raise HTTPException(status_code=400, detail="Could not decode audio. Check if the file is a valid audio format.")
        
        print(f"📝 Successfully transcribed: '{message_decoded}'")
        
        # Get chat response from Groq API
        print("🚀 Getting response from Groq API...")
        try:
            chat_response = get_chat_response(message_decoded)
            print(f"💬 Chat response received: '{chat_response}'")
        except Exception as e:
            print(f"❌ Error in get_chat_response: {str(e)}")
            print(traceback.format_exc())
            raise HTTPException(status_code=400, detail=f"Chat response failed: {str(e)}")

        if not chat_response or chat_response.strip() == "":
            print("❌ Empty or None chat response")
            raise HTTPException(status_code=400, detail="Could not get chat response from API.")
        
        print(f"✅ Successfully got chat response: '{chat_response}'")
        
        # Store messages
        try:
            print("💾 Storing messages to database...")
            store_messages(message_decoded, chat_response)
            print("✅ Messages stored successfully")
        except Exception as e:
            print(f"❌ Error storing messages: {str(e)}")
            print(traceback.format_exc())
        
        # Also save using the save_conversation function
        print("💾 Saving conversation to JSON...")
        save_conversation(message_decoded, chat_response)

        #Convert chat response to audio 
        print("🔊 Converting text to speech...")
        try:
            audio_output = convert_text_to_speech(chat_response)
            print(f"🔊 TTS result: {audio_output}")
        except Exception as e:
            print(f"❌ Error in convert_text_to_speech: {str(e)}")
            print(traceback.format_exc())
            raise HTTPException(status_code=400, detail=f"Text-to-speech failed: {str(e)}")

        if not audio_output:
            print("❌ Failed to get audio output from TTS")
            raise HTTPException(status_code=400, detail="Failed to get Eleven labs audio response.")

        print("✅ Successfully generated audio response")

        # Read the audio file
        try:
            with open(audio_output, "rb") as audio_file:
                audio_content = audio_file.read()
            print(f"🎵 Read audio file: {len(audio_content)} bytes")
        except Exception as e:
            print(f"❌ Error reading audio file: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error reading audio file: {str(e)}")

        #Create a generator that yields chunks of the data
        def iterfile():
            yield audio_content

        print("🎵 Returning audio stream response")
        print("="*50)
        
        #Return audio file as streaming response
        return StreamingResponse(iterfile(), media_type="audio/mpeg")
        
    except HTTPException as e:
        print(f"🚫 HTTP Exception: {e.detail}")
        print("="*50)
        # Re-raise HTTP exceptions
        raise e
    except Exception as e:
        print(f"❌ Unexpected error in get_audio: {str(e)}")
        print(traceback.format_exc())
        print("="*50)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

#get audio endpoint for frontend testing
@app.post("/post-audio/")
async def post_audio(file: UploadFile = File(...)):
    """Process audio file and return chat response"""
    print("\n" + "="*50)
    print("🎯 POST /post-audio/ endpoint accessed")
    print(f"📎 File: {file.filename}, Content-Type: {file.content_type}")
    print("="*50)
    
    try:
        #Save file for frontend testing
        print(f"💾 Saving uploaded file: {file.filename}")
        with open(file.filename, "wb") as buffer:
            content = file.file.read()
            buffer.write(content)
        print(f"✅ File saved: {len(content)} bytes")
        
        audio_input = open(file.filename, "rb")

        # Decode audio using local Whisper (pass file object)
        print("🎤 Transcribing audio with local Whisper...")
        try:
            message_decoded = convert_audio_to_text(audio_input)
            print(f"📝 Transcription result: '{message_decoded}'")
        except Exception as e:
            print(f"❌ Error in convert_audio_to_text: {str(e)}")
            print(traceback.format_exc())
            raise HTTPException(status_code=400, detail=f"Audio transcription failed: {str(e)}")
        finally:
            audio_input.close()
        
        if not message_decoded or message_decoded.strip() == "":
            print("❌ Empty or None transcription result")
            raise HTTPException(status_code=400, detail="Could not decode audio. Check if the file is a valid audio format.")
        
        print(f"📝 Successfully transcribed: '{message_decoded}'")
        
        # Get chat response from Groq API
        print("🚀 Getting response from Groq API...")
        try:
            chat_response = get_chat_response(message_decoded)
            print(f"💬 Chat response received: '{chat_response}'")
        except Exception as e:
            print(f"❌ Error in get_chat_response: {str(e)}")
            print(traceback.format_exc())
            raise HTTPException(status_code=400, detail=f"Chat response failed: {str(e)}")

        if not chat_response or chat_response.strip() == "":
            print("❌ Empty or None chat response")
            raise HTTPException(status_code=400, detail="Could not get chat response from API.")
        
        print(f"✅ Successfully got chat response: '{chat_response}'")

        # Store messages
        try:
            print("💾 Storing messages to database...")
            store_messages(message_decoded, chat_response)
            print("✅ Messages stored successfully")
        except Exception as e:
            print(f"❌ Error storing messages: {str(e)}")
            print(traceback.format_exc())

        #Convert chat response to audio 
        print("🔊 Converting text to speech...")
        try:
            audio_output = convert_text_to_speech(chat_response)
            print(f"🔊 TTS result: {audio_output}")
        except Exception as e:
            print(f"❌ Error in convert_text_to_speech: {str(e)}")
            print(traceback.format_exc())
            raise HTTPException(status_code=400, detail=f"Text-to-speech failed: {str(e)}")

        if not audio_output:
            print("❌ Failed to get audio output from TTS")
            raise HTTPException(status_code=400, detail="Failed to get Eleven labs audio response.")

        print("✅ Successfully generated audio response")

        # Read the audio file
        try:
            with open(audio_output, "rb") as audio_file:
                audio_content = audio_file.read()
            print(f"🎵 Read audio file: {len(audio_content)} bytes")
        except Exception as e:
            print(f"❌ Error reading audio file: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error reading audio file: {str(e)}")

        #Create a generator that yields chunks of the data
        def iterfile():
            yield audio_content

        print("🎵 Returning audio stream response")
        print("="*50)

        #Return audio file as streaming response
        return StreamingResponse(iterfile(), media_type="application/octet-stream")
        
    except HTTPException as e:
        print(f"🚫 HTTP Exception: {e.detail}")
        print("="*50)
        # Re-raise HTTP exceptions
        raise e
    except Exception as e:
        print(f"❌ Unexpected error in post_audio: {str(e)}")
        print(traceback.format_exc())
        print("="*50)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

print("🎉 Server setup complete!")