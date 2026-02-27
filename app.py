"""
AI Fitness Planner - Main Streamlit Application
================================================
Complete fitness and diet planning application with ML-based calorie prediction,
personalized food and workout recommendations, and AI trainer chatbot.

Features:
- Calorie prediction using trained ML model
- Food recommendations based on diet type and budget
- Workout recommendations based on fitness goals
- AI trainer chatbot for personalized advice
- User profile management
- Weekly fitness planning
"""

import streamlit as st
import pandas as pd
import joblib
from pathlib import Path
import os
from datetime import datetime

# Import custom modules
from recommender import FoodRecommender, WorkoutRecommender, get_nutritional_summary
from ai_chat import AITrainer, validate_api_key


# ==================== PAGE CONFIGURATION ====================

st.set_page_config(
    page_title="AI Fitness Planner",
    page_icon="💪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        color: #FF6B6B;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .success-text {
        color: #28a745;
        font-weight: bold;
    }
    .warning-text {
        color: #ffc107;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)


# ==================== HELPER FUNCTIONS ====================

@st.cache_resource
def load_models():
    """
    Load trained ML models and scalers.
    
    Returns:
        tuple: (model, scaler) or (None, None) if models not found
    """
    try:
        model_dir = Path(__file__).parent / 'models'
        
        # Check if models exist
        if not (model_dir / 'calorie_model.pkl').exists():
            return None, None
        
        model = joblib.load(model_dir / 'calorie_model.pkl')
        scaler = joblib.load(model_dir / 'scaler.pkl')
        return model, scaler
    except Exception as e:
        st.warning(f"Could not load models: {e}")
        return None, None


@st.cache_resource
def init_recommenders():
    """
    Initialize food and workout recommenders.
    
    Returns:
        tuple: (FoodRecommender, WorkoutRecommender)
    """
    return FoodRecommender(), WorkoutRecommender()


def predict_calorie_requirement(age, weight, height, activity_level, metabolism_rate):
    """
    Predict calorie requirement using the trained ML model.
    
    Args:
        age (int): User's age
        weight (float): User's weight in kg
        height (float): User's height in cm
        activity_level (int): Activity level (1-5)
        metabolism_rate (int): Base metabolism rate
    
    Returns:
        float: Predicted daily calorie requirement
    """
    model, scaler = load_models()
    
    if model is None:
        # Fallback calculation if model not available
        return weight * 10 + height / 6.25 + age * 5 - 161 + (activity_level * 100)
    
    try:
        # Prepare input data
        input_data = [[age, weight, height, activity_level, metabolism_rate]]
        input_scaled = scaler.transform(input_data)
        
        # Make prediction
        prediction = model.predict(input_scaled)[0]
        return max(prediction, 1200)  # Ensure minimum viable calorie count
    except Exception as e:
        st.error(f"Error in calorie prediction: {e}")
        return 2000  # Default fallback value


# ==================== MAIN APPLICATION ====================

def main():
    """Main application entry point."""
    
    # Initialize session state
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {}
    if 'ai_trainer' not in st.session_state:
        st.session_state.ai_trainer = None
    if 'models_trained' not in st.session_state:
        st.session_state.models_trained = load_models()[0] is not None
    
    # Sidebar
    with st.sidebar:
        st.title("🏋️ AI Fitness Planner")
        st.markdown("---")
        
        # Navigation
        page = st.radio(
            "Navigate to:",
            ["Home", "Profile Setup", "Calorie Calculator", "Food Planner", 
             "Workout Planner", "Weekly Plan", "AI Trainer Chat"]
        )
        
        st.markdown("---")
        
        # API Key Configuration
        st.subheader("⚙️ Settings")
        api_key_input = st.text_input(
            "OpenAI API Key (optional):",
            type="password",
            help="Get your API key from https://platform.openai.com/api-keys"
        )
        
        if api_key_input:
            if validate_api_key(api_key_input):
                st.session_state.ai_trainer = AITrainer(api_key=api_key_input)
                st.success("✓ API Key configured!")
            else:
                st.error("Invalid API key format")
    
    # Main content area
    if page == "Home":
        show_home_page()
    elif page == "Profile Setup":
        show_profile_setup()
    elif page == "Calorie Calculator":
        show_calorie_calculator()
    elif page == "Food Planner":
        show_food_planner()
    elif page == "Workout Planner":
        show_workout_planner()
    elif page == "Weekly Plan":
        show_weekly_plan()
    elif page == "AI Trainer Chat":
        show_ai_trainer()


# ==================== PAGE: HOME ====================

def show_home_page():
    """Display the home page with overview and features."""
    
    st.markdown('<h1 class="main-header">💪 Welcome to AI Fitness Planner</h1>', 
                unsafe_allow_html=True)
    
    st.markdown("""
    Your personal AI-powered fitness and nutrition companion designed to help you achieve 
    your health goals with personalized recommendations and expert guidance.
    """)
    
    st.markdown("---")
    
    # Features Overview
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Key Features")
        features = [
            "📊 Smart calorie prediction using machine learning",
            "🍽️ Personalized food recommendations",
            "🏃 Customized workout plans",
            "🤖 AI trainer chatbot (powered by OpenAI)",
            "📈 Progress tracking and analytics",
            "📋 Weekly fitness planning"
        ]
        for feature in features:
            st.write(f"• {feature}")
    
    with col2:
        st.subheader("🚀 Getting Started")
        steps = [
            ("1", "Set up your profile with your fitness details"),
            ("2", "Use the calorie calculator to find your daily needs"),
            ("3", "Get personalized food recommendations"),
            ("4", "Choose workouts matched to your goals"),
            ("5", "Chat with the AI trainer for expert advice"),
            ("6", "Create and follow your weekly plan")
        ]
        for num, step in steps:
            st.write(f"**{num}.** {step}")
    
    st.markdown("---")
    
    # Quick Stats
    st.subheader("📊 System Information")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("ML Model Status", "✓ Ready" if st.session_state.models_trained else "⚠ Not trained")
    
    with col2:
        st.metric("AI Trainer", "✓ Ready" if st.session_state.ai_trainer else "⚠ Not configured")
    
    with col3:
        food_rec, _ = init_recommenders()
        st.metric("Foods Available", len(food_rec.foods_df))
    
    with col4:
        _, workout_rec = init_recommenders()
        st.metric("Workouts Available", len(workout_rec.workouts_df))
    
    st.markdown("---")
    
    st.info("""
    💡 **Tip**: Start by setting up your profile in the "Profile Setup" section to get 
    the most personalized recommendations!
    """)


# ==================== PAGE: PROFILE SETUP ====================

def show_profile_setup():
    """Display user profile setup page."""
    
    st.markdown('<h1 class="main-header">👤 Your Fitness Profile</h1>', 
                unsafe_allow_html=True)
    
    st.write("Create or update your fitness profile for personalized recommendations.")
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Personal Information")
            name = st.text_input("Name", value=st.session_state.user_profile.get('name', ''))
            age = st.number_input("Age", min_value=13, max_value=120, 
                                 value=st.session_state.user_profile.get('age', 25))
            weight = st.number_input("Weight (kg)", min_value=30.0, max_value=300.0,
                                    value=st.session_state.user_profile.get('weight', 70.0),
                                    step=0.1)
            height = st.number_input("Height (cm)", min_value=100.0, max_value=250.0,
                                    value=st.session_state.user_profile.get('height', 175.0),
                                    step=0.1)
        
        with col2:
            st.subheader("Fitness Details")
            fitness_goal = st.selectbox(
                "Fitness Goal",
                ["WeightLoss", "MuscleGain", "Flexibility", "Toning", "Recovery"],
                index=0 if st.session_state.user_profile.get('fitness_goal') is None 
                      else ["WeightLoss", "MuscleGain", "Flexibility", "Toning", "Recovery"]
                           .index(st.session_state.user_profile.get('fitness_goal', 'WeightLoss'))
            )
            
            fitness_level = st.selectbox(
                "Fitness Level",
                ["Beginner", "Intermediate", "Advanced"],
                index=0 if st.session_state.user_profile.get('fitness_level') is None
                      else ["Beginner", "Intermediate", "Advanced"]
                           .index(st.session_state.user_profile.get('fitness_level', 'Beginner'))
            )
            
            activity_level = st.slider(
                "Activity Level (1=Sedentary to 5=Very Active)",
                min_value=1, max_value=5,
                value=st.session_state.user_profile.get('activity_level', 3)
            )
            
            metabolism_rate = st.number_input(
                "Base Metabolism Rate (optional)",
                min_value=800, max_value=3000,
                value=st.session_state.user_profile.get('metabolism_rate', 1500),
                help="Leave as default if unsure"
            )
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Nutrition Preferences")
            diet_preference = st.selectbox(
                "Diet Type",
                ["Balanced", "Vegan", "HighProtein"],
                index=0 if st.session_state.user_profile.get('diet_preference') is None
                      else ["Balanced", "Vegan", "HighProtein"]
                           .index(st.session_state.user_profile.get('diet_preference', 'Balanced'))
            )
            
            budget_level = st.selectbox(
                "Budget Level",
                ["Low", "Medium", "High"],
                index=0 if st.session_state.user_profile.get('budget_level') is None
                      else ["Low", "Medium", "High"]
                           .index(st.session_state.user_profile.get('budget_level', 'Low'))
            )
        
        with col2:
            st.subheader("Availability")
            days_per_week = st.slider(
                "Days Available for Workouts",
                min_value=1, max_value=7,
                value=st.session_state.user_profile.get('days_per_week', 5)
            )
            
            available_time = st.number_input(
                "Average Daily Workout Time (minutes)",
                min_value=15, max_value=180,
                value=st.session_state.user_profile.get('available_time', 60),
                step=5
            )
        
        st.markdown("---")
        
        submit = st.form_submit_button("💾 Save Profile", use_container_width=True)
        
        if submit:
            # Save profile to session state
            st.session_state.user_profile = {
                'name': name,
                'age': age,
                'weight': weight,
                'height': height,
                'fitness_goal': fitness_goal,
                'fitness_level': fitness_level,
                'activity_level': activity_level,
                'metabolism_rate': metabolism_rate,
                'diet_preference': diet_preference,
                'budget_level': budget_level,
                'days_per_week': days_per_week,
                'available_time': available_time
            }
            
            st.success("✅ Profile saved successfully!")
            st.balloons()


# ==================== PAGE: CALORIE CALCULATOR ====================

def show_calorie_calculator():
    """Display calorie calculator page."""
    
    st.markdown('<h1 class="main-header">🔥 Calorie Calculator</h1>', 
                unsafe_allow_html=True)
    
    st.write("Calculate your daily calorie requirement based on your profile using AI.")
    
    if not st.session_state.user_profile:
        st.warning("⚠️ Please set up your profile first in the 'Profile Setup' section.")
        return
    
    user = st.session_state.user_profile
    
    # Display user info
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Age", f"{user.get('age', 'N/A')} years")
    with col2:
        st.metric("Weight", f"{user.get('weight', 'N/A')} kg")
    with col3:
        st.metric("Height", f"{user.get('height', 'N/A')} cm")
    with col4:
        st.metric("Activity Level", f"{user.get('activity_level', 'N/A')}/5")
    
    st.markdown("---")
    
    # Calculate calorie requirement
    if st.button("📊 Calculate Calorie Requirement", use_container_width=True):
        with st.spinner("Calculating using ML model..."):
            calories = predict_calorie_requirement(
                age=user['age'],
                weight=user['weight'],
                height=user['height'],
                activity_level=user['activity_level'],
                metabolism_rate=user.get('metabolism_rate', 1500)
            )
        
        st.session_state.user_profile['predicted_calories'] = calories
        
        # Display result
        st.markdown("---")
        st.subheader("Your Daily Calorie Requirement")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Daily Calories", f"{int(calories)} kcal", 
                     delta=f"For {user['fitness_goal']}")
        
        with col2:
            weekly = calories * 7
            st.metric("Weekly Total", f"{int(weekly):,} kcal")
        
        with col3:
            monthly = calories * 30
            st.metric("Monthly Total", f"{int(monthly):,} kcal")
        
        st.markdown("---")
        
        # Macro breakdown
        st.subheader("📊 Recommended Macro Breakdown")
        
        # Adjust macros based on fitness goal
        if user['fitness_goal'] == 'MuscleGain':
            protein_pct, carb_pct, fat_pct = 0.30, 0.50, 0.20
            goal_text = "Muscle Building Focus"
        elif user['fitness_goal'] == 'WeightLoss':
            protein_pct, carb_pct, fat_pct = 0.35, 0.40, 0.25
            goal_text = "Weight Loss Focus"
        elif user['fitness_goal'] == 'Flexibility':
            protein_pct, carb_pct, fat_pct = 0.25, 0.50, 0.25
            goal_text = "Flexibility Focus"
        else:
            protein_pct, carb_pct, fat_pct = 0.30, 0.45, 0.25
            goal_text = "Balanced Nutrition"
        
        st.info(f"**{goal_text}** - Recommended macronutrient distribution")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            protein_cal = calories * protein_pct
            protein_g = protein_cal / 4
            st.metric("🥩 Protein", f"{int(protein_g)}g", 
                     f"{int(protein_pct*100)}% ({int(protein_cal)} cal)")
        
        with col2:
            carb_cal = calories * carb_pct
            carb_g = carb_cal / 4
            st.metric("🌾 Carbs", f"{int(carb_g)}g",
                     f"{int(carb_pct*100)}% ({int(carb_cal)} cal)")
        
        with col3:
            fat_cal = calories * fat_pct
            fat_g = fat_cal / 9
            st.metric("🥑 Fats", f"{int(fat_g)}g",
                     f"{int(fat_pct*100)}% ({int(fat_cal)} cal)")


