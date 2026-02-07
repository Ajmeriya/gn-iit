"""
Job Description Analyzer Module
Fully local, deterministic, offline JD analysis using spaCy and regex.
No API keys or paid services required.
"""

import re
from typing import Dict, List, Optional, Tuple
from collections import Counter

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

from skills import SKILLS, ROLE_MAP, SKILL_NORMALIZATION


def normalize_skill(skill: str) -> str:
    """
    Normalize skill name to standard form.
    
    Args:
        skill: Raw skill string
        
    Returns:
        Normalized skill name
    """
    skill_lower = skill.lower().strip()
    return SKILL_NORMALIZATION.get(skill_lower, skill.strip())


def extract_skills(jd_text: str) -> List[str]:
    """
    Extract skills from job description using dictionary matching.
    
    Args:
        jd_text: Raw job description text
        
    Returns:
        List of normalized, unique skills ordered by frequency
    """
    if not jd_text or not isinstance(jd_text, str):
        return []
    
    jd_lower = jd_text.lower()
    found_skills = []
    
    # Match skills case-insensitively
    for skill in SKILLS:
        skill_lower = skill.lower()
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(skill_lower) + r'\b'
        matches = re.findall(pattern, jd_lower, re.IGNORECASE)
        if matches:
            # Count occurrences for relevance ranking
            found_skills.extend([skill] * len(matches))
    
    # Count frequency and normalize
    skill_counter = Counter(found_skills)
    
    # Normalize and deduplicate
    normalized_skills = {}
    for skill, count in skill_counter.items():
        normalized = normalize_skill(skill)
        # Keep the highest count if duplicate after normalization
        if normalized not in normalized_skills or skill_counter[skill] > normalized_skills[normalized][1]:
            normalized_skills[normalized] = (normalized, count)
    
    # Sort by frequency (descending), then alphabetically
    sorted_skills = sorted(
        normalized_skills.values(),
        key=lambda x: (-x[1], x[0])
    )
    
    return [skill for skill, _ in sorted_skills]


def extract_experience(jd_text: str) -> Tuple[Optional[str], Optional[int]]:
    """
    Extract experience level and years from job description.
    
    Args:
        jd_text: Raw job description text
        
    Returns:
        Tuple of (experience_level, experience_years)
        experience_level: "Junior" | "Mid" | "Senior" | None
        experience_years: int | None
    """
    if not jd_text or not isinstance(jd_text, str):
        return None, None
    
    jd_lower = jd_text.lower()
    
    # Regex patterns for years extraction
    # Matches: "5 years", "5+ years", "5-7 years", "minimum 5 years", etc.
    patterns = [
        r'(\d+)\s*\+\s*years?',  # "5+ years", "5+ years of"
        r'(\d+)\s*-\s*(\d+)\s*years?',  # "3-5 years"
        r'(\d+)\s*years?',  # "5 years", "5 years of"
        r'minimum\s+(\d+)\s*years?',  # "minimum 5 years"
        r'at\s+least\s+(\d+)\s*years?',  # "at least 5 years"
        r'(\d+)\s*yr',  # "5 yr"
        r'(\d+)\s*yrs',  # "5 yrs"
    ]
    
    years_found = []
    
    for pattern in patterns:
        matches = re.finditer(pattern, jd_lower, re.IGNORECASE)
        for match in matches:
            # For range patterns (e.g., "3-5 years"), take the average
            if len(match.groups()) == 2:
                min_years = int(match.group(1))
                max_years = int(match.group(2))
                avg_years = (min_years + max_years) // 2
                years_found.append(avg_years)
            else:
                years_found.append(int(match.group(1)))
    
    if not years_found:
        return None, None
    
    # Take the maximum years mentioned (most conservative)
    experience_years = max(years_found)
    
    # Map years to level
    if experience_years <= 2:
        experience_level = "Junior"
    elif experience_years <= 4:
        experience_level = "Mid"
    else:  # >= 5
        experience_level = "Senior"
    
    return experience_level, experience_years


def extract_role(jd_text: str) -> str:
    """
    Extract role from job description using keyword mapping.
    
    Args:
        jd_text: Raw job description text
        
    Returns:
        Detected role string (default: "Software Developer")
    """
    if not jd_text or not isinstance(jd_text, str):
        return "Software Developer"
    
    jd_lower = jd_text.lower()
    
    # Check role mappings in order (more specific first)
    for keywords, role in ROLE_MAP:
        if not keywords:  # Default fallback
            continue
        
        for keyword in keywords:
            # Use word boundaries for exact matches
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, jd_lower, re.IGNORECASE):
                return role
    
    # Default fallback
    return "Software Developer"


def analyze_job_description(jd_text: str) -> Dict[str, any]:
    """
    Main function to analyze job description and extract structured data.
    
    Args:
        jd_text: Raw job description text (string)
        
    Returns:
        Dictionary with keys:
        - role: string
        - experience_level: "Junior" | "Mid" | "Senior" | null
        - experience_years: number | null
        - skills: string[]
        
    Example:
        >>> result = analyze_job_description("Java developer with 5 years experience...")
        >>> {
        ...     "role": "Java Developer",
        ...     "experience_level": "Senior",
        ...     "experience_years": 5,
        ...     "skills": ["Java", "Spring Boot", ...]
        ... }
    """
    # Input validation
    if not jd_text:
        return {
            "role": "Software Developer",
            "experience_level": None,
            "experience_years": None,
            "skills": []
        }
    
    if not isinstance(jd_text, str):
        jd_text = str(jd_text)
    
    # Extract components
    skills = extract_skills(jd_text)
    experience_level, experience_years = extract_experience(jd_text)
    role = extract_role(jd_text)
    
    # Build result
    result = {
        "role": role,
        "experience_level": experience_level,
        "experience_years": experience_years,
        "skills": skills
    }
    
    return result


# Backend integration helper (for FastAPI/Spring Boot)
def analyze_jd_for_backend(jd_text: str) -> Dict[str, any]:
    """
    Wrapper function optimized for backend API calls.
    Includes error handling and validation.
    
    Args:
        jd_text: Raw job description text
        
    Returns:
        Analysis result dictionary (JSON-compatible)
    """
    try:
        return analyze_job_description(jd_text)
    except Exception:
        # Return safe default on any error
        return {
            "role": "Software Developer",
            "experience_level": None,
            "experience_years": None,
            "skills": []
        }

