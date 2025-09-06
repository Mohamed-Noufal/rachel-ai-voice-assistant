import subprocess
import sys
import os

# Change to backend directory
os.chdir('backend')

# Activate virtual environment
venv_python = os.path.join('venv', 'Scripts', 'python.exe')
pip_path = os.path.join('venv', 'Scripts', 'pip.exe')

print("Installing whisper...")
try:
    # Try installing whisper
    result = subprocess.run([pip_path, 'install', 'openai-whisper'],
                          capture_output=True, text=True, timeout=300)

    if result.returncode == 0:
        print("✅ Whisper installed successfully!")
        print(result.stdout)
    else:
        print("❌ Failed to install whisper:")
        print(result.stderr)
        print("Trying alternative installation...")

        # Try alternative: pip install git+https://github.com/openai/whisper.git
        result2 = subprocess.run([pip_path, 'install', 'git+https://github.com/openai/whisper.git'],
                               capture_output=True, text=True, timeout=300)

        if result2.returncode == 0:
            print("✅ Whisper installed from git successfully!")
        else:
            print("❌ Git installation also failed:")
            print(result2.stderr)

except Exception as e:
    print(f"❌ Error during installation: {e}")
