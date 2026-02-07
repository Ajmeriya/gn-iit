"""
AI Service - REST API for Backend Integration
Provides HTTP endpoints for AI models (Resume Matching, Assessment Generation, PDF Parsing)
"""

import os
import sys
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from typing import Optional

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import AI modules
try:
    from ai_resume_matcher import load_model, evaluate_application, get_model
    RESUME_MATCHER_AVAILABLE = True
except (ImportError, OSError, Exception) as e:
    print(f"Warning: ai_resume_matcher not available: {e}")
    print("Note: Resume matching will be disabled. Other services may still work.")
    RESUME_MATCHER_AVAILABLE = False
    load_model = None
    evaluate_application = None
    get_model = None

try:
    from assessment_generator import generate_assessment, configure_gemini
    ASSESSMENT_GENERATOR_AVAILABLE = True
except ImportError as e:
    print(f"Warning: assessment_generator not available: {e}")
    ASSESSMENT_GENERATOR_AVAILABLE = False

try:
    from pdf_to_text import extract_resume_text
    PDF_PARSER_AVAILABLE = True
except ImportError as e:
    print(f"Warning: pdf_to_text not available: {e}")
    PDF_PARSER_AVAILABLE = False

try:
    from code_executor import evaluate_dsa_solution
    CODE_EXECUTOR_AVAILABLE = True
except ImportError as e:
    print(f"Warning: code_executor not available: {e}")
    CODE_EXECUTOR_AVAILABLE = False

try:
    from jd_analyzer import analyze_job_description
    JD_ANALYZER_AVAILABLE = True
except ImportError as e:
    print(f"Warning: jd_analyzer not available: {e}")
    JD_ANALYZER_AVAILABLE = False

app = Flask(__name__)
CORS(app)  # Enable CORS for backend

# Global model cache
_model_cache = None

def get_or_load_model():
    """Get cached model or load it"""
    global _model_cache
    if _model_cache is None and RESUME_MATCHER_AVAILABLE and load_model is not None:
        try:
            print("Loading AI model...")
            _model_cache = load_model()
            print("✅ Model loaded successfully!")
        except Exception as e:
            print(f"Error loading model: {e}")
            print("Resume matching will be disabled.")
            return None
    return _model_cache


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "services": {
            "resume_matcher": RESUME_MATCHER_AVAILABLE,
            "assessment_generator": ASSESSMENT_GENERATOR_AVAILABLE,
            "pdf_parser": PDF_PARSER_AVAILABLE,
            "jd_analyzer": JD_ANALYZER_AVAILABLE
        }
    }), 200


@app.route('/api/match-application', methods=['POST'])
def match_application():
    """
    PRIMARY: Evaluate single candidate application (for Apply button)
    Returns: {shortlisted: bool, score: float, reason: str, threshold: float}
    """
    if not RESUME_MATCHER_AVAILABLE:
        return jsonify({"error": "Resume matcher not available"}), 503
    
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        jd_text = data.get('jd_text')
        resume_text = data.get('resume_text')
        min_score_threshold = data.get('min_score_threshold', 0.50)
        
        if not jd_text or not resume_text:
            return jsonify({"error": "jd_text and resume_text are required"}), 400
        
        # Convert threshold from 0-100 to 0-1 if needed
        # Backend sends threshold in 0-100 scale, but we also handle if it's already 0-1
        if min_score_threshold > 1.0:
            min_score_threshold = min_score_threshold / 100.0
        # Ensure threshold is in valid range [0, 1]
        min_score_threshold = max(0.0, min(1.0, min_score_threshold))
        
        # Get or load model
        model = get_or_load_model()
        if model is None:
            return jsonify({"error": "Failed to load AI model"}), 500
        
        # Evaluate application
        result = evaluate_application(
            jd_text=jd_text,
            resume_text=resume_text,
            min_score_threshold=min_score_threshold,
            model=model
        )
        
        # Convert score back to 0-100 scale for backend
        result['score'] = int(result['score'] * 100)
        result['threshold'] = int(result['threshold'] * 100)
        
        return jsonify(result), 200
        
    except ValueError as e:
        return jsonify({"error": f"Invalid input: {str(e)}"}), 400
    except Exception as e:
        print(f"Error in match_application: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Internal error: {str(e)}"}), 500


