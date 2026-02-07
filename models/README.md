# AI Model Service

Python Flask service providing AI-powered features for the Job Assessment Platform.

## Features

- **Resume Matching**: Semantic matching between job descriptions and resumes
- **Assessment Generation**: AI-generated MCQ, SQL, and DSA questions
- **Assessment Scoring**: Automated scoring for all question types
- **PDF Parsing**: Extract text from PDF resumes
- **Code Execution**: Execute and test DSA solutions
- **JD Analysis**: Extract skills and requirements from job descriptions

## Quick Start

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Set API key
export GEMINI_API_KEY="your-api-key"

# Run service
python ai_service.py
```

### Deployment (Render)

See `DEPLOYMENT.md` for detailed instructions.

**Quick Deploy:**
1. Connect repository to Render
2. Set Root Directory: `models`
3. Build Command: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
4. Start Command: `bash start.sh`
5. Add `GEMINI_API_KEY` environment variable

## API Endpoints

- `GET /health` - Health check
- `POST /api/match-application` - Resume matching
- `POST /api/generate-assessment` - Generate assessment questions
- `POST /api/score-assessment` - Score assessment submissions
- `POST /api/parse-pdf` - Parse PDF resumes
- `POST /api/execute-code` - Execute DSA code
- `POST /api/analyze-jd` - Analyze job descriptions

## Dependencies

See `requirements.txt` for full list.

Key dependencies:
- Flask: Web framework
- sentence-transformers: Resume matching model
- google-generativeai: Assessment generation
- spacy: NLP for JD analysis
- pdfplumber: PDF parsing

## Project Structure

```
models/
├── ai_service.py              # Main Flask application
├── ai_resume_matcher.py       # Resume matching logic
├── assessment_generator.py     # Question generation
├── assessment_scorer.py       # Scoring logic
├── code_executor.py           # Code execution
├── jd_analyzer.py             # JD analysis
├── pdf_to_text.py            # PDF parsing
├── question_bank.py           # Question database
├── skills.py                  # Skills dictionary
├── sql_verifier.py            # SQL verification
├── multi_api_key_support.py   # API key rotation
├── dsa_engine/                # DSA question engine
│   ├── test_case_generator.py
│   └── reference_solvers/
├── tests/                     # Unit tests
├── requirements.txt           # Python dependencies
├── Procfile                   # Render deployment
├── render.yaml                # Render config
├── start.sh                   # Start script
└── README.md                  # This file
```

## Environment Variables

- `GEMINI_API_KEY`: Google Gemini API key (required)
- `GEMINI_API_KEY_2`: Secondary API key (optional)
- `PORT`: Service port (default: 5000)

## Testing

```bash
# Run tests
python -m pytest tests/

# Test specific module
python tests/test_assessment_generator.py
```

## Documentation

- `DEPLOYMENT.md` - Deployment guide
- `STEP_BY_STEP_DEPLOY.md` - Step-by-step deployment
- `QUICK_START_RENDER.md` - Quick deployment reference

