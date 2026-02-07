"""
Reference Solvers for DSA Patterns
Each pattern has one reference solver that generates correct expected outputs
"""

from .array_hashing_solver import solve_array_hashing
from .two_pointers_solver import solve_two_pointers
from .sliding_window_solver import solve_sliding_window
from .stack_solver import solve_stack
from .binary_search_solver import solve_binary_search
from .recursion_backtracking_solver import solve_recursion_backtracking
from .linked_list_solver import solve_linked_list
from .tree_traversal_solver import solve_tree_traversal

PATTERN_SOLVERS = {
    "Array + Hashing": solve_array_hashing,
    "Two Pointers": solve_two_pointers,
    "Sliding Window": solve_sliding_window,
    "Stack": solve_stack,
    "Binary Search": solve_binary_search,
    "Recursion / Backtracking": solve_recursion_backtracking,
    "Linked List": solve_linked_list,
    "Tree Traversal": solve_tree_traversal
}

def get_reference_solver(pattern_name: str):
    """Get reference solver function for a pattern"""
    if pattern_name not in PATTERN_SOLVERS:
        raise ValueError(f"Unknown pattern: {pattern_name}")
    return PATTERN_SOLVERS[pattern_name]

__all__ = ['get_reference_solver', 'PATTERN_SOLVERS']

