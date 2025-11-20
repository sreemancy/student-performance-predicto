import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def train_model():
    # Load data
    data_path = os.path.join('..', 'data', 'student_data.csv')
    df = pd.read_csv(data_path)
    
    # Features and target
    X = df[['attendance', 'study_hours', 'internal_marks', 'assignments_submitted', 'activities']]
    y = df['performance']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Random Forest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.2f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save model
    joblib.dump(model, 'student_performance_model.pkl')
    print("Model saved as 'student_performance_model.pkl'")
    
    return model

if __name__ == "__main__":
    train_model()