# ==================== PAGE: FOOD PLANNER ====================

def show_food_planner():
    """Display food recommendation page."""
    
    st.markdown('<h1 class="main-header">🍽️ Food Planner</h1>', 
                unsafe_allow_html=True)
    
    st.write("Get personalized food recommendations based on your preferences.")
    
    if not st.session_state.user_profile:
        st.warning("⚠️ Please set up your profile first.")
        return
    
    user = st.session_state.user_profile
    food_recommender, _ = init_recommenders()
    
    col1, col2 = st.columns(2)
    
    with col1:
        diet_type = st.selectbox(
            "Diet Type",
            food_recommender.get_all_diet_types(),
            index=0 if user.get('diet_preference') is None
                  else list(food_recommender.get_all_diet_types()).index(
                      user.get('diet_preference', 'Balanced'))
        )
    
    with col2:
        budget_level = st.selectbox(
            "Budget Level",
            food_recommender.get_budget_levels(),
            index=0 if user.get('budget_level') is None
                  else list(food_recommender.get_budget_levels()).index(
                      user.get('budget_level', 'Low'))
        )
    
    num_recommendations = st.slider("Number of Recommendations", 
                                   min_value=3, max_value=15, value=5)
    
    if st.button("🔍 Get Food Recommendations", use_container_width=True):
        target_calories = user.get('predicted_calories', 2000)
        
        recommendations = food_recommender.recommend_foods(
            diet_type=diet_type,
            budget_level=budget_level,
            target_calories=int(target_calories),
            count=num_recommendations
        )
        
        if recommendations:
            st.subheader("Recommended Foods")
            
            # Create dataframe for display
            df_display = pd.DataFrame([
                {
                    'Food': food['food_name'],
                    'Calories': food['calories'],
                    'Protein (g)': round(food['protein'], 1),
                    'Carbs (g)': round(food['carbs'], 1),
                    'Fats (g)': round(food['fats'], 1),
                    'Category': food['category']
                }
                for food in recommendations
            ])
            
            st.dataframe(df_display, use_container_width=True)
            
            # Nutritional summary
            st.markdown("---")
            st.subheader("📊 Nutritional Summary")
            
            summary = get_nutritional_summary(recommendations)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Calories", f"{int(summary['total_calories'])}")
            
            with col2:
                st.metric("Total Protein", f"{round(summary['total_protein'], 1)}g")
            
            with col3:
                st.metric("Total Carbs", f"{round(summary['total_carbs'], 1)}g")
            
            with col4:
                st.metric("Total Fats", f"{round(summary['total_fats'], 1)}g")
        else:
            st.error("No recommendations found for selected criteria.")


