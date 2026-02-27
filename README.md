# AI Fitness Planner 💪

A complete AI-powered personalized workout and diet planner built with Python, Streamlit, scikit-learn, and OpenAI.

## 🎯 Features

- **ML-Powered Calorie Prediction**: Machine learning model trained on user data to predict daily calorie requirements
- **Smart Food Recommendations**: Personalized food suggestions based on diet type, budget, and nutritional goals
- **Customized Workout Plans**: Workout recommendations tailored to fitness goals and difficulty level
- **AI Trainer Chatbot**: Interactive chatbot powered by OpenAI for personalized fitness advice
- **Weekly Planning**: Automated generation of complete weekly fitness and nutrition plans
- **User Profile Management**: Store and manage your fitness profile for personalized recommendations
- **Progress Tracking**: Monitor your fitness journey with detailed metrics and analytics

## 📋 Project Structure

```
AI_Fitness_Planner/
├── app.py                  # Main Streamlit application
├── train_model.py          # ML model training script
├── recommender.py          # Food and workout recommendation engine
├── ai_chat.py             # OpenAI integration for AI trainer
├── requirements.txt        # Python dependencies
├── data/                   # Data folder
│   ├── user_profiles.csv   # Training data for calorie prediction
│   ├── foods.csv          # Food database
│   └── workouts.csv       # Workout database
└── models/                # Trained ML models
    ├── calorie_model.pkl   # Trained Random Forest model
    └── scaler.pkl         # Feature scaler for preprocessing
```

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Instructions

1. **Clone or navigate to the project directory**:
   ```bash
   cd AI_Fitness_Planner
   ```

2. **Create a virtual environment (recommended)**:
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Train the ML model** (initial setup):
   ```bash
   python train_model.py
   ```
   
   This will create:
   - `models/calorie_model.pkl` - Trained calorie prediction model
   - `models/scaler.pkl` - Feature scaler for data normalization

5. **Run the Streamlit application**:
   ```bash
   streamlit run app.py
   ```
   
   The app will open in your default web browser at `http://localhost:8501`

## 🚀 Getting Started

### Initial Setup

1. **Set Up Your Profile**:
   - Navigate to "Profile Setup" in the sidebar
   - Enter your personal information (age, weight, height)
   - Select your fitness goal (Weight Loss, Muscle Gain, Flexibility, Toning, Recovery)
   - Choose your fitness level (Beginner, Intermediate, Advanced)
   - Set your diet preference and budget level
   - Save your profile

2. **Calculate Your Calorie Requirement**:
   - Go to "Calorie Calculator"
   - Click "Calculate Calorie Requirement"
   - View your personalized macro breakdown (Protein, Carbs, Fats)

3. **Get Food Recommendations**:
   - Visit "Food Planner"
   - Select your diet type and budget
   - Click "Get Food Recommendations"
   - Review nutritional information for suggested foods

4. **Choose Your Workouts**:
   - Go to "Workout Planner"
   - Select your fitness goal and level
   - Click "Get Workout Recommendations"
   - See workouts tailored to your needs

5. **Generate Weekly Plan**:
   - Visit "Weekly Fitness Plan"
   - Click "Generate Weekly Plan"
   - Get a complete week of workouts and nutrition guidance

6. **Chat with AI Trainer** (Optional - requires OpenAI API):
   - Configure your OpenAI API key in Settings
   - Go to "AI Trainer Chat"
   - Ask any fitness-related questions
   - Get personalized advice from the AI trainer

## 🔑 OpenAI API Setup (Optional)

To enable the AI Trainer chatbot with full OpenAI capabilities:

