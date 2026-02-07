"""
Reference Solver: Binary Search Pattern
Handles problems like Search in Rotated Array, Find Peak, Search Range, etc.
"""

from typing import List, Dict, Any

def solve_binary_search(problem_type: str, inputs: Dict[str, Any]) -> Any:
    """Reference solver for Binary Search pattern"""
    if problem_type == "search_rotated":
        nums = inputs.get("nums", [])
        target = inputs.get("target", 0)
        return _search_rotated(nums, target)
    
    elif problem_type == "find_peak":
        nums = inputs.get("nums", [])
        return _find_peak(nums)
    
    elif problem_type == "search_range":
        nums = inputs.get("nums", [])
        target = inputs.get("target", 0)
        return _search_range(nums, target)
    
    elif problem_type == "search_insert":
        nums = inputs.get("nums", [])
        target = inputs.get("target", 0)
        return _search_insert(nums, target)
    
    else:
        raise ValueError(f"Unknown problem type: {problem_type}")

def _search_rotated(nums: List[int], target: int) -> int:
    """Search in Rotated Sorted Array"""
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if nums[mid] == target:
            return mid
        
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    
    return -1

def _find_peak(nums: List[int]) -> int:
    """Find Peak Element"""
    left, right = 0, len(nums) - 1
    
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[mid + 1]:
            right = mid
        else:
            left = mid + 1
    
    return left

def _search_range(nums: List[int], target: int) -> List[int]:
    """Search for Range: Find first and last position"""
    def find_first():
        left, right = 0, len(nums) - 1
        first = -1
        
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                first = mid
                right = mid - 1
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return first
    
    def find_last():
        left, right = 0, len(nums) - 1
        last = -1
        
        while left <= right:
            mid = (left + right) // 2
            if nums[mid] == target:
                last = mid
                left = mid + 1
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1
        
        return last
    
    first = find_first()
    if first == -1:
        return [-1, -1]
    
    last = find_last()
    return [first, last]

def _search_insert(nums: List[int], target: int) -> int:
    """Search Insert Position"""
    left, right = 0, len(nums) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return left