@app.route('/api/score-assessment', methods=['POST'])
def score_assessment_endpoint():
    """Score an assessment submission"""
    print(f"\n{'='*80}")
    print(f"RECEIVED ASSESSMENT SCORING REQUEST")
    print(f"{'='*80}")
    
    try:
        from assessment_scorer import score_assessment
        
        data = request.json
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        questions = data.get('questions', [])
        answers = data.get('answers', {})
        
        if not questions:
            return jsonify({"error": "Questions are required"}), 400
        
        print(f"Scoring {len(questions)} questions with {len(answers)} answers")
        
        result = score_assessment(questions, answers)
        
        print(f"Scoring complete. Overall score: {result['overall_score']}%")
        print(f"  MCQ: {result['mcq']['score']*100:.1f}% ({result['mcq']['correct']}/{result['mcq']['total']})")
        print(f"  SQL: {result['sql']['score']*100:.1f}% ({result['sql']['correct']}/{result['sql']['total']})")
        print(f"  DSA: {result['dsa']['score']*100:.1f}% ({result['dsa']['correct']}/{result['dsa']['total']})")
        
        return jsonify(result), 200
        
    except ImportError as e:
        print(f"ERROR: assessment_scorer not available: {e}")
        return jsonify({"error": "Assessment scorer not available"}), 503
    except Exception as e:
        print(f"Error in score_assessment_endpoint: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Internal error: {str(e)}"}), 500


