# DSA Engine - Pattern-Based Question Generation

## Overview

The DSA Engine generates Data Structures and Algorithms questions using predefined algorithmic patterns and validates all test cases using reference solvers. This ensures 100% correctness of test cases.

## Architecture

### Phase-1 Patterns (8 Core Patterns)

1. **Array + Hashing** - Frequency counting, lookup, pair matching
2. **Two Pointers** - Traversing from different positions
3. **Sliding Window** - Maintaining a window of elements
4. **Stack** - LIFO-based problems
5. **Binary Search** - Searching in sorted arrays
6. **Recursion / Backtracking** - Basic recursive solutions
7. **Linked List** - Operations on linked lists
8. **Tree Traversal** - DFS and BFS traversal

### Key Components

#### 1. Pattern Configuration (`configs/patterns.json`)
- Defines all 8 patterns with descriptions
- Specifies allowed operations per pattern
- Defines test case types (Normal, Duplicate, Edge, Negative, Boundary)
- Configures public/hidden test split

#### 2. Reference Solvers (`reference_solvers/`)
- One reference solver per pattern
- Generates correct expected outputs
- Used to validate all test cases

#### 3. Test Case Generator (`test_case_generator.py`)
- Uses AI to generate test case inputs
- Validates using reference solvers
- Splits into public (2) and hidden (4) tests

## Test Case Generation Flow

```
AI generates problem statement + inputs
        ↓
Backend feeds inputs to reference solver
        ↓
Expected output generated (guaranteed correct)
        ↓
Store as test case (public or hidden)
```

## Usage

### Basic Usage

```python
from dsa_engine import generate_dsa_test_cases

# Generate test cases for a problem
test_cases = generate_dsa_test_cases(
    pattern_name="Array + Hashing",
    problem_statement="Given an array of integers, find two numbers that add up to a target value.",
    problem_type="two_sum",
    api_key="your-api-key"
)

# Result structure:
# {
#   "public_tests": [...],  # 2 simple tests
#   "hidden_tests": [...],   # 4 edge/boundary tests
#   "total_tests": 6,
#   "pattern": "Array + Hashing",
#   "problem_type": "two_sum"
# }
```

### Integration with Assessment Generator

The DSA engine is automatically integrated into `assessment_generator.py`. When generating coding questions:

1. AI generates problem statement with pattern and problem_type
2. DSA engine generates validated test cases
3. Test cases are attached to the problem

## Test Case Types

- **Normal**: Standard input testing core logic
- **Duplicate**: Inputs with duplicate values
- **Edge**: Smallest valid input (empty, single element)
- **Negative**: Negative numbers or sign edge cases
- **Boundary**: Largest valid input or boundary conditions

## Public vs Hidden Split

- **Public Tests (2)**: Simple, readable tests (Normal type)
- **Hidden Tests (4)**: Edge cases, boundaries, duplicates, negatives

## Reference Solvers

Each pattern has a reference solver that implements common problem types:

- **Array + Hashing**: two_sum, contains_duplicate, group_anagrams, longest_consecutive
- **Two Pointers**: valid_palindrome, two_sum_sorted, container_water, three_sum
- **Sliding Window**: longest_substring, min_window, max_average, length_of_longest_substring
- **Stack**: valid_parentheses, daily_temperatures, next_greater, largest_rectangle
- **Binary Search**: search_rotated, find_peak, search_range, search_insert
- **Recursion / Backtracking**: generate_parentheses, combination_sum, subsets, permutations
- **Linked List**: reverse_list, merge_lists, has_cycle, remove_nth
- **Tree Traversal**: max_depth, same_tree, level_order, path_sum

## Benefits

1. **100% Correct Test Cases**: All test cases validated by reference solvers
2. **Pattern-Based**: Questions follow industry-standard patterns
3. **Scalable**: Easy to add new patterns and problem types
4. **Validated**: Every test case has guaranteed correct expected output

## Industry Standard

> "We generate DSA questions using predefined algorithmic patterns and validate all test cases using reference solvers."

This approach ensures:
- Consistent question quality
- Reliable test case correctness
- Industry-standard problem patterns
- Professional assessment generation

