"""
Test script for Assessment Generator (Model-2B)
Tests question generation with Gemini API
"""

import json
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'AI-Powered-Job-Assessment-Screening-Platform', 'models'))

from assessment_generator import generate_assessment, DIFFICULTY_RANGE, EXPERIENCE_DEPTH

def test_assessment_generation():
    """Test assessment generation with sample configuration"""
    print("=" * 80)
    print("Assessment Generator - Model-2B Test")
    print("=" * 80)
    
    # Test configuration
    config = {
        "experience_years": 2,
        "experience_level": "Mid",
        "difficulty": "Medium",
        "sections": {
            "mcq": {
                "total_time_minutes": 20,
                "question_count": 15
            },
            "subjective": {
                "topic": "SQL",
                "total_time_minutes": 30,
                "question_count": 10
            },
            "coding": {
                "topic": "DSA",
                "total_time_minutes": 120,
                "question_count": 2
            }
        }
    }
    
    print("\n📋 Configuration:")
    print(json.dumps(config, indent=2))
    
    print("\n📊 Difficulty Range Logic:")
    print(f"Selected Difficulty: {config['difficulty']}")
    print(f"Allowed Difficulties: {DIFFICULTY_RANGE[config['difficulty']]}")
    
    print("\n👤 Experience Level:")
    print(f"Level: {config['experience_level']}")
    print(f"Focus: {EXPERIENCE_DEPTH[config['experience_level']]['focus']}")
    
    # Get API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        api_key = input("\nEnter Gemini API Key (or set GEMINI_API_KEY env var): ").strip()
    
    if not api_key:
        print("\n❌ API key required. Exiting.")
        return
    
    print("\n🤖 Generating assessment...")
    print("This may take a few moments...")
    
    try:
        result = generate_assessment(config, api_key=api_key)
        
        print("\n" + "=" * 80)
        print("✅ ASSESSMENT GENERATED SUCCESSFULLY!")
        print("=" * 80)
        
        # Display summary
        print(f"\n📊 Summary:")
        print(f"  MCQ Questions: {len(result['mcq'])}")
        print(f"  Subjective Questions: {len(result['subjective'])}")
        print(f"  Coding Problems: {len(result['coding'])}")
        
        # Validate time constraints
        mcq_time = sum(q.get("estimated_time", 0) for q in result["mcq"])
        subj_time = sum(q.get("estimated_time", 0) for q in result["subjective"])
        coding_time = sum(p.get("estimated_time", 0) for p in result["coding"])
        
        print(f"\n⏱️  Time Validation:")
        print(f"  MCQ: {mcq_time} / {config['sections']['mcq']['total_time_minutes']} minutes")
        print(f"  Subjective: {subj_time} / {config['sections']['subjective']['total_time_minutes']} minutes")
        print(f"  Coding: {coding_time} / {config['sections']['coding']['total_time_minutes']} minutes")
        
        # Validate difficulty ranges
        allowed = DIFFICULTY_RANGE[config["difficulty"]]
        print(f"\n🎯 Difficulty Validation:")
        mcq_diffs = [q.get("difficulty") for q in result["mcq"]]
        subj_diffs = [q.get("difficulty") for q in result["subjective"]]
        coding_diffs = [p.get("difficulty") for p in result["coding"]]
        
        all_valid = all(d in allowed for d in mcq_diffs + subj_diffs + coding_diffs)
        print(f"  All difficulties valid: {'✅' if all_valid else '❌'}")
        
        # Display full result
        print("\n" + "=" * 80)
        print("FULL RESULT (JSON):")
        print("=" * 80)
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_assessment_generation()

