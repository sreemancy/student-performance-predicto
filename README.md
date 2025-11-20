# Student Performance Predictor

A full-stack web application that predicts student academic performance (Pass/Fail) based on key factors like attendance, study hours, internal marks, assignments, and activities.

## Features

- **Machine Learning**: Random Forest classifier for accurate predictions
- **Web Interface**: Clean, responsive HTML/CSS/JS frontend
- **REST API**: Flask backend with prediction endpoints
- **Database**: SQLite for storing prediction history
- **Real-time Predictions**: Instant results with confidence levels

## Project Structure

```
studentperfo/
├── backend/
│   ├── app.py              # Flask API server
│   ├── train_model.py      # ML model training
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── index.html         # Main web interface
│   ├── style.css          # Styling
│   └── script.js          # Frontend logic
├── data/
│   └── student_data.csv   # Training dataset
└── README.md
```

## Setup Instructions

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Train the ML Model

```bash
cd backend
python train_model.py
```

### 3. Start the Backend Server

```bash
cd backend
python app.py
```

The API will be available at `http://localhost:5000`

### 4. Open the Frontend

Open `frontend/index.html` in your web browser or serve it using a local server:

```bash
cd frontend
python -m http.server 8000
```

Then visit `http://localhost:8000`

## Usage

1. Enter student details in the form:
   - Attendance percentage (0-100)
   - Study hours per day (0-24)
   - Internal marks percentage (0-100)
   - Number of assignments submitted (0-20)
   - Activities participated (0-10)

2. Click "Predict Performance" to get the result

3. View prediction history by clicking "Load History"

## API Endpoints

- `POST /predict` - Make a prediction
- `GET /history` - Get prediction history
- `GET /health` - Check API health

## Model Performance

The Random Forest model is trained on sample data with features:
- Attendance percentage
- Daily study hours
- Internal marks
- Assignments submitted
- Activities participated

The model provides both prediction (Pass/Fail) and confidence level.

## Technologies Used

- **Backend**: Python, Flask, Scikit-learn, SQLite
- **Frontend**: HTML5, CSS3, JavaScript
- **ML**: Random Forest Classifier
- **Database**: SQLite

## Future Enhancements

- Add more sophisticated ML models
- Implement user authentication
- Add data visualization charts
- Deploy to cloud platforms
- Add more input features