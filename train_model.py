"""
Train ML Model Script
=====================
This script trains a calorie prediction model using scikit-learn.
It reads user profile data and trains a Random Forest regression model
to predict target calories based on user characteristics.

The trained model is saved as a joblib file for use in the application.
"""

import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import os
from pathlib import Path


def train_calorie_model():
    """
    Train a Random Forest model to predict target calories for users.
    
    Returns:
        dict: Contains training metrics and model information
    """
    
    # Define file paths
    data_dir = Path(__file__).parent / 'data'
    model_dir = Path(__file__).parent / 'models'
    
    # Create models directory if it doesn't exist
    model_dir.mkdir(exist_ok=True)
    
    try:
        # Load user profile data
        df = pd.read_csv(data_dir / 'user_profiles.csv')
        
        print("Data loaded successfully!")
        print(f"Dataset shape: {df.shape}")
        print(f"Features: {df.columns.tolist()}")
        
        # Prepare features and target
        X = df[['age', 'weight', 'height', 'activity_level', 'metabolism_rate']]
        y = df['target_calories']
        
        # Split data into training and testing sets (80-20 split)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Standardize features for better model performance
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train Random Forest model with optimized hyperparameters
        model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            min_samples_split=2,
            min_samples_leaf=1,
            random_state=42,
            n_jobs=-1
        )
        
        print("\nTraining the model...")
        model.fit(X_train_scaled, y_train)
        
        # Make predictions on test set
        y_pred_train = model.predict(X_train_scaled)
        y_pred_test = model.predict(X_test_scaled)
        
        # Calculate performance metrics
        train_r2 = r2_score(y_train, y_pred_train)
        test_r2 = r2_score(y_test, y_pred_test)
        train_rmse = mean_squared_error(y_train, y_pred_train) ** 0.5
        test_rmse = mean_squared_error(y_test, y_pred_test) ** 0.5
        
        print("\n" + "="*50)
        print("MODEL TRAINING RESULTS")
        print("="*50)
        print(f"Training R² Score: {train_r2:.4f}")
        print(f"Testing R² Score: {test_r2:.4f}")
        print(f"Training RMSE: {train_rmse:.2f}")
        print(f"Testing RMSE: {test_rmse:.2f}")
        print("="*50)
        
        # Feature importance analysis
        feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\nFeature Importance:")
        print(feature_importance.to_string(index=False))
        
        # Save the trained model
        model_path = model_dir / 'calorie_model.pkl'
        joblib.dump(model, model_path)
        print(f"\n✓ Model saved to: {model_path}")
        
        # Save the scaler for later use
        scaler_path = model_dir / 'scaler.pkl'
        joblib.dump(scaler, scaler_path)
        print(f"✓ Scaler saved to: {scaler_path}")
        
        # Return training metrics
        return {
            'train_r2': train_r2,
            'test_r2': test_r2,
            'train_rmse': train_rmse,
            'test_rmse': test_rmse,
            'feature_importance': feature_importance.to_dict('records')
        }
        
    except FileNotFoundError as e:
        print(f"Error: Data file not found - {e}")
        print(f"Make sure user_profiles.csv exists in the data folder")
        return None
    except Exception as e:
        print(f"Error during training: {e}")
        return None


if __name__ == "__main__":
    print("Starting Calorie Prediction Model Training...\n")
    results = train_calorie_model()
    
    if results:
        print("\n✓ Model training completed successfully!")
    else:
        print("\n✗ Model training failed!")