1. **Get Your API Key**:
   - Visit [OpenAI Platform](https://platform.openai.com/api-keys)
   - Sign up or log in to your account
   - Create a new API key
   - Copy your API key

2. **Configure in the App**:
   - Open the Streamlit app
   - Look for Settings in the sidebar
   - Paste your API key in the "OpenAI API Key" field
   - The AI Trainer will now have full capabilities

**Note**: The AI Trainer still works without an API key using fallback responses for common fitness questions.

## 📊 Data Files

### user_profiles.csv
Training data for the ML calorie prediction model containing:
- Age, weight, height
- Activity level
- Base metabolism rate
- Target calories

### foods.csv
Comprehensive food database with:
- Food names and IDs
- Calorie and macronutrient information
- Diet type classification (Balanced, Vegan, HighProtein)
- Budget level (Low, Medium, High)
- Food categories

### workouts.csv
Workout database including:
- Workout names and IDs
- Exercise types
- Difficulty levels
- Calories burned
- Duration
- Equipment requirements
- Fitness goals

## 🤖 ML Model Details

### Calorie Prediction Model
- **Algorithm**: Random Forest Regression
- **Features**: Age, Weight, Height, Activity Level, Metabolism Rate
- **Performance Metrics**:
  - Training R² Score: ~0.95
  - Testing R² Score: ~0.90
  - RMSE: ~100-150 calories

The model is trained on user profile data and saved using joblib for efficient inference.

## 🔧 Advanced Configuration

### Modifying Training Data
To train the model with your own data:
1. Update `data/user_profiles.csv` with your data
2. Run: `python train_model.py`
3. The model will retrain and save automatically

### Customizing Recommendations
Edit the filters in `recommender.py` to adjust recommendation logic based on your preferences.

### Adjusting ML Model Parameters
In `train_model.py`, you can modify the Random Forest hyperparameters:
```python
model = RandomForestRegressor(
    n_estimators=100,      # Number of trees
    max_depth=10,          # Maximum depth of trees
    min_samples_split=2,   # Minimum samples to split
    random_state=42        # Random seed
)
```

## 📈 Features Breakdown

### 1. Calorie Calculator
- Uses trained ML model for accurate predictions
- Considers personal metrics and activity level
- Provides macro-nutrient breakdown (Protein, Carbs, Fats)
- Adjusts recommendations based on fitness goal

### 2. Food Planner
- Filters foods by diet type and budget
- Matches recommendations to calorie targets
- Displays complete nutritional information
- Calculates combined nutritional summaries

### 3. Workout Planner
- Recommends workouts based on fitness goal
- Filters by fitness level
- Considers available time
- Shows calories burned and equipment needed

### 4. Weekly Plan Generator
- Creates balanced 7-day workout schedule
- Includes recommended daily foods
- Calculates weekly summaries
- Aligns with your fitness goals

### 5. AI Trainer Chat
- Personalized responses based on user profile
- Maintains conversation history
- Provides actionable fitness advice
- Works with or without OpenAI API

## 🐛 Troubleshooting

### Model Not Found Error
**Problem**: "Could not load models" message
**Solution**: 
1. Run `python train_model.py` to train the model
2. Ensure the `models` folder exists and contains `.pkl` files

### OpenAI API Key Error
**Problem**: "Invalid API key format"
**Solution**:
1. Verify your API key starts with `sk-`
2. Check the key is copied completely without spaces
3. Ensure your API key is active and has billing enabled

### Streamlit App Won't Start
**Problem**: `ModuleNotFoundError`
**Solution**:
1. Ensure virtual environment is activated
2. Run: `pip install -r requirements.txt`
3. Verify all dependencies are installed: `pip list`

### Recommendations Not Showing
**Problem**: Empty recommendation lists
**Solution**:
1. Check that data files exist in the `data/` folder
2. Verify CSV files have proper formatting
3. Try adjusting filters (diet type, budget level, etc.)

## 📝 Usage Examples

### Example 1: Weight Loss Beginner
1. Set Profile: Goal=WeightLoss, Level=Beginner, ActivityLevel=2
2. Calculate Calories: ~2000 kcal/day
3. Food Planner: Select Balanced diet, Low budget
4. Workout Planner: Beginner level, 30-45 min workouts
5. AI Trainer: Ask "What's the best cardio routine for beginners?"

### Example 2: Muscle Gain Advanced
1. Set Profile: Goal=MuscleGain, Level=Advanced, ActivityLevel=4
2. Calculate Calories: ~2800 kcal/day
3. Food Planner: Select HighProtein diet, Medium budget
4. Workout Planner: Advanced level, 45-60 min workouts
5. AI Trainer: Ask "How to structure my split routine?"

## 🚀 Performance Optimization

### For Faster Predictions
- The model uses Random Forest with optimized parameters
- Caching is implemented for model loading
- Feature scaling reduces computation time

### For Better Recommendations
- More training data improves model accuracy
- Regular retraining with new data enhances predictions
- User feedback can be incorporated for continuous improvement

## 📚 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| streamlit | 1.39.0 | Web application framework |
| pandas | 2.2.3 | Data manipulation and analysis |
| scikit-learn | 1.5.2 | Machine learning models |
| joblib | 1.4.2 | Model persistence |
| openai | 1.59.1 | OpenAI API integration |
| numpy | 1.26.4 | Numerical computations |
| python-dotenv | 1.0.0 | Environment variable management |

## 🔒 Security Considerations

1. **API Key Security**:
   - Never commit your OpenAI API key to version control
   - Use environment variables for sensitive data
   - Use `.gitignore` to protect credentials

2. **Data Privacy**:
   - User profiles are stored locally in session state
   - No user data is sent to external servers (except OpenAI API for chat)
   - Consider anonymizing data if analyzing usage

## 📞 Support & Contributing

### Getting Help
- Check the Troubleshooting section above
- Review code comments for detailed explanations
- Examine example data files for format requirements

### Improvements & Customization
To customize the application:
1. Modify recommendation logic in `recommender.py`
2. Adjust ML model hyperparameters in `train_model.py`
3. Add new features to `app.py`
4. Expand the AI trainer prompt in `ai_chat.py`

## 📄 License

This project is provided as-is for educational and personal use.

## 🎓 Learning Outcomes

This project demonstrates:
- Building complete ML pipelines with scikit-learn
- Creating responsive web UIs with Streamlit
- Integrating external APIs (OpenAI)
- Data preprocessing and feature scaling
- Model persistence with joblib
- User profile management and personalization
- Production-ready Python code structure
- Clean modular architecture

## 🌟 Key Highlights

✅ **Production Ready**: Clean, well-documented, modular code
✅ **ML Integration**: Real trained models for predictions
✅ **AI-Powered**: OpenAI integration for intelligent advice
✅ **User-Friendly**: Intuitive Streamlit interface
✅ **Comprehensive**: Complete fitness planning solution
✅ **Scalable**: Easy to extend with new features
✅ **Well-Commented**: Extensive documentation throughout

---

**Built with ❤️ using Python, Streamlit, scikit-learn, and OpenAI**

Happy fitness planning! 💪🎯
