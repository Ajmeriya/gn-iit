"""
Assessment/Quiz Generator - Model-2B
Generates MCQs, Subjective (SQL), and Coding (DSA) questions using Gemini API

Standalone module - ready for backend integration
"""

import json
import os
from typing import Dict, List, Optional, Tuple
import google.generativeai as genai

# Import DSA Engine
try:
    from .dsa_engine import generate_dsa_test_cases, get_pattern_blueprint
    DSA_ENGINE_AVAILABLE = True
except ImportError:
    DSA_ENGINE_AVAILABLE = False


# ============================================================================
# DIFFICULTY RANGE LOGIC (Backend Enforced)
# ============================================================================

DIFFICULTY_RANGE = {
    "Easy": ["Low"],
    "Medium": ["Low", "Medium"],
    "Hard": ["Low", "Medium", "High"]
}

# Experience level mapping for question depth
EXPERIENCE_DEPTH = {
    "Junior": {
        "focus": "fundamentals, basic usage, syntax",
        "avoid": "optimization, edge cases, trade-offs"
    },
    "Mid": {
        "focus": "practical usage, common pitfalls, real-world scenarios",
        "avoid": "advanced optimization, complex edge cases"
    },
    "Senior": {
        "focus": "optimization, edge cases, trade-offs, system design",
        "avoid": None  # No restrictions
    }
}


# ============================================================================
# GEMINI API CONFIGURATION
# ============================================================================

def configure_gemini(api_key: Optional[str] = None) -> None:
    """
    Configure Gemini API with API key.
    
    Args:
        api_key: Gemini API key. If None, reads from GEMINI_API_KEY environment variable.
        
    Raises:
        ValueError: If API key is not provided and not found in environment.
    """
    if api_key is None:
        api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError(
            "Gemini API key not found. "
            "Set GEMINI_API_KEY environment variable or pass api_key parameter."
        )
    
    genai.configure(api_key=api_key)


def get_available_model() -> Tuple[str, genai.GenerativeModel]:
    """
    Detect and return available model (Gemini or PaLM fallback).
    
    Returns:
        Tuple of (model_name, model_instance)
        
    Raises:
        RuntimeError: If no suitable model is available
    """
    try:
        # Try Gemini first (prioritize latest/stable versions)
        models = list(genai.list_models())
        
        # Priority order: flash/pro-latest > flash > pro > others
        gemini_models = [
            m.name for m in models 
            if "gemini" in m.name.lower() and "generateContent" in m.supported_generation_methods
        ]
        
        # Prefer flash or pro-latest versions
        preferred_models = [
            m for m in gemini_models 
            if any(x in m.lower() for x in ["flash-latest", "pro-latest", "2.5-flash", "2.5-pro"])
        ]
        
        if preferred_models:
            model_name = preferred_models[0]  # Use preferred Gemini model
        elif gemini_models:
            model_name = gemini_models[0]  # Use first available Gemini
        else:
            model_name = None
        
        if model_name:
            return model_name, genai.GenerativeModel(model_name)
        
        # Fallback to PaLM
        palm_models = [
            m.name for m in models 
            if "bison" in m.name.lower() and "generateContent" in m.supported_generation_methods
        ]
        
        if palm_models:
            model_name = palm_models[0]  # Use first available PaLM
            return model_name, genai.GenerativeModel(model_name)
        
        # Last resort: any model with generateContent
        content_models = [
            m.name for m in models 
            if "generateContent" in m.supported_generation_methods
        ]
        
        if content_models:
            model_name = content_models[0]
            return model_name, genai.GenerativeModel(model_name)
        
        raise RuntimeError("No suitable model found with generateContent method")
        
    except Exception as e:
        raise RuntimeError(f"Failed to get available model: {str(e)}")


def get_gemini_model(model_name: Optional[str] = None) -> genai.GenerativeModel:
    """
    Get model instance (auto-detects if model_name not provided).
    
    Args:
        model_name: Model name (e.g., "models/gemini-pro" or "models/text-bison-001")
                   If None, auto-detects available model
        
    Returns:
        Configured model instance
    """
    if model_name:
        return genai.GenerativeModel(model_name)
    else:
        _, model = get_available_model()
        return model


# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_difficulty_range(selected_difficulty: str, question_difficulty: str) -> bool:
    """
    Validate that question difficulty is within allowed range.
    
    Args:
        selected_difficulty: Recruiter-selected difficulty ("Easy", "Medium", "Hard")
        question_difficulty: Question difficulty ("Low", "Medium", "High")
        
    Returns:
        True if question difficulty is allowed, False otherwise
    """
    allowed_difficulties = DIFFICULTY_RANGE.get(selected_difficulty, [])
    return question_difficulty in allowed_difficulties


def validate_time_constraint(questions: List[Dict], total_time: int) -> bool:
    """
    Validate that sum of estimated times <= total time.
    
    Args:
        questions: List of questions with estimated_time field
        total_time: Total time allowed for section (minutes)
        
    Returns:
        True if time constraint is satisfied, False otherwise
    """
    total_estimated = sum(q.get("estimated_time", 0) for q in questions)
    return total_estimated <= total_time


# ============================================================================
# PROMPT GENERATION
# ============================================================================

def generate_mcq_prompt(
    question_count: int,
    total_time: int,
    difficulty: str,
    experience_level: str,
    experience_years: int
) -> str:
    """
    Generate prompt for MCQ questions.
    
    Args:
        question_count: Number of MCQs to generate
        total_time: Total time for MCQ section (minutes)
        difficulty: Selected difficulty ("Easy", "Medium", "Hard")
        experience_level: Experience level ("Junior", "Mid", "Senior")
        experience_years: Years of experience
        
    Returns:
        Formatted prompt string
    """
    allowed_difficulties = DIFFICULTY_RANGE[difficulty]
    depth_info = EXPERIENCE_DEPTH[experience_level]
    
    prompt = f"""Generate exactly {question_count} Multiple Choice Questions (MCQs) for a technical assessment.

REQUIREMENTS:
1. Total time for all questions: {total_time} minutes
2. Each question must include estimated_time (in minutes)
3. Sum of all estimated_time must be <= {total_time} minutes
4. Difficulty levels allowed: {', '.join(allowed_difficulties)}
5. Experience level: {experience_level} ({experience_years} years)
6. Focus: {depth_info['focus']}
"""
    if depth_info['avoid']:
        prompt += f"7. Avoid: {depth_info['avoid']}\n"
    
    prompt += """
OUTPUT FORMAT (JSON only, no markdown):
{
  "questions": [
    {
      "question": "What is the time complexity of binary search?",
      "options": ["O(n)", "O(log n)", "O(n log n)", "O(1)"],
      "correct_answer": "O(log n)",
      "difficulty": "Low",
      "estimated_time": 1
    }
  ]
}

IMPORTANT:
- Generate exactly the specified number of questions
- Ensure sum of estimated_time <= total_time
- Use only allowed difficulty levels
- Questions must match experience level depth
- Return ONLY valid JSON, no explanations
"""
    return prompt


def generate_subjective_prompt(
    question_count: int,
    total_time: int,
    topic: str,
    difficulty: str,
    experience_level: str,
    experience_years: int
) -> str:
    """
    Generate prompt for Subjective (SQL) questions.
    
    Args:
        question_count: Number of subjective questions to generate
        total_time: Total time for subjective section (minutes)
        topic: Topic (e.g., "SQL")
        difficulty: Selected difficulty ("Easy", "Medium", "Hard")
        experience_level: Experience level ("Junior", "Mid", "Senior")
        experience_years: Years of experience
        
    Returns:
        Formatted prompt string
    """
    allowed_difficulties = DIFFICULTY_RANGE[difficulty]
    depth_info = EXPERIENCE_DEPTH[experience_level]
    
    prompt = f"""Generate exactly {question_count} Subjective Questions for {topic} assessment.

REQUIREMENTS:
1. Total time for all questions: {total_time} minutes
2. Each question must include estimated_time (in minutes)
3. Sum of all estimated_time must be <= {total_time} minutes
4. Difficulty levels allowed: {', '.join(allowed_difficulties)}
5. Experience level: {experience_level} ({experience_years} years)
6. Focus: {depth_info['focus']}
"""
    if depth_info['avoid']:
        prompt += f"7. Avoid: {depth_info['avoid']}\n"
    
    prompt += f"""
OUTPUT FORMAT (JSON only, no markdown):
{{
  "questions": [
    {{
      "question": "Write a SQL query to find the second highest salary from employees table.",
      "difficulty": "Medium",
      "estimated_time": 3
    }}
  ]
}}

IMPORTANT:
- Generate exactly the specified number of questions
- Ensure sum of estimated_time <= total_time
- Use only allowed difficulty levels
- Questions must match experience level depth
- Return ONLY valid JSON, no explanations
"""
    return prompt