# ==================== PAGE: WORKOUT PLANNER ====================

def show_workout_planner():
    """Display workout recommendation page."""
    
    st.markdown('<h1 class="main-header">🏃 Workout Planner</h1>', 
                unsafe_allow_html=True)
    
    st.write("Get personalized workout recommendations based on your goals and fitness level.")
    
    if not st.session_state.user_profile:
        st.warning("⚠️ Please set up your profile first.")
        return
    
    user = st.session_state.user_profile
    _, workout_recommender = init_recommenders()
    
    col1, col2 = st.columns(2)
    
    with col1:
        fitness_goal = st.selectbox(
            "Fitness Goal",
            workout_recommender.get_all_goals(),
            index=0 if user.get('fitness_goal') is None
                  else list(workout_recommender.get_all_goals()).index(
                      user.get('fitness_goal', 'WeightLoss'))
        )
    
    with col2:
        fitness_level = st.selectbox(
            "Fitness Level",
            workout_recommender.get_difficulty_levels(),
            index=0 if user.get('fitness_level') is None
                  else list(workout_recommender.get_difficulty_levels()).index(
                      user.get('fitness_level', 'Beginner'))
        )
    
    available_time = st.slider("Available Time (minutes)", 
                              min_value=15, max_value=180,
                              value=user.get('available_time', 60))
    
    num_recommendations = st.slider("Number of Recommendations",
                                   min_value=3, max_value=12, value=5)
    
    if st.button("🔍 Get Workout Recommendations", use_container_width=True):
        recommendations = workout_recommender.recommend_workouts(
            goal=fitness_goal,
            difficulty_level=fitness_level,
            available_time=available_time,
            count=num_recommendations
        )
        
        if recommendations:
            st.subheader("Recommended Workouts")
            
            # Create dataframe for display
            df_display = pd.DataFrame([
                {
                    'Workout': workout['workout_name'],
                    'Type': workout['exercise_type'],
                    'Duration (min)': workout['duration_minutes'],
                    'Calories Burned': workout['calories_burned'],
                    'Equipment': workout['equipment']
                }
                for workout in recommendations
            ])
            
            st.dataframe(df_display, use_container_width=True)
            
            # Summary stats
            st.markdown("---")
            st.subheader("📊 Workout Summary")
            
            total_calories = sum(w['calories_burned'] for w in recommendations)
            total_time = sum(w['duration_minutes'] for w in recommendations)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Calories Burned", f"{int(total_calories)}")
            
            with col2:
                st.metric("Total Duration", f"{int(total_time)} min")
            
            with col3:
                st.metric("Avg Intensity", f"{int(total_calories/total_time)} cal/min")
        else:
            st.error("No recommendations found for selected criteria.")


