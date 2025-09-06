@echo off
cd backend
call venv\Scripts\activate
pip install -r requirements.txt
echo Dependencies installed successfully
pause
