@echo off
title Restaurant Analytics — Python Dashboard
color 0A
echo.
echo  ================================================
echo   Restaurant Analytics Dashboard (Python)
echo   Installing dependencies and launching...
echo  ================================================
echo.

cd /d "e:\Restaurant Analysis project\python-dashboard"

echo [1/2] Installing required libraries...
pip install -r requirements.txt -q
echo       Done!
echo.

echo [2/2] Launching Streamlit dashboard...
echo       Open your browser to: http://localhost:8501
echo       Press Ctrl+C to stop
echo.

streamlit run app.py

pause
