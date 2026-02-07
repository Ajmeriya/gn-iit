"""
Assessment Scoring Service
Calculates scores for MCQ, SQL, and DSA questions
"""

import json
from typing import Dict, List, Optional, Any

try:
    from sql_verifier import verify_sql_answer
    SQL_VERIFIER_AVAILABLE = True
except ImportError:
    SQL_VERIFIER_AVAILABLE = False
    print("Warning: sql_verifier not available")

try:
    from code_executor import evaluate_dsa_solution
    CODE_EXECUTOR_AVAILABLE = True
except ImportError:
    CODE_EXECUTOR_AVAILABLE = False
    print("Warning: code_executor not available")


def score_mcq_questions(questions: List[Dict], answers: Dict[str, Any]) -> Dict[str, Any]:
    """
    Score MCQ questions.
    
    Args:
        questions: List of MCQ question dictionaries
        answers: Dictionary mapping question ID to answer
        
    Returns:
        Dictionary with:
        - total: int
        - correct: int
        - incorrect: int
        - score: float (0.0 to 1.0)
        - details: list of question results
    """
    if not questions:
        return {
            "total": 0,
            "correct": 0,
            "incorrect": 0,
            "score": 0.0,
            "details": []
        }
    
    correct = 0
    details = []
    
    for q in questions:
        q_id = str(q.get("id", ""))
        correct_answer = q.get("correctAnswer") or q.get("correct_answer")
        user_answer = answers.get(q_id)
        
        is_correct = False
        if correct_answer and user_answer:
            is_correct = str(correct_answer).strip().lower() == str(user_answer).strip().lower()
        
        if is_correct:
            correct += 1
        
        details.append({
            "question_id": q_id,
            "correct": is_correct,
            "user_answer": user_answer,
            "correct_answer": correct_answer
        })
    
    total = len(questions)
    score = correct / total if total > 0 else 0.0
    
    return {
        "total": total,
        "correct": correct,
        "incorrect": total - correct,
        "score": score,
        "details": details
    }


def score_sql_questions(questions: List[Dict], answers: Dict[str, Any]) -> Dict[str, Any]:
    """
    Score SQL questions.
    
    Args:
        questions: List of SQL question dictionaries
        answers: Dictionary mapping question ID to SQL query
        
    Returns:
        Dictionary with:
        - total: int
        - correct: int
        - incorrect: int
        - score: float (0.0 to 1.0)
        - details: list of question results
    """
    if not questions or not SQL_VERIFIER_AVAILABLE:
        return {
            "total": len(questions) if questions else 0,
            "correct": 0,
            "incorrect": len(questions) if questions else 0,
            "score": 0.0,
            "details": []
        }
    
    correct = 0
    details = []
    
    for q in questions:
        q_id = str(q.get("id", ""))
        user_query = answers.get(q_id, "")
        
        # Extract verification data from question
        schema = q.get("schema")
        test_data = q.get("test_data")
        expected_result = q.get("expected_result")
        expected_query = q.get("expected_query")
        
        if not user_query:
            details.append({
                "question_id": q_id,
                "correct": False,
                "score": 0.0,
                "message": "No answer provided"
            })
            continue
        
        # Verify SQL answer
        verification = verify_sql_answer(
            user_query=user_query,
            expected_query=expected_query,
            schema=schema,
            test_data=test_data,
            expected_result=expected_result
        )
        
        if verification["correct"]:
            correct += 1
        
        details.append({
            "question_id": q_id,
            "correct": verification["correct"],
            "score": verification["score"],
            "message": verification["message"],
            "user_result": verification.get("user_result"),
            "comparison": verification.get("comparison")
        })
    
    total = len(questions)
    score = correct / total if total > 0 else 0.0
    
    return {
        "total": total,
        "correct": correct,
        "incorrect": total - correct,
        "score": score,
        "details": details
    }


def score_dsa_questions(questions: List[Dict], answers: Dict[str, Any]) -> Dict[str, Any]:
    """
    Score DSA questions.
    
    Args:
        questions: List of DSA question dictionaries
        answers: Dictionary mapping question ID to code solution
        
    Returns:
        Dictionary with:
        - total: int
        - correct: int
        - incorrect: int
        - score: float (0.0 to 1.0)
        - details: list of question results
    """
    if not questions or not CODE_EXECUTOR_AVAILABLE:
        return {
            "total": len(questions) if questions else 0,
            "correct": 0,
            "incorrect": len(questions) if questions else 0,
            "score": 0.0,
            "details": []
        }
    
    correct = 0
    details = []
    
    for q in questions:
        q_id = str(q.get("id", ""))
        user_code = answers.get(q_id, "")
        
        if not user_code:
            details.append({
                "question_id": q_id,
                "correct": False,
                "score": 0.0,
                "message": "No code provided"
            })
            continue
        
        # Get test cases from question
        public_tests = q.get("public_tests", q.get("testCases", []))
        hidden_tests = q.get("hidden_tests", [])
        all_tests = public_tests + hidden_tests
        
        if not all_tests:
            # No test cases - give partial credit for valid code
            details.append({
                "question_id": q_id,
                "correct": False,
                "score": 0.5,
                "message": "No test cases available - partial credit for submission"
            })
            continue
        
        # Evaluate solution
        language = q.get("language", "python")
        evaluation = evaluate_dsa_solution(
            code=user_code,
            test_cases=all_tests,
            language=language
        )
        
        # Consider correct if score >= 0.8 (80% of test cases passed)
        is_correct = evaluation["score"] >= 0.8
        
        if is_correct:
            correct += 1
        
        details.append({
            "question_id": q_id,
            "correct": is_correct,
            "score": evaluation["score"],
            "total_tests": evaluation["total_tests"],
            "passed_tests": evaluation["passed_tests"],
            "failed_tests": evaluation["failed_tests"],
            "test_results": evaluation["results"]
        })
    
    total = len(questions)
    score = correct / total if total > 0 else 0.0
    
    return {
        "total": total,
        "correct": correct,
        "incorrect": total - correct,
        "score": score,
        "details": details
    }


