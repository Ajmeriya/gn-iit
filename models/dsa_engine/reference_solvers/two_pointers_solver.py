"""
Reference Solver: Two Pointers Pattern
Handles problems like Valid Palindrome, Two Sum (sorted), Container With Most Water, etc.
"""

from typing import List, Dict, Any

def solve_two_pointers(problem_type: str, inputs: Dict[str, Any]) -> Any:
    """Reference solver for Two Pointers pattern"""
    if problem_type == "valid_palindrome":
        s = inputs.get("s", "")
        return _valid_palindrome(s)
    
    elif problem_type == "two_sum_sorted":
        numbers = inputs.get("numbers", [])
        target = inputs.get("target", 0)
        return _two_sum_sorted(numbers, target)
    
    elif problem_type == "container_water":
        height = inputs.get("height", [])
        return _container_water(height)
    
    elif problem_type == "three_sum":
        nums = inputs.get("nums", [])
        return _three_sum(nums)
    
    else:
        raise ValueError(f"Unknown problem type: {problem_type}")

def _valid_palindrome(s: str) -> bool:
    """Valid Palindrome: Check if string is palindrome (alphanumeric only)"""
    left, right = 0, len(s) - 1
    
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        
        if s[left].lower() != s[right].lower():
            return False
        
        left += 1
        right -= 1
    
    return True

def _two_sum_sorted(numbers: List[int], target: int) -> List[int]:
    """Two Sum (sorted array): Find indices (1-indexed)"""
    left, right = 0, len(numbers) - 1
    
    while left < right:
        current_sum = numbers[left] + numbers[right]
        if current_sum == target:
            return [left + 1, right + 1]  # 1-indexed
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    
    return []

def _container_water(height: List[int]) -> int:
    """Container With Most Water: Maximum area"""
    left, right = 0, len(height) - 1
    max_area = 0
    
    while left < right:
        width = right - left
        area = width * min(height[left], height[right])
        max_area = max(max_area, area)
        
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    
    return max_area

def _three_sum(nums: List[int]) -> List[List[int]]:
    """3Sum: Find all unique triplets that sum to zero"""
    nums.sort()
    result = []
    
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        
        left, right = i + 1, len(nums) - 1
        
        while left < right:
            current_sum = nums[i] + nums[left] + nums[right]
            
            if current_sum == 0:
                result.append([nums[i], nums[left], nums[right]])
                
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif current_sum < 0:
                left += 1
            else:
                right -= 1
    
    return result

