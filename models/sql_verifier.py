"""
SQL Query Verifier
Executes and validates SQL queries against expected results
"""

import sqlite3
import json
from typing import Dict, List, Optional, Any
import re


def create_test_database(schema: str, test_data: Optional[List[Dict]] = None) -> sqlite3.Connection:
    """
    Create an in-memory SQLite database with the given schema and test data.
    
    Args:
        schema: SQL DDL statements to create tables
        test_data: Optional list of INSERT statements or data dictionaries
        
    Returns:
        SQLite connection to the test database
    """
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # Execute schema
    try:
        cursor.executescript(schema)
        conn.commit()
    except sqlite3.Error as e:
        conn.close()
        raise RuntimeError(f"Failed to create database schema: {str(e)}")
    
    # Insert test data if provided
    if test_data:
        for item in test_data:
            if isinstance(item, str):
                # Direct SQL INSERT statement
                try:
                    cursor.execute(item)
                except sqlite3.Error:
                    pass  # Ignore errors for test data
            elif isinstance(item, dict):
                # Dictionary with table and data
                table = item.get('table')
                data = item.get('data', [])
                if table and data:
                    for row in data:
                        try:
                            columns = ', '.join(row.keys())
                            placeholders = ', '.join(['?' for _ in row])
                            values = list(row.values())
                            cursor.execute(f"INSERT INTO {table} ({columns}) VALUES ({placeholders})", values)
                        except sqlite3.Error:
                            pass
        conn.commit()
    
    return conn


def execute_sql_query(conn: sqlite3.Connection, query: str) -> Dict[str, Any]:
    """
    Execute a SQL query and return results.
    
    Args:
        conn: SQLite database connection
        query: SQL query to execute
        
    Returns:
        Dictionary with:
        - success: bool
        - results: list of rows (if SELECT)
        - columns: list of column names (if SELECT)
        - error: error message (if failed)
        - row_count: number of rows affected/returned
    """
    try:
        cursor = conn.cursor()
        
        # Clean query - remove comments and extra whitespace
        query = re.sub(r'--.*?$', '', query, flags=re.MULTILINE)
        query = re.sub(r'/\*.*?\*/', '', query, flags=re.DOTALL)
        query = query.strip()
        
        if not query:
            return {
                "success": False,
                "error": "Empty query",
                "results": [],
                "columns": [],
                "row_count": 0
            }
        
        cursor.execute(query)
        
        # Check if it's a SELECT query
        if query.strip().upper().startswith('SELECT'):
            results = cursor.fetchall()
            columns = [description[0] for description in cursor.description] if cursor.description else []
            
            # Convert to list of dictionaries
            result_list = []
            for row in results:
                result_dict = {}
                for i, col in enumerate(columns):
                    result_dict[col] = row[i]
                result_list.append(result_dict)
            
            return {
                "success": True,
                "results": result_list,
                "columns": columns,
                "row_count": len(results),
                "error": None
            }
        else:
            # INSERT, UPDATE, DELETE, etc.
            conn.commit()
            return {
                "success": True,
                "results": [],
                "columns": [],
                "row_count": cursor.rowcount,
                "error": None
            }
            
    except sqlite3.Error as e:
        return {
            "success": False,
            "error": str(e),
            "results": [],
            "columns": [],
            "row_count": 0
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "results": [],
            "columns": [],
            "row_count": 0
        }


def compare_query_results(result1: List[Dict], result2: List[Dict], 
                         ignore_order: bool = True, 
                         ignore_case: bool = True) -> Dict[str, Any]:
    """
    Compare two query result sets.
    
    Args:
        result1: First result set (list of dictionaries)
        result2: Second result set (list of dictionaries)
        ignore_order: If True, ignore row order when comparing
        ignore_case: If True, ignore case for string comparisons
        
    Returns:
        Dictionary with:
        - match: bool
        - message: str
        - differences: list of differences
    """
    if not result1 and not result2:
        return {
            "match": True,
            "message": "Both results are empty",
            "differences": []
        }
    
    if len(result1) != len(result2):
        return {
            "match": False,
            "message": f"Row count mismatch: {len(result1)} vs {len(result2)}",
            "differences": [f"Expected {len(result2)} rows, got {len(result1)}"]
        }
    
    # Normalize results
    def normalize_row(row: Dict) -> Dict:
        normalized = {}
        for k, v in row.items():
            key = k.lower() if ignore_case else k
            if isinstance(v, str) and ignore_case:
                normalized[key] = v.lower()
            else:
                normalized[key] = v
        return normalized
    
    norm1 = [normalize_row(r) for r in result1]
    norm2 = [normalize_row(r) for r in result2]
    
    if ignore_order:
        # Sort by all column values
        def sort_key(row):
            return tuple(sorted(row.items()))
        norm1_sorted = sorted(norm1, key=sort_key)
        norm2_sorted = sorted(norm2, key=sort_key)
    else:
        norm1_sorted = norm1
        norm2_sorted = norm2
    
    # Compare row by row
    differences = []
    for i, (r1, r2) in enumerate(zip(norm1_sorted, norm2_sorted)):
        if r1 != r2:
            differences.append(f"Row {i+1} mismatch: {r1} vs {r2}")
    
    if differences:
        return {
            "match": False,
            "message": f"Found {len(differences)} row differences",
            "differences": differences
        }
    
    return {
        "match": True,
        "message": "Results match",
        "differences": []
    }