def generate_coding_prompt(
    question_count: int,
    total_time: int,
    topic: str,
    difficulty: str,
    experience_level: str,
    experience_years: int
) -> str:
    """
    Generate prompt for Coding (DSA) questions.
    
    Args:
        question_count: Number of coding questions to generate
        total_time: Total time for coding section (minutes)
        topic: Topic (e.g., "DSA")
        difficulty: Selected difficulty ("Easy", "Medium", "Hard")
        experience_level: Experience level ("Junior", "Mid", "Senior")
        experience_years: Years of experience
        
    Returns:
        Formatted prompt string
    """
    allowed_difficulties = DIFFICULTY_RANGE[difficulty]
    depth_info = EXPERIENCE_DEPTH[experience_level]
    
    prompt = f"""Generate exactly {question_count} Coding Problems for {topic} assessment.

REQUIREMENTS:
1. Total time for all problems: {total_time} minutes
2. Each problem must include estimated_time (in minutes)
3. Sum of all estimated_time must be <= {total_time} minutes
4. Difficulty levels allowed: {', '.join(allowed_difficulties)}
5. Experience level: {experience_level} ({experience_years} years)
6. Focus: {depth_info['focus']}
"""
    if depth_info['avoid']:
        prompt += f"7. Avoid: {depth_info['avoid']}\n"
    
    prompt += f"""
OUTPUT FORMAT (JSON only, no markdown):
{{
  "problems": [
    {{
      "problem": "Given an array of integers, find two numbers that add up to a target value. Return their indices.",
      "pattern": "Array + Hashing",
      "problem_type": "two_sum",
      "difficulty": "Medium",
      "estimated_time": 60
    }}
  ]
}}

AVAILABLE PATTERNS (use one per problem):
- "Array + Hashing" (problem_type: "two_sum", "contains_duplicate", "group_anagrams", "longest_consecutive")
- "Two Pointers" (problem_type: "valid_palindrome", "two_sum_sorted", "container_water", "three_sum")
- "Sliding Window" (problem_type: "longest_substring", "min_window", "max_average", "length_of_longest_substring")
- "Stack" (problem_type: "valid_parentheses", "daily_temperatures", "next_greater", "largest_rectangle")
- "Binary Search" (problem_type: "search_rotated", "find_peak", "search_range", "search_insert")
- "Recursion / Backtracking" (problem_type: "generate_parentheses", "combination_sum", "subsets", "permutations")
- "Linked List" (problem_type: "reverse_list", "merge_lists", "has_cycle", "remove_nth")
- "Tree Traversal" (problem_type: "max_depth", "same_tree", "level_order", "path_sum")

IMPORTANT:
- Generate exactly the specified number of problems
- Ensure sum of estimated_time <= total_time
- Use only allowed difficulty levels
- Problems must match experience level depth
- Return ONLY valid JSON, no explanations
"""
    return prompt


# ============================================================================
# QUESTION GENERATION
# ============================================================================

