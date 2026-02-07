"""
DSA Engine - Pattern-Based Question Generation
Generates DSA questions using predefined patterns and validates with reference solvers
"""

from .test_case_generator import generate_dsa_test_cases, get_pattern_blueprint
from .reference_solvers import get_reference_solver

__all__ = [
    'generate_dsa_test_cases',
    'get_pattern_blueprint',
    'get_reference_solver'
]

