import os
import sys
import subprocess

# Change to backend directory
os.chdir('backend')

# Use virtual environment's Python
venv_python = os.path.join('venv', 'Scripts', 'python.exe')

print('Current directory:', os.getcwd())
print('Using virtual environment Python:', venv_python)

# Test imports using virtual environment
test_code = '''
import sys
sys.path.append('.')

try:
    import main
    print('✅ Main module imported successfully')
except Exception as e:
    print('❌ Error importing main:', e)
    import traceback
    traceback.print_exc()

try:
    from functions.grouq_api import convert_audio_to_text, get_chat_response
    print('✅ Functions imported successfully')
except Exception as e:
    print('❌ Error importing functions:', e)
    import traceback
    traceback.print_exc()
'''

try:
    result = subprocess.run([venv_python, '-c', test_code],
                          capture_output=True, text=True, cwd=os.getcwd())

    print("STDOUT:")
    print(result.stdout)
    if result.stderr:
        print("STDERR:")
        print(result.stderr)

    if result.returncode == 0:
        print("✅ All imports successful!")
    else:
        print(f"❌ Import test failed with return code: {result.returncode}")

except Exception as e:
    print(f"❌ Error running test: {e}")
