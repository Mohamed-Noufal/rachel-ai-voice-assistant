#install requirements.txt & activate venv
#cd D:\LLM\React\project\chat-with-Rachel\backend; .\venv\Scripts\Activate
#uvicorn main:app
#uvicorn main:app --reload


#Main Imports
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from decouple import config



#Custom Function Imports
from functions.openai_requests import convert_audio_to_text, get_chat_response


#Initialize  app
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

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to the Chat with Rachel API"}

#check health endpoint
@app.get("/health")
async def check_health():
    print("Health check endpoint called")
    return {"message": "hello world"}

#get audio endpoint
@app.get("/post-audio-get/")
async def get_audio():
    try:
        # Check if file exists first
        audio_input = open("voice.mp3", "rb")
        
        # Rest of your code...
        message_decoded = convert_audio_to_text(audio_input)
        
        if not message_decoded:
            raise HTTPException(status_code=400, detail="Could not decode audio")
        
        chat_response = get_chat_response(message_decoded)
        print(chat_response)
        
        return {"message": "Done", "response": chat_response}
        
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Audio file 'voice.mp3' not found")
    finally:
        if 'audio_input' in locals():
            audio_input.close()


#Post bot response
#Note:Not playing in browser when using post request
#@app.post("/post-audio/")
#async def post_audio(file: UploadFile = File(...)):

#    print("Hello")