def calculate_overall_score(
    mcq_score: Dict[str, Any],
    sql_score: Dict[str, Any],
    dsa_score: Dict[str, Any],
    weights: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Calculate overall assessment score.
    
    Args:
        mcq_score: MCQ scoring result
        sql_score: SQL scoring result
        dsa_score: DSA scoring result
        weights: Optional weights for each section (default: equal weights)
        
    Returns:
        Dictionary with:
        - overall_score: float (0.0 to 100.0)
        - mcq_score: float
        - sql_score: float
        - dsa_score: float
        - breakdown: detailed breakdown
    """
    if weights is None:
        weights = {
            "mcq": 0.3,  # 30%
            "sql": 0.3,  # 30%
            "dsa": 0.4   # 40%
        }
    
    # Normalize weights
    total_weight = weights["mcq"] + weights["sql"] + weights["dsa"]
    if total_weight == 0:
        total_weight = 1.0
    
    mcq_weight = weights["mcq"] / total_weight
    sql_weight = weights["sql"] / total_weight
    dsa_weight = weights["dsa"] / total_weight
    
    # Calculate weighted score
    mcq_contribution = mcq_score["score"] * mcq_weight * 100
    sql_contribution = sql_score["score"] * sql_weight * 100
    dsa_contribution = dsa_score["score"] * dsa_weight * 100
    
    overall_score = mcq_contribution + sql_contribution + dsa_contribution
    
    return {
        "overall_score": round(overall_score, 2),
        "mcq_score": round(mcq_score["score"] * 100, 2),
        "sql_score": round(sql_score["score"] * 100, 2),
        "dsa_score": round(dsa_score["score"] * 100, 2),
        "breakdown": {
            "mcq": {
                "score": mcq_score["score"] * 100,
                "weight": mcq_weight * 100,
                "contribution": mcq_contribution,
                "details": mcq_score
            },
            "sql": {
                "score": sql_score["score"] * 100,
                "weight": sql_weight * 100,
                "contribution": sql_contribution,
                "details": sql_score
            },
            "dsa": {
                "score": dsa_score["score"] * 100,
                "weight": dsa_weight * 100,
                "contribution": dsa_contribution,
                "details": dsa_score
            }
        }
    }


def score_assessment(questions: List[Dict], answers: Dict[str, Any]) -> Dict[str, Any]:
    """
    Score complete assessment.
    
    Args:
        questions: List of all questions (MCQ, SQL, DSA)
        answers: Dictionary mapping question ID to answer
        
    Returns:
        Complete scoring result with overall score and breakdown
    """
    # Separate questions by type
    mcq_questions = [q for q in questions if q.get("type", "").lower() == "mcq"]
    sql_questions = [q for q in questions if q.get("type", "").lower() in ["subjective", "sql"]]
    dsa_questions = [q for q in questions if q.get("type", "").lower() in ["coding", "dsa"]]
    
    # Score each section
    mcq_result = score_mcq_questions(mcq_questions, answers)
    sql_result = score_sql_questions(sql_questions, answers)
    dsa_result = score_dsa_questions(dsa_questions, answers)
    
    # Calculate overall score
    overall = calculate_overall_score(mcq_result, sql_result, dsa_result)
    
    return {
        "overall_score": overall["overall_score"],
        "mcq": mcq_result,
        "sql": sql_result,
        "dsa": dsa_result,
        "breakdown": overall["breakdown"]
    }


# Example usage
if __name__ == "__main__":
    # Example questions
    questions = [
        {
            "id": "1",
            "type": "mcq",
            "question": "What is 2+2?",
            "options": ["3", "4", "5", "6"],
            "correctAnswer": "4"
        },
        {
            "id": "2",
            "type": "sql",
            "question": "Write a query to select all employees",
            "schema": "CREATE TABLE employees (id INT, name TEXT);",
            "expected_result": [{"id": 1, "name": "Alice"}]
        },
        {
            "id": "3",
            "type": "coding",
            "question": "Implement two_sum",
            "public_tests": [
                {"input": [[2, 7, 11, 15], 9], "expected_output": [0, 1]}
            ]
        }
    ]
    
    answers = {
        "1": "4",
        "2": "SELECT * FROM employees;",
        "3": "def two_sum(nums, target):\n    return [0, 1]"
    }
    
    result = score_assessment(questions, answers)
    print(json.dumps(result, indent=2))