# ==================== PAGE: WEEKLY PLAN ====================

def show_weekly_plan():
    """Display weekly fitness plan page."""
    
    st.markdown('<h1 class="main-header">📋 Weekly Fitness Plan</h1>', 
                unsafe_allow_html=True)
    
    st.write("Generate a complete weekly fitness and nutrition plan.")
    
    if not st.session_state.user_profile:
        st.warning("⚠️ Please set up your profile first.")
        return
    
    user = st.session_state.user_profile
    food_recommender, workout_recommender = init_recommenders()
    
    if st.button("📅 Generate Weekly Plan", use_container_width=True):
        with st.spinner("Creating your personalized weekly plan..."):
            
            # Generate workout plan
            days_per_week = user.get('days_per_week', 5)
            workout_plan = workout_recommender.calculate_weekly_plan(
                goal=user['fitness_goal'],
                difficulty_level=user['fitness_level'],
                days_per_week=days_per_week
            )
            
            # Generate food recommendations
            foods = food_recommender.recommend_foods(
                diet_type=user['diet_preference'],
                budget_level=user['budget_level'],
                target_calories=int(user.get('predicted_calories', 2000)),
                count=10
            )
            
            # Display plan
            st.subheader("🏃 Weekly Workout Schedule")
            
            for workout in workout_plan:
                with st.expander(f"Day {workout['day']}: {workout['workout_name']}", 
                                expanded=(workout['day'] == 1)):
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Duration", f"{workout['duration_minutes']} min")
                    with col2:
                        st.metric("Intensity", workout['difficulty_level'])
                    with col3:
                        st.metric("Calories Burned", f"{workout['calories_burned']}")
                    with col4:
                        st.metric("Equipment", workout['equipment'])
            
            st.markdown("---")
            
            # Daily nutrition summary
            st.subheader("🍽️ Recommended Daily Foods")
            
            df_foods = pd.DataFrame([
                {
                    'Food': food['food_name'],
                    'Calories': food['calories'],
                    'Protein (g)': round(food['protein'], 1),
                    'Carbs (g)': round(food['carbs'], 1),
                    'Fats (g)': round(food['fats'], 1)
                }
                for food in foods
            ])
            
            st.dataframe(df_foods, use_container_width=True)
            
            # Weekly summary
            st.markdown("---")
            st.subheader("📊 Weekly Summary")
            
            total_workout_calories = sum(w['calories_burned'] for w in workout_plan)
            total_food_calories = sum(f['calories'] for f in foods) * 7
            daily_avg_calories = user.get('predicted_calories', 2000)
            weekly_goal_calories = daily_avg_calories * 7
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Workout Calories", f"{int(total_workout_calories)}")
            
            with col2:
                st.metric("Weekly Goal", f"{int(weekly_goal_calories):,}")
            
            with col3:
                st.metric("Workout Days", days_per_week)
            
            with col4:
                st.metric("Rest Days", 7 - days_per_week)