@app.route('/api/generate-assessment', methods=['POST'])
def generate_assessment_endpoint():
    """
    Generate assessment questions (MCQ, Subjective, Coding)
    Returns: {mcq: [...], subjective: [...], coding: [...]}
    """
    print("\n" + "="*80)
    print("RECEIVED ASSESSMENT GENERATION REQUEST")
    print("="*80)
    
    if not ASSESSMENT_GENERATOR_AVAILABLE:
        print("ERROR: Assessment generator not available")
        return jsonify({"error": "Assessment generator not available"}), 503
    
    try:
        data = request.json
        if not data:
            print("ERROR: Request body is required")
            return jsonify({"error": "Request body is required"}), 400
        
        print(f"Request data keys: {list(data.keys()) if data else 'None'}")
        
        # Get API key from request or environment (supports multiple keys)
        api_key = data.get('api_key')
        
        # If not in request, try to use multi-key manager
        if not api_key:
            try:
                from multi_api_key_support import get_api_key_manager
                key_manager = get_api_key_manager()
                api_key = key_manager.get_current_key()
                if api_key:
                    status = key_manager.get_status()
                    print(f"Using API key manager: {status['available_keys']}/{status['total_keys']} keys available")
            except ImportError:
                # Fallback to single key
                api_key = os.getenv('GEMINI_API_KEY')
        
        if not api_key:
            print("ERROR: GEMINI_API_KEY is required")
            return jsonify({"error": "GEMINI_API_KEY is required"}), 400
        
        print(f"API Key provided: {'YES' if api_key else 'NO'}")
        if api_key:
            print(f"API Key length: {len(api_key)}")
        
        # Build config from request - support both flat format and sections format
        sections_data = data.get('sections', {})
        
        # Extract from sections structure if provided, otherwise use flat format
        if sections_data:
            mcq_section = sections_data.get('mcq', {})
            subj_section = sections_data.get('subjective', {})
            coding_section = sections_data.get('coding', {})
            
            config = {
                "experience_years": data.get('experience_years', 2),
                "experience_level": data.get('experience_level', 'Mid'),
                "difficulty": data.get('difficulty', 'Medium'),
                "sections": {
                    "mcq": {
                        "total_time_minutes": mcq_section.get('total_time_minutes', data.get('mcq_time_minutes', 20)),
                        "question_count": mcq_section.get('question_count', data.get('mcq_count', 15))
                    },
                    "subjective": {
                        "topic": subj_section.get('topic', 'SQL'),
                        "total_time_minutes": subj_section.get('total_time_minutes', data.get('descriptive_time_minutes', 30)),
                        "question_count": subj_section.get('question_count', data.get('descriptive_count', 10))
                    },
                    "coding": {
                        "topic": coding_section.get('topic', 'DSA'),
                        "total_time_minutes": coding_section.get('total_time_minutes', data.get('dsa_time_minutes', 120)),
                        "question_count": coding_section.get('question_count', data.get('dsa_count', 2))
                    }
                }
            }
        else:
            # Fallback to flat format
            config = {
                "experience_years": data.get('experience_years', 2),
                "experience_level": data.get('experience_level', 'Mid'),
                "difficulty": data.get('difficulty', 'Medium'),
                "sections": {
                    "mcq": {
                        "total_time_minutes": data.get('mcq_time_minutes', 20),
                        "question_count": data.get('mcq_count', 15)
                    },
                    "subjective": {
                        "topic": "SQL",
                        "total_time_minutes": data.get('descriptive_time_minutes', 30),
                        "question_count": data.get('descriptive_count', 10)
                    },
                    "coding": {
                        "topic": "DSA",
                        "total_time_minutes": data.get('dsa_time_minutes', 120),
                        "question_count": data.get('dsa_count', 2)
                    }
                }
            }
        
        print(f"Config structure: {json.dumps(config, indent=2)}")
        
        # Get job description (recruiter's requirements) for question matching
        job_description = data.get('job_description', '') or data.get('description', '') or data.get('jd_text', '')
        
        # Get resume text as fallback
        resume_text = data.get('resume_text', '') or data.get('resumeText', '')
        
        # Prioritize job description over resume for question selection
        if job_description:
            print(f"Job description provided for question matching ({len(job_description)} chars)")
            print("Questions will be selected based on recruiter's requirements")
        elif resume_text:
            print(f"Resume text provided for question matching ({len(resume_text)} chars)")
            print("Questions will be selected based on candidate's resume")
        else:
            print("No job description or resume provided - questions will be randomly selected")
        
        print("Calling generate_assessment()...")
        
        # Generate assessment with job description (recruiter requirements) for skill-based selection
        result = generate_assessment(config, api_key=api_key, resume_text=resume_text, job_description=job_description)
        
        print(f"Generation successful! Result keys: {list(result.keys()) if result else 'None'}")
        if result:
            mcq_count = len(result.get('mcq', []))
            subj_count = len(result.get('subjective', []))
            coding_count = len(result.get('coding', []))
            print(f"Generated: {mcq_count} MCQ, {subj_count} Subjective, {coding_count} Coding questions")
        
        print("="*80 + "\n")
        
        return jsonify(result), 200
        
    except Exception as e:
        error_msg = str(e)
        print(f"ERROR in generate_assessment_endpoint: {error_msg}")
        import traceback
        traceback.print_exc()
        print("="*80 + "\n")
        
        # Check if it's a quota exceeded error
        if "429" in error_msg or "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
            return jsonify({
                "error": "Gemini API quota exceeded",
                "message": "Free tier limit: 20 requests/day. Please wait 24 hours or upgrade your API plan.",
                "quota_exceeded": True,
                "details": error_msg
            }), 429
        else:
            return jsonify({"error": f"Internal error: {error_msg}"}), 500


@app.route('/api/parse-pdf', methods=['POST'])
def parse_pdf():
    """
    Extract text from PDF resume
    Accepts: multipart/form-data with 'file' field
    Returns: {text: str, success: bool}
    """
    if not PDF_PARSER_AVAILABLE:
        return jsonify({"error": "PDF parser not available"}), 503
    
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
        
        # Save temporarily
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
            file.save(tmp_file.name)
            tmp_path = tmp_file.name
        
        try:
            # Extract text
            text = extract_resume_text(tmp_path)
            
            if not text or len(text.strip()) < 10:
                return jsonify({"error": "Could not extract text from PDF"}), 400
            
            return jsonify({
                "text": text,
                "success": True
            }), 200
        finally:
            # Clean up temp file
            try:
                os.unlink(tmp_path)
            except:
                pass
        
    except Exception as e:
        print(f"Error in parse_pdf: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Internal error: {str(e)}"}), 500


