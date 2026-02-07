"""
Reference Solver: Recursion / Backtracking Pattern
Handles problems like Generate Parentheses, Combination Sum, Subsets, Permutations
"""

from typing import List, Dict, Any

def solve_recursion_backtracking(problem_type: str, inputs: Dict[str, Any]) -> Any:
    """Reference solver for Recursion / Backtracking pattern"""
    if problem_type == "generate_parentheses":
        n = inputs.get("n", 0)
        return _generate_parentheses(n)
    
    elif problem_type == "combination_sum":
        candidates = inputs.get("candidates", [])
        target = inputs.get("target", 0)
        return _combination_sum(candidates, target)
    
    elif problem_type == "subsets":
        nums = inputs.get("nums", [])
        return _subsets(nums)
    
    elif problem_type == "permutations":
        nums = inputs.get("nums", [])
        return _permutations(nums)
    
    else:
        raise ValueError(f"Unknown problem type: {problem_type}")

def _generate_parentheses(n: int) -> List[str]:
    """Generate Parentheses: All valid combinations"""
    result = []
    
    def backtrack(current, open_count, close_count):
        if len(current) == 2 * n:
            result.append(current)
            return
        
        if open_count < n:
            backtrack(current + '(', open_count + 1, close_count)
        
        if close_count < open_count:
            backtrack(current + ')', open_count, close_count + 1)
    
    backtrack("", 0, 0)
    return result

def _combination_sum(candidates: List[int], target: int) -> List[List[int]]:
    """Combination Sum: All unique combinations that sum to target"""
    result = []
    candidates.sort()
    
    def backtrack(remaining, combo, start):
        if remaining == 0:
            result.append(combo[:])
            return
        
        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break
            
            combo.append(candidates[i])
            backtrack(remaining - candidates[i], combo, i)
            combo.pop()
    
    backtrack(target, [], 0)
    return result

def _subsets(nums: List[int]) -> List[List[int]]:
    """Subsets: All possible subsets"""
    result = []
    
    def backtrack(start, current):
        result.append(current[:])
        
        for i in range(start, len(nums)):
            current.append(nums[i])
            backtrack(i + 1, current)
            current.pop()
    
    backtrack(0, [])
    return result

def _permutations(nums: List[int]) -> List[List[int]]:
    """Permutations: All possible permutations"""
    result = []
    
    def backtrack(current):
        if len(current) == len(nums):
            result.append(current[:])
            return
        
        for num in nums:
            if num not in current:
                current.append(num)
                backtrack(current)
                current.pop()
    
    backtrack([])
    return result

