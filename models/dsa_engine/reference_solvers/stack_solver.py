"""
Reference Solver: Stack Pattern
Handles problems like Valid Parentheses, Daily Temperatures, Next Greater Element, etc.
"""

from typing import List, Dict, Any

def solve_stack(problem_type: str, inputs: Dict[str, Any]) -> Any:
    """Reference solver for Stack pattern"""
    if problem_type == "valid_parentheses":
        s = inputs.get("s", "")
        return _valid_parentheses(s)
    
    elif problem_type == "daily_temperatures":
        temperatures = inputs.get("temperatures", [])
        return _daily_temperatures(temperatures)
    
    elif problem_type == "next_greater":
        nums = inputs.get("nums", [])
        return _next_greater_element(nums)
    
    elif problem_type == "largest_rectangle":
        heights = inputs.get("heights", [])
        return _largest_rectangle(heights)
    
    else:
        raise ValueError(f"Unknown problem type: {problem_type}")

def _valid_parentheses(s: str) -> bool:
    """Valid Parentheses: Check if parentheses are balanced"""
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    
    for char in s:
        if char in mapping:
            if not stack or stack.pop() != mapping[char]:
                return False
        else:
            stack.append(char)
    
    return len(stack) == 0

def _daily_temperatures(temperatures: List[int]) -> List[int]:
    """Daily Temperatures: Days until warmer temperature"""
    result = [0] * len(temperatures)
    stack = []
    
    for i, temp in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temp:
            prev_index = stack.pop()
            result[prev_index] = i - prev_index
        stack.append(i)
    
    return result

def _next_greater_element(nums: List[int]) -> List[int]:
    """Next Greater Element I: Find next greater element for each"""
    result = [-1] * len(nums)
    stack = []
    
    for i in range(len(nums)):
        while stack and nums[stack[-1]] < nums[i]:
            index = stack.pop()
            result[index] = nums[i]
        stack.append(i)
    
    return result

def _largest_rectangle(heights: List[int]) -> int:
    """Largest Rectangle in Histogram"""
    stack = []
    max_area = 0
    
    for i, height in enumerate(heights):
        while stack and heights[stack[-1]] > height:
            h = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, h * width)
        stack.append(i)
    
    while stack:
        h = heights[stack.pop()]
        width = len(heights) if not stack else len(heights) - stack[-1] - 1
        max_area = max(max_area, h * width)
    
    return max_area