def generate_mcq_questions(
    config: Dict,
    model: genai.GenerativeModel,
    api_key: Optional[str] = None
) -> List[Dict]:
    """
    Generate MCQ questions using Gemini API.
    
    Args:
        config: Assessment configuration dictionary
        model: Gemini model instance
        api_key: Optional API key (if not configured globally)
        
    Returns:
        List of MCQ question dictionaries
    """
    if api_key:
        configure_gemini(api_key)
    
    mcq_config = config["sections"]["mcq"]
    prompt = generate_mcq_prompt(
        question_count=mcq_config["question_count"],
        total_time=mcq_config["total_time_minutes"],
        difficulty=config["difficulty"],
        experience_level=config["experience_level"],
        experience_years=config["experience_years"]
    )
    
    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        result = json.loads(response_text)
        questions = result.get("questions", [])
        
        # Validate difficulty range
        allowed_difficulties = DIFFICULTY_RANGE[config["difficulty"]]
        validated_questions = []
        for q in questions:
            if q.get("difficulty") in allowed_difficulties:
                validated_questions.append(q)
            else:
                # Regenerate if difficulty doesn't match
                continue
        
        # Validate time constraint
        if not validate_time_constraint(validated_questions, mcq_config["total_time_minutes"]):
            # If time exceeded, adjust estimated_time proportionally
            total_estimated = sum(q.get("estimated_time", 0) for q in validated_questions)
            if total_estimated > 0:
                scale_factor = mcq_config["total_time_minutes"] / total_estimated
                for q in validated_questions:
                    q["estimated_time"] = max(1, int(q.get("estimated_time", 1) * scale_factor))
        
        # Ensure exact count
        while len(validated_questions) < mcq_config["question_count"]:
            # Generate additional questions if needed
            additional_prompt = generate_mcq_prompt(
                question_count=1,
                total_time=1,
                difficulty=config["difficulty"],
                experience_level=config["experience_level"],
                experience_years=config["experience_years"]
            )
            additional_response = model.generate_content(additional_prompt)
            additional_text = additional_response.text.strip()
            if additional_text.startswith("```json"):
                additional_text = additional_text[7:]
            if additional_text.startswith("```"):
                additional_text = additional_text[3:]
            if additional_text.endswith("```"):
                additional_text = additional_text[:-3]
            additional_text = additional_text.strip()
            
            try:
                additional_result = json.loads(additional_text)
                additional_questions = additional_result.get("questions", [])
                for q in additional_questions:
                    if q.get("difficulty") in allowed_difficulties:
                        validated_questions.append(q)
                        if len(validated_questions) >= mcq_config["question_count"]:
                            break
            except:
                pass
        
        return validated_questions[:mcq_config["question_count"]]
        
    except Exception as e:
        raise RuntimeError(f"Failed to generate MCQ questions: {str(e)}")


def generate_subjective_questions(
    config: Dict,
    model: genai.GenerativeModel,
    api_key: Optional[str] = None
) -> List[Dict]:
    """
    Generate Subjective (SQL) questions using Gemini API.
    
    Args:
        config: Assessment configuration dictionary
        model: Gemini model instance
        api_key: Optional API key (if not configured globally)
        
    Returns:
        List of subjective question dictionaries
    """
    if api_key:
        configure_gemini(api_key)
    
    subjective_config = config["sections"]["subjective"]
    prompt = generate_subjective_prompt(
        question_count=subjective_config["question_count"],
        total_time=subjective_config["total_time_minutes"],
        topic=subjective_config.get("topic", "SQL"),
        difficulty=config["difficulty"],
        experience_level=config["experience_level"],
        experience_years=config["experience_years"]
    )
    
    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        result = json.loads(response_text)
        questions = result.get("questions", [])
        
        # Validate difficulty range
        allowed_difficulties = DIFFICULTY_RANGE[config["difficulty"]]
        validated_questions = []
        for q in questions:
            if q.get("difficulty") in allowed_difficulties:
                validated_questions.append(q)
        
        # Validate time constraint
        if not validate_time_constraint(validated_questions, subjective_config["total_time_minutes"]):
            total_estimated = sum(q.get("estimated_time", 0) for q in validated_questions)
            if total_estimated > 0:
                scale_factor = subjective_config["total_time_minutes"] / total_estimated
                for q in validated_questions:
                    q["estimated_time"] = max(1, int(q.get("estimated_time", 1) * scale_factor))
        
        # Ensure exact count
        while len(validated_questions) < subjective_config["question_count"]:
            additional_prompt = generate_subjective_prompt(
                question_count=1,
                total_time=1,
                topic=subjective_config.get("topic", "SQL"),
                difficulty=config["difficulty"],
                experience_level=config["experience_level"],
                experience_years=config["experience_years"]
            )
            additional_response = model.generate_content(additional_prompt)
            additional_text = additional_response.text.strip()
            if additional_text.startswith("```json"):
                additional_text = additional_text[7:]
            if additional_text.startswith("```"):
                additional_text = additional_text[3:]
            if additional_text.endswith("```"):
                additional_text = additional_text[:-3]
            additional_text = additional_text.strip()
            
            try:
                additional_result = json.loads(additional_text)
                additional_questions = additional_result.get("questions", [])
                for q in additional_questions:
                    if q.get("difficulty") in allowed_difficulties:
                        validated_questions.append(q)
                        if len(validated_questions) >= subjective_config["question_count"]:
                            break
            except:
                pass
        
        return validated_questions[:subjective_config["question_count"]]
        
    except Exception as e:
        raise RuntimeError(f"Failed to generate subjective questions: {str(e)}")


