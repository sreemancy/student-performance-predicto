@echo off
echo Setting up Student Performance Predictor...

echo.
echo 1. Installing Python dependencies...
cd backend
pip install -r requirements.txt

echo.
echo 2. Training ML model...
python train_model.py

echo.
echo 3. Setup complete!
echo.
echo To run the application:
echo 1. Start backend: cd backend && python app.py
echo 2. Open frontend/index.html in your browser
echo.
pause