"""
Code Executor for DSA Questions
Executes code and runs test cases
"""

import subprocess
import tempfile
import os
import json
from typing import Dict, List, Optional, Any
import sys


def execute_code(code: str, language: str = "python", timeout: int = 10) -> Dict[str, Any]:
    """
    Execute code and return output.
    
    Args:
        code: Source code to execute
        language: Programming language (python, javascript, java, cpp)
        timeout: Execution timeout in seconds
        
    Returns:
        Dictionary with:
        - success: bool
        - output: str (stdout)
        - error: str (stderr)
        - exit_code: int
        - execution_time: float (seconds)
    """
    import time
    
    start_time = time.time()
    
    # Create temporary file
    ext_map = {
        "python": ".py",
        "javascript": ".js",
        "java": ".java",
        "cpp": ".cpp",
        "c": ".c"
    }
    
    ext = ext_map.get(language.lower(), ".py")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix=ext, delete=False) as f:
        f.write(code)
        temp_file = f.name
    
    try:
        # Execute based on language
        if language.lower() == "python":
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=timeout
            )
        elif language.lower() == "javascript":
            result = subprocess.run(
                ["node", temp_file],
                capture_output=True,
                text=True,
                timeout=timeout
            )
        elif language.lower() == "java":
            # Compile first
            compile_result = subprocess.run(
                ["javac", temp_file],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            if compile_result.returncode != 0:
                return {
                    "success": False,
                    "output": "",
                    "error": compile_result.stderr,
                    "exit_code": compile_result.returncode,
                    "execution_time": time.time() - start_time
                }
            # Run compiled class
            class_name = os.path.splitext(os.path.basename(temp_file))[0]
            class_dir = os.path.dirname(temp_file)
            result = subprocess.run(
                ["java", "-cp", class_dir, class_name],
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=class_dir
            )
        else:
            return {
                "success": False,
                "output": "",
                "error": f"Unsupported language: {language}",
                "exit_code": -1,
                "execution_time": time.time() - start_time
            }
        
        execution_time = time.time() - start_time
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr,
            "exit_code": result.returncode,
            "execution_time": execution_time
        }
        
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "output": "",
            "error": f"Execution timeout after {timeout} seconds",
            "exit_code": -1,
            "execution_time": timeout
        }
    except Exception as e:
        return {
            "success": False,
            "output": "",
            "error": f"Execution error: {str(e)}",
            "exit_code": -1,
            "execution_time": time.time() - start_time
        }
    finally:
        # Cleanup
        try:
            os.unlink(temp_file)
            # Remove .class file for Java
            if language.lower() == "java":
                class_file = temp_file.replace(".java", ".class")
                if os.path.exists(class_file):
                    os.unlink(class_file)
        except:
            pass


def run_test_case(code: str, test_case: Dict[str, Any], language: str = "python") -> Dict[str, Any]:
    """
    Run a single test case against code.
    
    Args:
        code: Source code to test
        test_case: Dictionary with:
            - input: input value(s)
            - expected_output: expected output
            - function_name: function name to call (optional)
        language: Programming language
        
    Returns:
        Dictionary with:
        - passed: bool
        - input: input used
        - expected: expected output
        - actual: actual output
        - error: error message if any
    """
    # Wrap code with test harness
    if language.lower() == "python":
        # Extract function name or use default
        function_name = test_case.get("function_name", "solution")
        
        # Create test harness
        test_code = f"""
{code}

# Test execution
import json
import sys

input_data = {json.dumps(test_case.get('input'))}
expected = {json.dumps(test_case.get('expected_output'))}

try:
    result = {function_name}(*input_data) if isinstance(input_data, (list, tuple)) else {function_name}(input_data)
    
    # Compare results
    if result == expected:
        print(json.dumps({{"passed": True, "input": input_data, "expected": expected, "actual": result}}))
        sys.exit(0)
    else:
        print(json.dumps({{"passed": False, "input": input_data, "expected": expected, "actual": result}}))
        sys.exit(1)
except Exception as e:
    print(json.dumps({{"passed": False, "input": input_data, "expected": expected, "actual": None, "error": str(e)}}))
    sys.exit(1)
"""
    else:
        # For other languages, use simpler approach
        test_code = code
    
    execution = execute_code(test_code, language, timeout=5)
    
    if not execution["success"]:
        return {
            "passed": False,
            "input": test_case.get("input"),
            "expected": test_case.get("expected_output"),
            "actual": None,
            "error": execution["error"]
        }
    
    # Parse output
    try:
        result = json.loads(execution["output"].strip())
        return result
    except:
        # Fallback: string comparison
        output = execution["output"].strip()
        expected_str = str(test_case.get("expected_output", ""))
        
        return {
            "passed": output == expected_str,
            "input": test_case.get("input"),
            "expected": test_case.get("expected_output"),
            "actual": output,
            "error": None
        }


def evaluate_dsa_solution(
    code: str,
    test_cases: List[Dict[str, Any]],
    language: str = "python"
) -> Dict[str, Any]:
    """
    Evaluate a DSA solution against multiple test cases.
    
    Args:
        code: Source code solution
        test_cases: List of test case dictionaries
        language: Programming language
        
    Returns:
        Dictionary with:
        - total_tests: int
        - passed_tests: int
        - failed_tests: int
        - score: float (0.0 to 1.0)
        - results: list of individual test results
    """
    if not test_cases:
        return {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "score": 0.0,
            "results": []
        }
    
    results = []
    passed = 0
    
    for i, test_case in enumerate(test_cases):
        result = run_test_case(code, test_case, language)
        results.append({
            "test_case": i + 1,
            **result
        })
        if result.get("passed", False):
            passed += 1
    
    total = len(test_cases)
    score = passed / total if total > 0 else 0.0
    
    return {
        "total_tests": total,
        "passed_tests": passed,
        "failed_tests": total - passed,
        "score": score,
        "results": results
    }


# Example usage
if __name__ == "__main__":
    # Example: Two Sum problem
    code = """
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
"""
    
    test_cases = [
        {
            "input": [[2, 7, 11, 15], 9],
            "expected_output": [0, 1],
            "function_name": "two_sum"
        },
        {
            "input": [[3, 2, 4], 6],
            "expected_output": [1, 2],
            "function_name": "two_sum"
        },
        {
            "input": [[3, 3], 6],
            "expected_output": [0, 1],
            "function_name": "two_sum"
        }
    ]
    
    result = evaluate_dsa_solution(code, test_cases, "python")
    print(json.dumps(result, indent=2))