def generate_coding_questions(
    config: Dict,
    model: genai.GenerativeModel,
    api_key: Optional[str] = None
) -> List[Dict]:
    """
    Generate Coding (DSA) questions using Gemini API.
    
    Args:
        config: Assessment configuration dictionary
        model: Gemini model instance
        api_key: Optional API key (if not configured globally)
        
    Returns:
        List of coding problem dictionaries
    """
    if api_key:
        configure_gemini(api_key)
    
    coding_config = config["sections"]["coding"]
    prompt = generate_coding_prompt(
        question_count=coding_config["question_count"],
        total_time=coding_config["total_time_minutes"],
        topic=coding_config.get("topic", "DSA"),
        difficulty=config["difficulty"],
        experience_level=config["experience_level"],
        experience_years=config["experience_years"]
    )
    
    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        response_text = response_text.strip()
        
        result = json.loads(response_text)
        problems = result.get("problems", result.get("questions", []))
        
        # Validate difficulty range
        allowed_difficulties = DIFFICULTY_RANGE[config["difficulty"]]
        validated_problems = []
        for p in problems:
            if p.get("difficulty") in allowed_difficulties:
                validated_problems.append(p)
        
        # Validate time constraint
        if not validate_time_constraint(validated_problems, coding_config["total_time_minutes"]):
            total_estimated = sum(p.get("estimated_time", 0) for p in validated_problems)
            if total_estimated > 0:
                scale_factor = coding_config["total_time_minutes"] / total_estimated
                for p in validated_problems:
                    p["estimated_time"] = max(1, int(p.get("estimated_time", 1) * scale_factor))
        
        # Integrate DSA Engine for test case generation
        if DSA_ENGINE_AVAILABLE:
            for problem in validated_problems:
                try:
                    # Extract pattern and problem type from problem
                    pattern = problem.get("pattern", "Array + Hashing")
                    problem_type = problem.get("problem_type", "two_sum")
                    problem_statement = problem.get("problem", problem.get("description", ""))
                    
                    if problem_statement and pattern and problem_type:
                        # Generate validated test cases using DSA engine
                        test_cases = generate_dsa_test_cases(
                            pattern_name=pattern,
                            problem_statement=problem_statement,
                            problem_type=problem_type,
                            api_key=api_key,
                            model_name=model.name if hasattr(model, 'name') else None
                        )
                        
                        # Attach test cases to problem
                        problem["public_tests"] = test_cases.get("public_tests", [])
                        problem["hidden_tests"] = test_cases.get("hidden_tests", [])
                except Exception as e:
                    # If DSA engine fails, continue without test cases
                    print(f"Warning: Could not generate test cases for problem: {str(e)}")
        
        # Ensure exact count
        while len(validated_problems) < coding_config["question_count"]:
            additional_prompt = generate_coding_prompt(
                question_count=1,
                total_time=1,
                topic=coding_config.get("topic", "DSA"),
                difficulty=config["difficulty"],
                experience_level=config["experience_level"],
                experience_years=config["experience_years"]
            )
            additional_response = model.generate_content(additional_prompt)
            additional_text = additional_response.text.strip()
            if additional_text.startswith("```json"):
                additional_text = additional_text[7:]
            if additional_text.startswith("```"):
                additional_text = additional_text[3:]
            if additional_text.endswith("```"):
                additional_text = additional_text[:-3]
            additional_text = additional_text.strip()
            
            try:
                additional_result = json.loads(additional_text)
                additional_problems = additional_result.get("problems", [])
                for p in additional_problems:
                    if p.get("difficulty") in allowed_difficulties:
                        validated_problems.append(p)
                        if len(validated_problems) >= coding_config["question_count"]:
                            break
            except:
                pass
        
        return validated_problems[:coding_config["question_count"]]
        
    except Exception as e:
        raise RuntimeError(f"Failed to generate coding questions: {str(e)}")


# ============================================================================
# MAIN GENERATION FUNCTION
# ============================================================================

