"""
Reference Solver: Array + Hashing Pattern
Handles problems like Two Sum, Group Anagrams, Contains Duplicate, etc.
"""

from typing import List, Dict, Any, Optional

def solve_array_hashing(problem_type: str, inputs: Dict[str, Any]) -> Any:
    """
    Reference solver for Array + Hashing pattern.
    
    Args:
        problem_type: Type of problem (e.g., "two_sum", "contains_duplicate")
        inputs: Dictionary with input parameters
        
    Returns:
        Expected output for the given inputs
    """
    if problem_type == "two_sum":
        nums = inputs.get("nums", [])
        target = inputs.get("target", 0)
        return _two_sum(nums, target)
    
    elif problem_type == "contains_duplicate":
        nums = inputs.get("nums", [])
        return _contains_duplicate(nums)
    
    elif problem_type == "group_anagrams":
        strs = inputs.get("strs", [])
        return _group_anagrams(strs)
    
    elif problem_type == "longest_consecutive":
        nums = inputs.get("nums", [])
        return _longest_consecutive(nums)
    
    else:
        raise ValueError(f"Unknown problem type: {problem_type}")

def _two_sum(nums: List[int], target: int) -> List[int]:
    """Two Sum: Find indices of two numbers that add up to target"""
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []

def _contains_duplicate(nums: List[int]) -> bool:
    """Contains Duplicate: Check if array has duplicates"""
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False

def _group_anagrams(strs: List[str]) -> List[List[str]]:
    """Group Anagrams: Group strings that are anagrams"""
    groups = {}
    for s in strs:
        key = ''.join(sorted(s))
        if key not in groups:
            groups[key] = []
        groups[key].append(s)
    return list(groups.values())

def _longest_consecutive(nums: List[int]) -> int:
    """Longest Consecutive Sequence: Find longest consecutive sequence length"""
    if not nums:
        return 0
    
    num_set = set(nums)
    max_length = 0
    
    for num in num_set:
        if num - 1 not in num_set:  # Start of sequence
            current_length = 1
            while num + current_length in num_set:
                current_length += 1
            max_length = max(max_length, current_length)
    
    return max_length

