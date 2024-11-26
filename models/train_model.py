import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression  # Example model
# Import other models (ensemble model? Neural Network)
from joblib import dump
from preprocess import preprocess_data  # Import the preprocessing steps

def train_model():
    # Load your dataset (adjust file path as needed)
    data = pd.read_csv('track_and_field_data.csv')
    
      # Preprocess the data
    X, y = preprocess_data(data)
    
     # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale the features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.fit_transform(X_test)
    
    # Train the model (LinearRegression is just an example; use your own model)
    model = LinearRegression()
    model.fit(X_train_scaled, y_train)
    
    dump(model, 'model.pkl')
    dump(scaler, 'scaler.pkl')
    
    score = model.score(X_test_scaled, y_test)
    print(f'Model accuracy: {score:.2f}')

if __name__ == '__main__':
    train_model()