def generate_assessment(
    config: Dict,
    api_key: Optional[str] = None,
    model_name: Optional[str] = None
) -> Dict:
    """
    Main function: Generate complete assessment with all sections.
    
    This function generates MCQs, Subjective (SQL), and Coding (DSA) questions
    based on recruiter-defined configuration.
    
    Args:
        config: Assessment configuration dictionary with structure:
            {
                "experience_years": int,
                "experience_level": str,  # "Junior", "Mid", "Senior"
                "difficulty": str,  # "Easy", "Medium", "Hard"
                "sections": {
                    "mcq": {
                        "total_time_minutes": int,
                        "question_count": int
                    },
                    "subjective": {
                        "topic": str,  # e.g., "SQL"
                        "total_time_minutes": int,
                        "question_count": int
                    },
                    "coding": {
                        "topic": str,  # e.g., "DSA"
                        "total_time_minutes": int,
                        "question_count": int
                    }
                }
            }
        api_key: Google AI API key (optional, can use GEMINI_API_KEY env var)
        model_name: Model name (e.g., "models/gemini-pro" or "models/text-bison-001")
                    If None, auto-detects available model
        
    Returns:
        Dictionary with generated questions in strict JSON format:
        {
            "mcq": [
                {
                    "question": str,
                    "options": [str, str, str, str],
                    "correct_answer": str,
                    "difficulty": str,  # "Low", "Medium", "High"
                    "estimated_time": int  # minutes
                }
            ],
            "subjective": [
                {
                    "question": str,
                    "difficulty": str,
                    "estimated_time": int
                }
            ],
            "coding": [
                {
                    "problem": str,
                    "difficulty": str,
                    "estimated_time": int
                }
            ]
        }
        
    Raises:
        ValueError: If configuration is invalid
        RuntimeError: If question generation fails
        
    Example:
        config = {
            "experience_years": 2,
            "experience_level": "Mid",
            "difficulty": "Medium",
            "sections": {
                "mcq": {"total_time_minutes": 20, "question_count": 15},
                "subjective": {"topic": "SQL", "total_time_minutes": 30, "question_count": 10},
                "coding": {"topic": "DSA", "total_time_minutes": 120, "question_count": 2}
            }
        }
        result = generate_assessment(config, api_key="your-api-key")
    """
    # Validate configuration
    if not isinstance(config, dict):
        raise ValueError("config must be a dictionary")
    
    required_fields = ["experience_years", "experience_level", "difficulty", "sections"]
    for field in required_fields:
        if field not in config:
            raise ValueError(f"Missing required field: {field}")
    
    if config["experience_level"] not in EXPERIENCE_DEPTH:
        raise ValueError(f"Invalid experience_level: {config['experience_level']}")
    
    if config["difficulty"] not in DIFFICULTY_RANGE:
        raise ValueError(f"Invalid difficulty: {config['difficulty']}")
    
    required_sections = ["mcq", "subjective", "coding"]
    for section in required_sections:
        if section not in config["sections"]:
            raise ValueError(f"Missing required section: {section}")
    
    # Configure API
    configure_gemini(api_key)
    
    # Get model (auto-detect if not specified)
    if model_name:
        model = genai.GenerativeModel(model_name)
    else:
        detected_name, model = get_available_model()
        # Model auto-detected and ready to use
    
    # Generate questions for each section
    try:
        mcq_questions = generate_mcq_questions(config, model, api_key)
        subjective_questions = generate_subjective_questions(config, model, api_key)
        coding_problems = generate_coding_questions(config, model, api_key)
        
        # Build result
        result = {
            "mcq": mcq_questions,
            "subjective": subjective_questions,
            "coding": coding_problems
        }
        
        return result
        
    except Exception as e:
        raise RuntimeError(f"Failed to generate assessment: {str(e)}")


if __name__ == "__main__":
    # Test configuration
    test_config = {
        "experience_years": 2,
        "experience_level": "Mid",
        "difficulty": "Medium",
        "sections": {
            "mcq": {
                "total_time_minutes": 20,
                "question_count": 15
            },
            "subjective": {
                "topic": "SQL",
                "total_time_minutes": 30,
                "question_count": 10
            },
            "coding": {
                "topic": "DSA",
                "total_time_minutes": 120,
                "question_count": 2
            }
        }
    }
    
    print("=" * 80)
    print("Assessment Generator - Test")
    print("=" * 80)
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("\n⚠️  GEMINI_API_KEY not set in environment")
        print("Set it using: export GEMINI_API_KEY='your-api-key'")
        print("\nOr pass it directly in the code.")
    else:
        try:
            result = generate_assessment(test_config, api_key=api_key)
            print("\n✅ Assessment generated successfully!")
            print("\n" + json.dumps(result, indent=2))
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()

