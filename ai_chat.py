"""
AI Chat Module
==============
This module provides integration with OpenAI's API to create an AI fitness trainer chatbot.
It handles conversation history, context management, and personalized fitness advice.

Uses OpenAI Python SDK v1+ with the latest API standards.
"""

import os
from dotenv import load_dotenv
from typing import List, Dict, Optional
from pathlib import Path

# Load environment variables
load_dotenv()

# Import OpenAI with error handling
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class AITrainer:
    """
    AI Fitness Trainer using OpenAI API.
    
    This class manages conversations with OpenAI's GPT models to provide
    personalized fitness and nutrition advice.
    
    Features:
    - Conversation history with memory management (last 5 messages)
    - Secure API key handling via environment variables
    - Fallback responses when API is unavailable
    - User context personalization
    - Error handling and friendly error messages
    """
    
    # Model configuration
    MODEL = "gpt-4o-mini"
    MAX_HISTORY = 5  # Store only last 5 messages for memory management
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the AI Trainer.
        
        Args:
            api_key (str, optional): OpenAI API key. If not provided,
                                    will look for OPENAI_API_KEY environment variable
                                    
        Raises:
            ValueError: If OpenAI package is not installed and no API key provided
        """
        if not OPENAI_AVAILABLE:
            raise ImportError(
                "OpenAI package not installed. "
                "Install it with: pip install openai"
            )
        
        # Get API key from parameter or environment
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.conversation_history: List[Dict[str, str]] = []
        self.client = None
        self.api_available = False
        
        # Initialize OpenAI client
        if self.api_key:
            try:
                self.client = OpenAI(api_key=self.api_key)
                self.api_available = True
                self._validate_api_key()
            except Exception as e:
                self.api_available = False
        else:
            # API key is optional - will use fallback responses
            pass
        
        # System prompt for the AI trainer
        self.system_prompt = """
You are an expert AI fitness trainer and nutritionist with years of experience helping people 
achieve their fitness goals. You provide personalized advice based on the user's fitness level,
goals, and preferences. 

Your approach is:
- Encouraging and motivating
- Evidence-based and practical
- Adaptive to individual needs
- Safety-conscious (warn about potential injuries)

