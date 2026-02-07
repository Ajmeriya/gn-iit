"""
Backend Integration Example for Assessment Generator
Shows how to use the module in backend services (Flask, FastAPI, Spring Boot)
"""

from assessment_generator import generate_assessment, configure_gemini, DIFFICULTY_RANGE

# ============================================================================
# BACKEND INTEGRATION PATTERNS
# ============================================================================

def initialize_assessment_generator(api_key: str):
    """
    Initialize assessment generator at backend startup.
    Call this once when application starts.
    """
    configure_gemini(api_key)
    print("✅ Assessment Generator initialized")


# ============================================================================
# FLASK EXAMPLE
# ============================================================================

"""
from flask import Flask, request, jsonify
from assessment_generator import generate_assessment
import os

app = Flask(__name__)

# Initialize at startup
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
configure_gemini(GEMINI_API_KEY)

@app.route('/api/generate-assessment', methods=['POST'])
def generate_assessment_endpoint():
    try:
        config = request.json
        
        # Validate required fields
        required = ["experience_years", "experience_level", "difficulty", "sections"]
        for field in required:
            if field not in config:
                return jsonify({"error": f"Missing field: {field}"}), 400
        
        # Generate assessment
        result = generate_assessment(config, api_key=GEMINI_API_KEY)
        
        return jsonify(result), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500
"""

# ============================================================================
# FASTAPI EXAMPLE
# ============================================================================

"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from assessment_generator import generate_assessment
import os

app = FastAPI()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
configure_gemini(GEMINI_API_KEY)

class AssessmentConfig(BaseModel):
    experience_years: int
    experience_level: str
    difficulty: str
    sections: Dict

@app.post("/api/generate-assessment")
async def generate_assessment_endpoint(config: AssessmentConfig):
    try:
        result = generate_assessment(
            config.dict(),
            api_key=GEMINI_API_KEY
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
"""

# ============================================================================
# ERROR HANDLING EXAMPLE
# ============================================================================

def safe_generate_assessment(config: dict, api_key: str) -> dict:
    """
    Generate assessment with comprehensive error handling.
    Returns result with success status.
    """
    try:
        # Validate config structure
        if not isinstance(config, dict):
            return {"success": False, "error": "Config must be a dictionary"}
        
        # Generate assessment
        result = generate_assessment(config, api_key=api_key)
        
        return {"success": True, "data": result}
        
    except ValueError as e:
        return {"success": False, "error": f"Invalid configuration: {str(e)}"}
    except RuntimeError as e:
        return {"success": False, "error": f"Generation failed: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}


if __name__ == "__main__":
    # Example usage
    print("Backend Integration Examples for Assessment Generator")
    print("See code comments for Flask/FastAPI integration patterns")

