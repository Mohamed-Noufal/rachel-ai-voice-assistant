import subprocess
import os

# Change to backend directory
os.chdir('backend')

# Use virtual environment
venv_python = os.path.join('venv', 'Scripts', 'python.exe')
uvicorn_path = os.path.join('venv', 'Scripts', 'uvicorn.exe')

print("Starting server with virtual environment...")
print(f"Python: {venv_python}")
print(f"Uvicorn: {uvicorn_path}")

try:
    # Start uvicorn server
    result = subprocess.run([
        uvicorn_path,
        'main:app',
        '--host', '127.0.0.1',
        '--port', '8000',
        '--reload'
    ], cwd=os.getcwd(), timeout=10)  # 10 second timeout for testing

    print(f"Server exited with code: {result.returncode}")

except subprocess.TimeoutExpired:
    print("✅ Server started successfully (timeout reached as expected)")
except Exception as e:
    print(f"❌ Error starting server: {e}")