# ==================== PAGE: AI TRAINER CHAT ====================

def show_ai_trainer():
    """Display AI trainer chatbot page."""
    
    st.markdown('<h1 class="main-header">🤖 AI Trainer Chat</h1>', 
                unsafe_allow_html=True)
    
    st.write("Chat with your AI fitness trainer for personalized advice and guidance.")
    
    if st.session_state.ai_trainer is None:
        st.warning("""
        ⚠️ **AI Trainer Not Configured**
        
        To use the AI trainer chatbot, please:
        1. Get your OpenAI API key from https://platform.openai.com/api-keys
        2. Enter it in the Settings section in the sidebar
        
        You can still ask common fitness questions, but personalized AI responses require API configuration.
        """)
        trainer = AITrainer()  # Use fallback trainer
    else:
        trainer = st.session_state.ai_trainer
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Display chat history
    if st.session_state.chat_history:
        st.subheader("💬 Conversation")
        
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                with st.chat_message("user"):
                    st.write(message['content'])
            else:
                with st.chat_message("assistant"):
                    st.write(message['content'])
    
    st.markdown("---")
    
    # User input
    col1, col2 = st.columns([0.9, 0.1])
    
    with col1:
        user_input = st.text_area(
            "Ask your question:",
            placeholder="e.g., How can I improve my running endurance? What should I eat before my workout?",
            height=80,
            key="user_input"
        )
    
    with col2:
        send_button = st.button("Send", use_container_width=True, key="send_button")
    
    if send_button and user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input
        })
        
        # Get AI response
        with st.spinner("AI Trainer is thinking..."):
            response = trainer.chat(
                user_input,
                user_context=st.session_state.user_profile if st.session_state.user_profile else None
            )
        
        # Add AI response to history
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': response
        })
        
        # Clear input and rerun
        st.rerun()
    
    # Quick suggestion buttons
    st.markdown("---")
    st.subheader("💡 Suggested Questions")
    
    suggestions = [
        "How can I lose weight effectively?",
        "What's the best workout for muscle gain?",
        "How should I structure my meals?",
        "What exercises should a beginner start with?",
        "How long until I see results?"
    ]
    
    cols = st.columns(len(suggestions))
    for col, suggestion in zip(cols, suggestions):
        with col:
            if st.button(suggestion, use_container_width=True):
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': suggestion
                })
                
                with st.spinner("AI Trainer is thinking..."):
                    response = trainer.chat(
                        suggestion,
                        user_context=st.session_state.user_profile if st.session_state.user_profile else None
                    )
                
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': response
                })
                
                st.rerun()
    
    # Clear chat button
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.chat_history = []
        if st.session_state.ai_trainer:
            st.session_state.ai_trainer.clear_history()
        st.rerun()


# ==================== RUN APPLICATION ====================

if __name__ == "__main__":
    main()