Always ask clarifying questions to better understand the user's needs.
Provide actionable, specific advice with examples when possible.
Keep responses concise but comprehensive (under 500 words).
"""
    
    def _validate_api_key(self) -> bool:
        """
        Validate if the OpenAI API key works by making a test call.
        
        Returns:
            bool: True if API key is valid and working
        """
        try:
            if not self.client:
                return False
            
            # Test with a minimal request
            response = self.client.chat.completions.create(
                model=self.MODEL,
                messages=[{"role": "user", "content": "ping"}],
                max_tokens=10
            )
            return True
        except Exception as e:
            self.api_available = False
            return False
    
    def _manage_history(self) -> None:
        """
        Manage conversation history to keep only the last MAX_HISTORY messages.
        This prevents context overflow and manages token usage.
        """
        if len(self.conversation_history) > self.MAX_HISTORY:
            # Keep only the most recent messages
            self.conversation_history = self.conversation_history[-self.MAX_HISTORY:]
    
    def chat(self, user_message: str, user_context: Optional[Dict] = None) -> str:
        """
        Send a message to the AI trainer and get a response.
        
        Args:
            user_message (str): The user's message/question
            user_context (dict, optional): User profile context for personalization
                                         (e.g., {'goal': 'weight_loss', 'level': 'beginner'})
        
        Returns:
            str: AI trainer's response
            
        Raises:
            ValueError: If user_message is empty
        """
        
        # Input validation
        if not user_message or not isinstance(user_message, str):
            raise ValueError("User message must be a non-empty string")
        
        user_message = user_message.strip()
        if not user_message:
            raise ValueError("User message cannot be empty")
        
        # Use fallback if API not available
        if not self.api_available:
            return self._get_fallback_response(user_message, user_context)
        
        try:
            # Prepare the enhanced message with context
            if user_context:
                context_str = self._format_context(user_context)
                enhanced_message = f"{context_str}\n\nUser Question: {user_message}"
            else:
                enhanced_message = user_message
            
            # Add user message to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": enhanced_message
            })
            
            # Manage history to prevent token overflow
            self._manage_history()
            
            # Create messages for API call (include system prompt and history)
            messages = [
                {"role": "system", "content": self.system_prompt}
            ] + self.conversation_history
            
            # Call OpenAI API with latest SDK syntax
            response = self.client.chat.completions.create(
                model=self.MODEL,
                messages=messages,
                temperature=0.7,
                max_tokens=500
            )
            
            # Extract response text
            ai_response = response.choices[0].message.content
            
            # Add assistant response to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": ai_response
            })
            
            # Manage history after adding response
            self._manage_history()
            
            return ai_response
            
        except Exception as e:
            # Provide friendly error message
            error_msg = str(e)
            if "401" in error_msg or "Unauthorized" in error_msg:
                return (
                    "❌ API Key Error: Your OpenAI API key is invalid or expired.\n\n"
                    "Please:\n"
                    "1. Check your API key at https://platform.openai.com/api-keys\n"
                    "2. Update your OPENAI_API_KEY environment variable\n"
                    "3. Restart the application"
                )
            elif "429" in error_msg or "rate" in error_msg.lower():
                return (
                    "⏳ Rate Limited: Too many requests to OpenAI API.\n\n"
                    "Please wait a moment and try again."
                )
            elif "model_not_found" in error_msg or "404" in error_msg:
                return (
                    f"⚠️ Model Error: {self.MODEL} not available in your account.\n\n"
                    "Please check your OpenAI subscription and available models."
                )
            else:
                return (
                    "❌ API Error: Could not reach OpenAI service.\n\n"
                    f"Details: {error_msg[:100]}\n\n"
                    "Falling back to general fitness advice..."
                )
    
    def _format_context(self, user_context: Dict) -> str:
        """
        Format user context into a readable string for the AI.
        
        Args:
            user_context (dict): User profile information
        
        Returns:
            str: Formatted context string
        """
        if not user_context:
            return ""
        
        context_parts = ["[User Context]"]
        
        # Add available context fields
        field_mapping = {
            'name': 'Name',
            'fitness_goal': 'Fitness Goal',
            'fitness_level': 'Fitness Level',
            'age': 'Age',
            'weight': 'Weight (kg)',
            'height': 'Height (cm)',
            'diet_preference': 'Diet Preference',
            'activity_level': 'Activity Level',
            'budget_level': 'Budget Level'
        }
        
        for key, label in field_mapping.items():
            if key in user_context and user_context[key]:
                context_parts.append(f"{label}: {user_context[key]}")
        
        return "\n".join(context_parts)
    
    def _get_fallback_response(self, user_message: str, 
                              user_context: Optional[Dict] = None) -> str:
        """
        Provide fallback responses when OpenAI API is not available.
        
        Args:
            user_message (str): The user's message
            user_context (dict, optional): User context
        
        Returns:
            str: A helpful response based on keywords
        """
        
        if not user_message:
            return (
                "Please ask me a question about fitness, nutrition, or workouts!\n\n"
                "Examples: How can I lose weight? What workouts should I do? "
                "How much protein do I need?"
            )
        
        message_lower = user_message.lower()
        
        # Weight loss responses
        if any(word in message_lower for word in ['weight loss', 'lose weight', 'lose fat', 'fat loss']):
            return """
**Weight Loss Strategy:**

1. **Calorie Deficit**: Create 300-500 cal/day deficit below maintenance
2. **Nutrition**:
   - Increase protein to 25-30% of calories (prevents muscle loss)
   - Eat whole foods: vegetables, lean proteins, whole grains
   - Reduce processed foods and added sugars
3. **Exercise**:
   - Cardio: 150+ minutes moderate or 75+ minutes vigorous per week
   - Strength: 2-3 sessions weekly (preserves muscle)
4. **Lifestyle**:
   - Sleep: 7-9 hours nightly
   - Water: 8+ glasses daily
   - Stress: Practice relaxation techniques