@app.route('/api/execute-code', methods=['POST'])
def execute_code_endpoint():
    """Execute code and run test cases"""
    if not CODE_EXECUTOR_AVAILABLE:
        return jsonify({"error": "Code executor not available"}), 503
    
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        code = data.get('code')
        test_cases = data.get('test_cases', [])
        language = data.get('language', 'python')
        
        if not code:
            return jsonify({"error": "code is required"}), 400
        
        if not test_cases:
            return jsonify({"error": "test_cases are required"}), 400
        
        print(f"\n{'='*80}")
        print(f"EXECUTING CODE")
        print(f"{'='*80}")
        print(f"Language: {language}")
        print(f"Test cases: {len(test_cases)}")
        print(f"Code length: {len(code)} characters")
        
        result = evaluate_dsa_solution(code, test_cases, language)
        
        print(f"Result: {result['passed_tests']}/{result['total_tests']} passed")
        print(f"{'='*80}\n")
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"Error in execute_code: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Internal error: {str(e)}"}), 500


@app.route('/api/analyze-jd', methods=['POST'])
def analyze_jd_endpoint():
    """
    Analyze Job Description and extract structured data.
    Returns: {role, experience_level, experience_years, skills}
    """
    if not JD_ANALYZER_AVAILABLE:
        return jsonify({"error": "JD analyzer not available"}), 503
    
    try:
        data = request.json
        if not data:
            return jsonify({"error": "Request body is required"}), 400
        
        jd_text = data.get('job_description') or data.get('jd_text') or data.get('text')
        
        if not jd_text:
            return jsonify({"error": "job_description is required"}), 400
        
        if not isinstance(jd_text, str):
            return jsonify({"error": "job_description must be a string"}), 400
        
        print(f"\n{'='*80}")
        print(f"ANALYZING JOB DESCRIPTION")
        print(f"{'='*80}")
        print(f"JD length: {len(jd_text)} characters")
        
        result = analyze_job_description(jd_text)
        
        print(f"Extracted:")
        print(f"  Role: {result.get('role')}")
        print(f"  Experience: {result.get('experience_level')} ({result.get('experience_years')} years)")
        print(f"  Skills: {len(result.get('skills', []))} skills")
        print(f"{'='*80}\n")
        
        return jsonify(result), 200
        
    except Exception as e:
        print(f"Error in analyze_jd: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": f"Internal error: {str(e)}"}), 500


if __name__ == '__main__':
    # Load model at startup
    if RESUME_MATCHER_AVAILABLE:
        get_or_load_model()
    
    # Run server
    # Render sets PORT env var, fallback to AI_SERVICE_PORT or 5000
    port = int(os.getenv('PORT', os.getenv('AI_SERVICE_PORT', 5000)))
    print(f"🚀 Starting AI Service on port {port}")
    print(f"📊 Services available:")
    print(f"   - Resume Matcher: {RESUME_MATCHER_AVAILABLE}")
    print(f"   - Assessment Generator: {ASSESSMENT_GENERATOR_AVAILABLE}")
    print(f"   - PDF Parser: {PDF_PARSER_AVAILABLE}")
    print(f"   - Code Executor: {CODE_EXECUTOR_AVAILABLE}")
    print(f"   - JD Analyzer: {JD_ANALYZER_AVAILABLE}")
    print(f"\n🔗 Endpoints:")
    print(f"   - GET  /health")
    print(f"   - POST /api/match-application")
    print(f"   - POST /api/generate-assessment")
    print(f"   - POST /api/score-assessment")
    print(f"   - POST /api/parse-pdf")
    print(f"   - POST /api/execute-code")
    print(f"   - POST /api/analyze-jd")
    
    app.run(host='0.0.0.0', port=port, debug=False)

