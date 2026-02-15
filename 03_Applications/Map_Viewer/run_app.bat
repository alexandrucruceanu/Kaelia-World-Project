@echo off
cd /d "%~dp0"
echo Starting Kaelia Map Viewer...
echo --------------------------------
echo 1. Launching Server (node server.js)...
start "Kaelia Map Server" node server.js

echo 2. Waiting for server to initialize...
timeout /t 3 >nul

echo 3. Opening Application...
start http://localhost:3000

echo --------------------------------
echo Done! You can close this window, but keep the Server window open.
timeout /t 5