**Timeline**: 0.5-1 kg per week is sustainable

*For personalized advice, configure your OpenAI API key.*
"""
        
        # Muscle gain responses
        elif any(word in message_lower for word in ['muscle', 'gain', 'build muscle', 'bulk']):
            return """
**Muscle Gain Strategy:**

1. **Nutrition** (Calorie Surplus):
   - 200-300 cal/day above maintenance
   - Protein: 1.6-2.2g per kg of body weight
   - Carbs: 4-7g per kg (for energy)
   - Fats: 0.5-1.5g per kg
2. **Strength Training**:
   - Focus on compound movements: squats, deadlifts, bench press, rows
   - Progressive overload: increase weight/reps gradually
   - 3-4 sessions per week
   - 8-12 reps per set for hypertrophy
3. **Recovery**:
   - Sleep: 7-9 hours nightly
   - Rest days: 48 hours between same muscle groups
   - Foam rolling and stretching

**Timeline**: 0.25-0.5 kg per week is realistic

*For personalized advice, configure your OpenAI API key.*
"""
        
        # Workout responses
        elif any(word in message_lower for word in ['workout', 'exercise', 'training', 'routine']):
            return """
**General Workout Guidelines:**

**Beginners**:
- 3-4 days per week
- 30-45 minutes per session
- Mix cardio and strength training
- Focus on form over weight

**Intermediate**:
- 4-5 days per week
- 45-60 minutes per session
- Structured program (push/pull/legs)
- Progressive overload

**Advanced**:
- 5-6 days per week
- 60+ minutes per session
- Specialized training splits
- Periodization strategies

*For a personalized workout plan, configure your OpenAI API key.*
"""
        
        # Nutrition responses
        elif any(word in message_lower for word in ['nutrition', 'diet', 'food', 'eating', 'meal', 'macro']):
            return """
**Basic Nutrition Guide:**

**Macronutrients**:
- Protein: 1.2-2.0g per kg body weight
- Carbs: 3-5g per kg (varies by goal)
- Fats: 0.5-1.5g per kg

**Meal Timing**:
- Spread protein throughout day
- Pre-workout: carbs + protein (30-60 min before)
- Post-workout: protein + carbs (within 2 hours)

**Food Quality**:
- Lean proteins: chicken, fish, eggs
- Whole grains: oats, brown rice, quinoa
- Vegetables: all types, especially leafy greens
- Healthy fats: nuts, avocado, olive oil

*For a personalized meal plan, configure your OpenAI API key.*
"""
        
        # Default response
        else:
            return """
**AI Trainer Status**: Basic Mode (API Not Configured)

I can help with common fitness questions, but for personalized advice, 
please configure your OpenAI API key:

1. Get your API key: https://platform.openai.com/api-keys
2. Set environment variable: OPENAI_API_KEY=sk-...
3. Or configure in the app settings

**Topics I can help with**:
- Weight loss strategies
- Muscle building routines
- Workout programming
- Basic nutrition guidelines
- Fitness tips and motivation

Try asking: "How can I lose weight?" or "What exercises should I do?"

*For full AI capabilities, add your OpenAI API key.*
"""
    
    def get_personalized_plan(self, user_context: Dict) -> str:
        """
        Generate a personalized fitness plan based on user context.
        
        Args:
            user_context (dict): User profile information
        
        Returns:
            str: Personalized fitness plan
            
        Raises:
            ValueError: If user_context is invalid or API is not available
        """
        
        if not user_context:
            raise ValueError("User context is required for personalized plan")
        
        if not self.api_available:
            return (
                "❌ Cannot generate personalized plan without OpenAI API.\n\n"
                "Please configure your API key to get personalized fitness plans."
            )
        
        plan_prompt = f"""
Based on the following user profile, create a comprehensive 4-week fitness plan:

{self._format_context(user_context)}

