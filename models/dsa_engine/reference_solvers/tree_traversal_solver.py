"""
Reference Solver: Tree Traversal Pattern
Handles problems like Maximum Depth, Same Tree, Level Order, Path Sum, etc.
"""

from typing import List, Dict, Any, Optional
from collections import deque

class TreeNode:
    """Simple TreeNode class for reference solver"""
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def solve_tree_traversal(problem_type: str, inputs: Dict[str, Any]) -> Any:
    """Reference solver for Tree Traversal pattern"""
    if problem_type == "max_depth":
        root = _list_to_tree(inputs.get("values", []))
        return _max_depth(root)
    
    elif problem_type == "same_tree":
        p_values = inputs.get("p", [])
        q_values = inputs.get("q", [])
        p = _list_to_tree(p_values)
        q = _list_to_tree(q_values)
        return _same_tree(p, q)
    
    elif problem_type == "level_order":
        root = _list_to_tree(inputs.get("values", []))
        return _level_order(root)
    
    elif problem_type == "path_sum":
        root = _list_to_tree(inputs.get("values", []))
        target_sum = inputs.get("targetSum", 0)
        return _path_sum(root, target_sum)
    
    else:
        raise ValueError(f"Unknown problem type: {problem_type}")

def _list_to_tree(values: List[Any]) -> Optional[TreeNode]:
    """Convert level-order list to binary tree (None for null nodes)"""
    if not values:
        return None
    
    root = TreeNode(values[0])
    queue = deque([root])
    i = 1
    
    while queue and i < len(values):
        node = queue.popleft()
        
        if i < len(values) and values[i] is not None:
            node.left = TreeNode(values[i])
            queue.append(node.left)
        i += 1
        
        if i < len(values) and values[i] is not None:
            node.right = TreeNode(values[i])
            queue.append(node.right)
        i += 1
    
    return root

def _max_depth(root: Optional[TreeNode]) -> int:
    """Maximum Depth of Binary Tree"""
    if not root:
        return 0
    
    return 1 + max(_max_depth(root.left), _max_depth(root.right))

def _same_tree(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
    """Same Tree: Check if two trees are identical"""
    if not p and not q:
        return True
    
    if not p or not q:
        return False
    
    if p.val != q.val:
        return False
    
    return _same_tree(p.left, q.left) and _same_tree(p.right, q.right)

def _level_order(root: Optional[TreeNode]) -> List[List[int]]:
    """Binary Tree Level Order Traversal"""
    if not root:
        return []
    
    result = []
    queue = deque([root])
    
    while queue:
        level_size = len(queue)
        level = []
        
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        result.append(level)
    
    return result

def _path_sum(root: Optional[TreeNode], target_sum: int) -> bool:
    """Path Sum: Check if root-to-leaf path exists with target sum"""
    if not root:
        return False
    
    if not root.left and not root.right:
        return root.val == target_sum
    
    remaining = target_sum - root.val
    return _path_sum(root.left, remaining) or _path_sum(root.right, remaining)

