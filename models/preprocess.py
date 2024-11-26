import pandas as pd

def preprocess_data(data):
    # Example preprocessing steps:
    
    # Handle missing values (e.g., filling with mean or dropping rows)
    data = data.fillna(data.mean())
    
    # Feature engineering (e.g., extracting useful information from existing columns)
    data['BMI'] = data['weight'] / (data['height'] / 100) ** 2
    
    # Convert categorical features to numeric (e.g., one-hot encoding)
    data = pd.get_dummies(data, columns=['race', 'school', 'state'], drop_first=True)
    
    # Split into features (X) and target labels (y)
    X = data.drop('performance', axis=1)  # Assuming 'performance' is the target variable
    y = data['performance']

    return X, y