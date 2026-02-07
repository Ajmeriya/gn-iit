"""
Reference Solver: Sliding Window Pattern
Handles problems like Longest Substring, Minimum Window, Maximum Average, etc.
"""

from typing import List, Dict, Any

def solve_sliding_window(problem_type: str, inputs: Dict[str, Any]) -> Any:
    """Reference solver for Sliding Window pattern"""
    if problem_type == "longest_substring":
        s = inputs.get("s", "")
        return _longest_substring(s)
    
    elif problem_type == "min_window":
        s = inputs.get("s", "")
        t = inputs.get("t", "")
        return _min_window(s, t)
    
    elif problem_type == "max_average":
        nums = inputs.get("nums", [])
        k = inputs.get("k", 0)
        return _max_average(nums, k)
    
    elif problem_type == "length_of_longest_substring":
        s = inputs.get("s", "")
        k = inputs.get("k", 0)
        return _length_of_longest_substring(s, k)
    
    else:
        raise ValueError(f"Unknown problem type: {problem_type}")

def _longest_substring(s: str) -> int:
    """Longest Substring Without Repeating Characters"""
    char_map = {}
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        if s[right] in char_map and char_map[s[right]] >= left:
            left = char_map[s[right]] + 1
        
        char_map[s[right]] = right
        max_length = max(max_length, right - left + 1)
    
    return max_length

def _min_window(s: str, t: str) -> str:
    """Minimum Window Substring"""
    if not s or not t:
        return ""
    
    from collections import Counter
    required = Counter(t)
    required_count = len(required)
    
    left = 0
    formed = 0
    window_counts = {}
    
    min_len = float('inf')
    min_window = ""
    
    for right in range(len(s)):
        char = s[right]
        window_counts[char] = window_counts.get(char, 0) + 1
        
        if char in required and window_counts[char] == required[char]:
            formed += 1
        
        while left <= right and formed == required_count:
            if right - left + 1 < min_len:
                min_len = right - left + 1
                min_window = s[left:right + 1]
            
            char = s[left]
            window_counts[char] -= 1
            if char in required and window_counts[char] < required[char]:
                formed -= 1
            
            left += 1
    
    return min_window if min_len != float('inf') else ""

def _max_average(nums: List[int], k: int) -> float:
    """Maximum Average Subarray of length k"""
    if not nums or k == 0:
        return 0.0
    
    window_sum = sum(nums[:k])
    max_sum = window_sum
    
    for i in range(k, len(nums)):
        window_sum = window_sum - nums[i - k] + nums[i]
        max_sum = max(max_sum, window_sum)
    
    return max_sum / k

def _length_of_longest_substring(s: str, k: int) -> int:
    """Longest Substring with At Most K Distinct Characters"""
    if not s or k == 0:
        return 0
    
    char_count = {}
    left = 0
    max_length = 0
    
    for right in range(len(s)):
        char_count[s[right]] = char_count.get(s[right], 0) + 1
        
        while len(char_count) > k:
            char_count[s[left]] -= 1
            if char_count[s[left]] == 0:
                del char_count[s[left]]
            left += 1
        
        max_length = max(max_length, right - left + 1)
    
    return max_length

