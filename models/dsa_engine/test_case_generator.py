"""
Test Case Generator for DSA Questions
Generates test cases using AI, validates with reference solvers, and splits into public/hidden
"""

import json
import os
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

# Import reference solvers
from .reference_solvers import get_reference_solver

# Load pattern configurations
CONFIG_PATH = Path(__file__).parent / "configs" / "patterns.json"

def load_pattern_config() -> Dict[str, Any]:
    """Load pattern configuration from JSON"""
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def get_pattern_blueprint(pattern_name: str) -> Dict[str, Any]:
    """Get test case blueprint for a specific pattern"""
    config = load_pattern_config()
    
    pattern = next((p for p in config["patterns"] if p["pattern"] == pattern_name), None)
    if not pattern:
        raise ValueError(f"Pattern not found: {pattern_name}")
    
    return {
        "pattern": pattern,
        "test_case_types": config["test_case_types"],
        "test_split": config["test_split"]
    }

def generate_dsa_test_cases(
    pattern_name: str,
    problem_statement: str,
    problem_type: str,
    api_key: Optional[str] = None,
    model_name: Optional[str] = None
) -> Dict[str, Any]:
    """
    Generate test cases for a DSA problem using AI and validate with reference solver.
    
    Args:
        pattern_name: Name of the pattern (e.g., "Array + Hashing")
        problem_statement: The problem description
        problem_type: Type identifier (e.g., "two_sum", "valid_palindrome")
        api_key: Google AI API key
        model_name: Optional model name override
        
    Returns:
        Dictionary with public and hidden test cases, all validated
    """
    import google.generativeai as genai
    
    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        raise ValueError("API key required. Set GEMINI_API_KEY or pass api_key parameter")
    
    genai.configure(api_key=api_key)
    
    # Get pattern blueprint
    blueprint = get_pattern_blueprint(pattern_name)
    test_types = blueprint["test_case_types"]
    test_split = blueprint["test_split"]
    
    # Get reference solver
    solver = get_reference_solver(pattern_name)
    
    # Use model
    if not model_name:
        try:
            models = list(genai.list_models())
            gemini_models = [
                m.name for m in models 
                if "gemini" in m.name.lower() and "generateContent" in m.supported_generation_methods
            ]
            model_name = gemini_models[0] if gemini_models else "models/text-bison-001"
        except:
            model_name = "models/text-bison-001"
    
    model = genai.GenerativeModel(model_name)
    
    # Generate test case inputs using AI
    prompt = f"""
Generate test case inputs for this DSA problem:

Problem: {problem_statement}
Pattern: {pattern_name}
Problem Type: {problem_type}

Generate test case inputs for each type:
1. Normal: Standard input testing core logic
2. Duplicate: Inputs with duplicate values (if applicable)
3. Edge: Smallest valid input (empty, single element, etc.)
4. Negative: Negative numbers or edge cases with signs (if applicable)
5. Boundary: Largest valid input or boundary conditions

For each test case, provide ONLY the input parameters as a JSON object.
Return a JSON array with this structure:
[
  {{"type": "Normal", "inputs": {{"param1": value1, "param2": value2}}}},
  {{"type": "Duplicate", "inputs": {{"param1": value1, "param2": value2}}}},
  {{"type": "Edge", "inputs": {{"param1": value1, "param2": value2}}}},
  {{"type": "Negative", "inputs": {{"param1": value1, "param2": value2}}}},
  {{"type": "Boundary", "inputs": {{"param1": value1, "param2": value2}}}}
]

Return ONLY valid JSON, no explanations.
"""
    
    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Clean JSON (remove markdown code blocks if present)
        if response_text.startswith("```"):
            response_text = response_text.split("```")[1]
            if response_text.startswith("json"):
                response_text = response_text[4:]
        response_text = response_text.strip()
        
        test_inputs = json.loads(response_text)
    except Exception as e:
        raise ValueError(f"Failed to generate test inputs: {str(e)}")
    
    # Validate each test case using reference solver
    validated_tests = []
    
    for test_input in test_inputs:
        test_type = test_input.get("type", "Normal")
        inputs = test_input.get("inputs", {})
        
        try:
            # Get expected output from reference solver
            expected_output = solver(problem_type, inputs)
            
            validated_tests.append({
                "type": test_type,
                "input": inputs,
                "expected_output": expected_output
            })
        except Exception as e:
            # Skip invalid test cases
            print(f"Warning: Skipping {test_type} test case due to solver error: {str(e)}")
            continue
    
    # Split into public and hidden
    public_tests = [
        t for t in validated_tests 
        if t["type"] in test_split["public_types"]
    ][:test_split["public_count"]]
    
    hidden_tests = [
        t for t in validated_tests 
        if t["type"] in test_split["hidden_types"]
    ][:test_split["hidden_count"]]
    
    # Ensure we have at least some tests
    if not public_tests and validated_tests:
        public_tests = validated_tests[:test_split["public_count"]]
    
    if not hidden_tests and len(validated_tests) > len(public_tests):
        hidden_tests = validated_tests[len(public_tests):len(public_tests) + test_split["hidden_count"]]
    
    return {
        "public_tests": public_tests,
        "hidden_tests": hidden_tests,
        "total_tests": len(public_tests) + len(hidden_tests),
        "pattern": pattern_name,
        "problem_type": problem_type
    }

def validate_test_case(
    pattern_name: str,
    problem_type: str,
    inputs: Dict[str, Any]
) -> Tuple[Any, bool]:
    """
    Validate a test case using reference solver.
    
    Returns:
        Tuple of (expected_output, is_valid)
    """
    try:
        solver = get_reference_solver(pattern_name)
        expected_output = solver(problem_type, inputs)
        return expected_output, True
    except Exception as e:
        return None, False

__all__ = ['generate_dsa_test_cases', 'get_pattern_blueprint', 'validate_test_case']

