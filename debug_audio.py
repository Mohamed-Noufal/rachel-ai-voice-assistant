import os
import subprocess

# Change to backend directory
os.chdir('backend')

# Use virtual environment
venv_python = os.path.join('venv', 'Scripts', 'python.exe')

print("Debugging audio file processing...")

# Check if voice.mp3 exists and get its info
audio_file = 'voice.mp3'
if os.path.exists(audio_file):
    file_size = os.path.getsize(audio_file)
    print(f"✅ Audio file exists: {audio_file} ({file_size} bytes)")

    # Test whisper directly on the file
    test_code = f'''
import whisper
import os

print("Testing Whisper directly...")
model = whisper.load_model("base")
result = model.transcribe("{audio_file}", fp16=False)
print("Transcription result:", result["text"])
'''

    try:
        print("Running Whisper test...")
        result = subprocess.run([venv_python, '-c', test_code],
                              capture_output=True, text=True, cwd=os.getcwd(), timeout=60)

        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)

        if result.returncode == 0:
            print("✅ Whisper test successful!")
        else:
            print(f"❌ Whisper test failed with code: {result.returncode}")

    except subprocess.TimeoutExpired:
        print("❌ Whisper test timed out")
    except Exception as e:
        print(f"❌ Error running Whisper test: {e}")

else:
    print(f"❌ Audio file not found: {audio_file}")
    print("Files in directory:", os.listdir('.'))