Include:
1. Weekly workout schedule (specific exercises with sets/reps)
2. Daily meal plan outline (meal structure, not detailed recipes)
3. Nutrition guidelines specific to their goal
4. Recovery and rest recommendations
5. Progress tracking metrics
6. Potential challenges and how to overcome them

Make it practical and actionable.
"""
        
        return self.chat(plan_prompt, user_context)
    
    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history = []
    
    def get_history(self) -> List[Dict[str, str]]:
        """
        Get a copy of the conversation history.
        
        Returns:
            list: List of conversation messages
        """
        return self.conversation_history.copy()
    
    def get_history_length(self) -> int:
        """
        Get the current number of messages in history.
        
        Returns:
            int: Number of messages
        """
        return len(self.conversation_history)


def validate_api_key(api_key: str) -> bool:
    """
    Validate if the OpenAI API key format is correct.
    
    Args:
        api_key (str): The API key to validate
    
    Returns:
        bool: True if API key format is valid
    """
    
    if not api_key or not isinstance(api_key, str):
        return False
    
    # OpenAI API keys start with 'sk-'
    if not api_key.startswith('sk-'):
        return False
    
    # Minimum reasonable length
    if len(api_key) < 40:
        return False
    
    return True


# ==================== TEST/DEMO FUNCTIONALITY ====================

def test_ai_trainer():
    """
    Test function to verify AITrainer works correctly.
    Can be run as: python ai_chat.py
    """
    
    print("=" * 60)
    print("AI Fitness Trainer - Test Mode")
    print("=" * 60)
    
    # Test 1: Initialize without API key
    print("\n[Test 1] Initializing AITrainer without API key...")
    try:
        trainer = AITrainer()
        print("✓ AITrainer initialized (API not available - fallback mode)")
    except Exception as e:
        print(f"✗ Failed to initialize: {e}")
        return
    
    # Test 2: Fallback responses
    print("\n[Test 2] Testing fallback responses...")
    test_queries = [
        "How can I lose weight?",
        "How do I build muscle?",
        "What exercises should I do?",
        "Tell me about nutrition"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        try:
            response = trainer.chat(query)
            print(f"Response: {response[:100]}...")
        except Exception as e:
            print(f"✗ Error: {e}")
    
    # Test 3: Empty input handling
    print("\n[Test 3] Testing empty input handling...")
    try:
        trainer.chat("")
        print("✗ Should have raised ValueError for empty input")
    except ValueError as e:
        print(f"✓ Correctly raised ValueError: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
    
    # Test 4: Conversation history management
    print("\n[Test 4] Testing conversation history management...")
    trainer.clear_history()
    for i in range(10):
        try:
            trainer.chat(f"Test message {i}")
        except Exception:
            pass
    
    history_length = trainer.get_history_length()
    if history_length <= trainer.MAX_HISTORY * 2:
        print(f"✓ History managed correctly: {history_length} messages")
    else:
        print(f"✗ History not managed: {history_length} messages (max: {trainer.MAX_HISTORY * 2})")
    
    # Test 5: Context formatting
    print("\n[Test 5] Testing context formatting...")
    sample_context = {
        'name': 'John',
        'age': 30,
        'weight': 80,
        'fitness_goal': 'WeightLoss',
        'fitness_level': 'Beginner'
    }
    
    try:
        formatted = trainer._format_context(sample_context)
        if 'John' in formatted and 'WeightLoss' in formatted:
            print(f"✓ Context formatted correctly")
            print(f"  Output: {formatted[:50]}...")
        else:
            print(f"✗ Context not formatted correctly")
    except Exception as e:
        print(f"✗ Error formatting context: {e}")
    
    # Test 6: API key validation
    print("\n[Test 6] Testing API key validation...")
    test_keys = [
        ("sk-proj-valid1234567890validkey123456789", True),
        ("invalid-key", False),
        ("sk-short", False),
        ("", False),
    ]
    
    for key, expected in test_keys:
        result = validate_api_key(key)
        status = "✓" if result == expected else "✗"
        print(f"{status} Key '{key[:20]}...': {result} (expected: {expected})")
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)


if __name__ == "__main__":
    test_ai_trainer()