def verify_sql_answer(
    user_query: str,
    expected_query: Optional[str] = None,
    schema: Optional[str] = None,
    test_data: Optional[List[Dict]] = None,
    expected_result: Optional[List[Dict]] = None,
    ignore_order: bool = True,
    ignore_case: bool = True
) -> Dict[str, Any]:
    """
    Verify a SQL query answer.
    
    Args:
        user_query: The SQL query submitted by the user
        expected_query: Optional expected SQL query (for exact match)
        schema: Database schema (DDL statements)
        test_data: Test data to insert
        expected_result: Expected query result
        ignore_order: Ignore row order when comparing
        ignore_case: Ignore case for string comparisons
        
    Returns:
        Dictionary with:
        - correct: bool
        - score: float (0.0 to 1.0)
        - message: str
        - user_result: user query execution result
        - expected_result: expected result
        - comparison: comparison details
    """
    if not user_query or not user_query.strip():
        return {
            "correct": False,
            "score": 0.0,
            "message": "Empty query submitted",
            "user_result": None,
            "expected_result": expected_result,
            "comparison": None
        }
    
    # If expected_query is provided, do syntax/semantic comparison
    if expected_query:
        # Simple comparison (can be enhanced with AST parsing)
        user_normalized = re.sub(r'\s+', ' ', user_query.strip().upper())
        expected_normalized = re.sub(r'\s+', ' ', expected_query.strip().upper())
        
        if user_normalized == expected_normalized:
            return {
                "correct": True,
                "score": 1.0,
                "message": "Query matches expected query exactly",
                "user_result": None,
                "expected_result": expected_result,
                "comparison": {"type": "exact_match"}
            }
    
    # Execute user query if schema is provided
    if schema:
        try:
            conn = create_test_database(schema, test_data)
            user_execution = execute_sql_query(conn, user_query)
            conn.close()
            
            if not user_execution["success"]:
                return {
                    "correct": False,
                    "score": 0.0,
                    "message": f"Query execution failed: {user_execution['error']}",
                    "user_result": user_execution,
                    "expected_result": expected_result,
                    "comparison": None
                }
            
            # Compare with expected result
            if expected_result is not None:
                comparison = compare_query_results(
                    user_execution["results"],
                    expected_result,
                    ignore_order=ignore_order,
                    ignore_case=ignore_case
                )
                
                return {
                    "correct": comparison["match"],
                    "score": 1.0 if comparison["match"] else 0.0,
                    "message": comparison["message"],
                    "user_result": user_execution,
                    "expected_result": expected_result,
                    "comparison": comparison
                }
            else:
                # No expected result - just check if query executed successfully
                return {
                    "correct": True,
                    "score": 0.5,  # Partial credit for valid syntax
                    "message": "Query executed successfully (no expected result to compare)",
                    "user_result": user_execution,
                    "expected_result": None,
                    "comparison": None
                }
        except Exception as e:
            return {
                "correct": False,
                "score": 0.0,
                "message": f"Error during verification: {str(e)}",
                "user_result": None,
                "expected_result": expected_result,
                "comparison": None
            }
    
    # Fallback: if no schema/expected result, return partial credit
    return {
        "correct": False,
        "score": 0.0,
        "message": "No verification method available (missing schema or expected result)",
        "user_result": None,
        "expected_result": expected_result,
        "comparison": None
    }


# Example usage
if __name__ == "__main__":
    # Example schema
    schema = """
    CREATE TABLE employees (
        id INTEGER PRIMARY KEY,
        name TEXT,
        department TEXT,
        salary INTEGER
    );
    """
    
    # Example test data
    test_data = [
        "INSERT INTO employees (id, name, department, salary) VALUES (1, 'Alice', 'Engineering', 100000);",
        "INSERT INTO employees (id, name, department, salary) VALUES (2, 'Bob', 'Engineering', 95000);",
        "INSERT INTO employees (id, name, department, salary) VALUES (3, 'Charlie', 'Sales', 80000);",
    ]
    
    # Test query
    user_query = "SELECT name, salary FROM employees WHERE department = 'Engineering' ORDER BY salary DESC;"
    expected_result = [
        {"name": "Alice", "salary": 100000},
        {"name": "Bob", "salary": 95000}
    ]
    
    result = verify_sql_answer(
        user_query=user_query,
        schema=schema,
        test_data=test_data,
        expected_result=expected_result
    )
    
    print(json.dumps(result, indent=2))

