"""
Recommender System
==================
This module provides recommendation functionality for foods and workouts.
It uses content-based filtering to recommend items based on user preferences,
diet type, budget, fitness goals, and fitness level.
"""

import pandas as pd
from pathlib import Path
from typing import List, Dict, Any


class FoodRecommender:
    """
    Recommends foods based on user preferences, diet type, and budget.
    
    Attributes:
        foods_df (pd.DataFrame): DataFrame containing food information
    """
    
    def __init__(self):
        """Initialize the food recommender with food data."""
        data_dir = Path(__file__).parent / 'data'
        self.foods_df = pd.read_csv(data_dir / 'foods.csv')
    
    def recommend_foods(self, 
                       diet_type: str, 
                       budget_level: str,
                       target_calories: int,
                       count: int = 5) -> List[Dict[str, Any]]:
        """
        Recommend foods based on diet type and budget level.
        
        Args:
            diet_type (str): Type of diet ('Balanced', 'Vegan', 'HighProtein')
            budget_level (str): Budget level ('Low', 'Medium', 'High')
            target_calories (int): Target calorie intake for recommendation
            count (int): Number of recommendations to return (default: 5)
        
        Returns:
            list: List of recommended foods as dictionaries
        """
        
        # Filter foods by diet type and budget level
        filtered_foods = self.foods_df[
            (self.foods_df['diet_type'] == diet_type) &
            (self.foods_df['budget_level'] == budget_level)
        ]
        
        if filtered_foods.empty:
            # Fallback: return foods by diet type only if budget filter yields nothing
            filtered_foods = self.foods_df[
                self.foods_df['diet_type'] == diet_type
            ]
        
        # Sort by calorie proximity to target for balanced nutrition
        filtered_foods['calorie_diff'] = abs(
            filtered_foods['calories'] - (target_calories / 5)  # Assuming 5 meals per day
        )
        
        # Get top recommendations sorted by calorie difference
        recommendations = filtered_foods.nsmallest(count, 'calorie_diff')
        
        return [
            {
                'food_id': row['food_id'],
                'food_name': row['food_name'],
                'calories': row['calories'],
                'protein': row['protein'],
                'carbs': row['carbs'],
                'fats': row['fats'],
                'category': row['category']
            }
            for _, row in recommendations.iterrows()
        ]
    
    def get_all_diet_types(self) -> List[str]:
        """
        Get all available diet types.
        
        Returns:
            list: List of unique diet types
        """
        return self.foods_df['diet_type'].unique().tolist()
    
    def get_budget_levels(self) -> List[str]:
        """
        Get all available budget levels.
        
        Returns:
            list: List of unique budget levels
        """
        return self.foods_df['budget_level'].unique().tolist()


class WorkoutRecommender:
    """
    Recommends workouts based on fitness goals and difficulty level.
    
    Attributes:
        workouts_df (pd.DataFrame): DataFrame containing workout information
    """
    
    def __init__(self):
        """Initialize the workout recommender with workout data."""
        data_dir = Path(__file__).parent / 'data'
        self.workouts_df = pd.read_csv(data_dir / 'workouts.csv')
    
    def recommend_workouts(self,
                          goal: str,
                          difficulty_level: str,
                          available_time: int = 60,
                          count: int = 5) -> List[Dict[str, Any]]:
        """
        Recommend workouts based on fitness goal and difficulty level.
        
        Args:
            goal (str): Fitness goal ('WeightLoss', 'MuscleGain', 'Flexibility', 'Toning', 'Recovery')
            difficulty_level (str): Difficulty level ('Beginner', 'Intermediate', 'Advanced')
            available_time (int): Available time in minutes for workout (default: 60)
            count (int): Number of recommendations to return (default: 5)
        
        Returns:
            list: List of recommended workouts as dictionaries
        """
        
        # Filter workouts by goal and difficulty level
        filtered_workouts = self.workouts_df[
            (self.workouts_df['goal'] == goal) &
            (self.workouts_df['difficulty_level'] == difficulty_level)
        ]
        
        if filtered_workouts.empty:
            # Fallback: return workouts by goal only
            filtered_workouts = self.workouts_df[
                self.workouts_df['goal'] == goal
            ]
        
        # Filter by available time (workouts that fit within available time)
        time_filtered = filtered_workouts[
            filtered_workouts['duration_minutes'] <= available_time
        ]
        
        if time_filtered.empty:
            time_filtered = filtered_workouts
        
        # Sort by calories burned (descending) for efficiency
        recommendations = time_filtered.nlargest(count, 'calories_burned')
        
        return [
            {
                'workout_id': row['workout_id'],
                'workout_name': row['workout_name'],
                'exercise_type': row['exercise_type'],
                'difficulty_level': row['difficulty_level'],
                'calories_burned': row['calories_burned'],
                'duration_minutes': row['duration_minutes'],
                'equipment': row['equipment']
            }
            for _, row in recommendations.iterrows()
        ]
    
    def get_all_goals(self) -> List[str]:
        """
        Get all available fitness goals.
        
        Returns:
            list: List of unique fitness goals
        """
        return self.workouts_df['goal'].unique().tolist()
    
    def get_difficulty_levels(self) -> List[str]:
        """
        Get all available difficulty levels.
        
        Returns:
            list: List of unique difficulty levels
        """
        return self.workouts_df['difficulty_level'].unique().tolist()
    
    def calculate_weekly_plan(self,
                             goal: str,
                             difficulty_level: str,
                             days_per_week: int = 5) -> List[Dict[str, Any]]:
        """
        Generate a weekly workout plan based on goal and available days.
        
        Args:
            goal (str): Fitness goal
            difficulty_level (str): Difficulty level
            days_per_week (int): Number of workout days per week (default: 5)
        
        Returns:
            list: List of workouts for weekly plan
        """
        
        plan = []
        total_workouts = min(days_per_week, len(self.workouts_df))
        
        for day in range(total_workouts):
            workouts = self.recommend_workouts(goal, difficulty_level, count=1)
            if workouts:
                workout = workouts[0].copy()
                workout['day'] = day + 1
                plan.append(workout)
        
        return plan


def get_nutritional_summary(foods: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Calculate nutritional summary from a list of foods.
    
    Args:
        foods (list): List of food dictionaries with nutrition info
    
    Returns:
        dict: Summary of total nutrients
    """
    
    summary = {
        'total_calories': 0,
        'total_protein': 0,
        'total_carbs': 0,
        'total_fats': 0
    }
    
    for food in foods:
        summary['total_calories'] += food.get('calories', 0)
        summary['total_protein'] += food.get('protein', 0)
        summary['total_carbs'] += food.get('carbs', 0)
        summary['total_fats'] += food.get('fats', 0)
    
    return summary
