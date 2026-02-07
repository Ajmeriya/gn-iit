package com.iitg.jobassessment.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.client.RestClientException;
import org.springframework.web.multipart.MultipartFile;

import java.util.*;

/**
 * Service for calling Python AI models via REST API
 * Provides fallback to simple matching if AI service is unavailable
 */
@Service
public class AIService {
    
    private final RestTemplate restTemplate;
    
    @Value("${ai.service.url:http://localhost:5000}")
    private String aiServiceUrl;
    
    @Value("${ai.service.enabled:true}")
    private boolean aiServiceEnabled;
    
    public AIService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }
    
    /**
     * Check if AI service is available
     */
    public boolean isServiceAvailable() {
        if (!aiServiceEnabled) {
            return false;
        }
        try {
            String url = aiServiceUrl + "/health";
            @SuppressWarnings("rawtypes")
            ResponseEntity<Map> response = restTemplate.getForEntity(url, Map.class);
            return response.getStatusCode().is2xxSuccessful();
        } catch (Exception e) {
            System.out.println("AI Service not available: " + e.getMessage());
            return false;
        }
    }
    
    /**
     * Evaluate candidate application using AI resume matcher
     * Returns: {shortlisted: bool, score: int (0-100), reason: str, threshold: int}
     * Falls back to simple matching if AI service unavailable
     */
    public Map<String, Object> evaluateApplication(
            String jdText, 
            String resumeText, 
            int minScoreThreshold
    ) {
        if (!aiServiceEnabled || !isServiceAvailable()) {
            // Fallback to simple matching
            return fallbackSimpleMatching(jdText, resumeText, minScoreThreshold);
        }
        
        try {
            String url = aiServiceUrl + "/api/match-application";
            
            Map<String, Object> request = new HashMap<>();
            request.put("jd_text", jdText);
            request.put("resume_text", resumeText);
            request.put("min_score_threshold", minScoreThreshold / 100.0); // Convert to 0-1
            
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(request, headers);
            
            @SuppressWarnings("rawtypes")
            ResponseEntity<Map> response = restTemplate.postForEntity(url, entity, Map.class);
            
            if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                @SuppressWarnings("unchecked")
                Map<String, Object> result = (Map<String, Object>) response.getBody();
                // Ensure score is int (0-100)
                if (result.containsKey("score")) {
                    Object score = result.get("score");
                    if (score instanceof Double) {
                        result.put("score", ((Double) score).intValue());
                    } else if (score instanceof Integer) {
                        // Already int
                    } else {
                        result.put("score", (int) Math.round(((Number) score).doubleValue()));
                    }
                }
                return result;
            }
        } catch (RestClientException e) {
            System.out.println("AI Service call failed, using fallback: " + e.getMessage());
        } catch (Exception e) {
            System.out.println("Error calling AI service: " + e.getMessage());
        }
        
        // Fallback to simple matching
        return fallbackSimpleMatching(jdText, resumeText, minScoreThreshold);
    }
    
    /**
     * Generate assessment questions using AI
     * Returns: {mcq: [...], subjective: [...], coding: [...]}
     */
    public Map<String, Object> generateAssessment(Map<String, Object> config) {
        if (!aiServiceEnabled || !isServiceAvailable()) {
            throw new RuntimeException("AI service not available for assessment generation");
        }
        
        try {
            String url = aiServiceUrl + "/api/generate-assessment";
            
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(config, headers);
            
            @SuppressWarnings("rawtypes")
            ResponseEntity<Map> response = restTemplate.postForEntity(url, entity, Map.class);
            
            if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                @SuppressWarnings("unchecked")
                Map<String, Object> result = (Map<String, Object>) response.getBody();
                return result;
            }
            
            // Check if it's a 429 (quota exceeded) - return empty map to trigger fallback
            if (response.getStatusCode().value() == 429) {
                System.out.println("⚠️  Received 429 (Quota Exceeded) from AI service - will use fallback");
                throw new RuntimeException("Gemini API quota exceeded - using fallback questions");
            }
            
            throw new RuntimeException("Failed to generate assessment");
        } catch (org.springframework.web.client.HttpClientErrorException e) {
            // Handle HTTP errors (including 429)
            if (e.getStatusCode() != null && e.getStatusCode().value() == 429) {
                System.out.println("⚠️  HTTP 429 (Quota Exceeded) from AI service - will use fallback");
                throw new RuntimeException("Gemini API quota exceeded - using fallback questions");
            }
            throw new RuntimeException("AI service HTTP error: " + e.getMessage(), e);
        } catch (RestClientException e) {
            throw new RuntimeException("AI service error: " + e.getMessage(), e);
        }
    }
    
    /**
     * Score assessment submission
     * Returns: {overall_score: float, mcq: {...}, sql: {...}, dsa: {...}}
     */
    public Map<String, Object> scoreAssessment(Map<String, Object> request) {
        if (!aiServiceEnabled || !isServiceAvailable()) {
            throw new RuntimeException("AI service not available for assessment scoring");
        }
        
        try {
            String url = aiServiceUrl + "/api/score-assessment";
            
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(request, headers);
            
            @SuppressWarnings("rawtypes")
            ResponseEntity<Map> response = restTemplate.postForEntity(url, entity, Map.class);
            
            if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                @SuppressWarnings("unchecked")
                Map<String, Object> result = (Map<String, Object>) response.getBody();
                return result;
            }
            
            throw new RuntimeException("Failed to score assessment");
        } catch (RestClientException e) {
            throw new RuntimeException("AI service error: " + e.getMessage(), e);
        }
    }
    
    /**
     * Parse PDF resume to text
     */
    public String parsePdfResume(MultipartFile file) {
        if (!aiServiceEnabled || !isServiceAvailable()) {
            throw new RuntimeException("AI service not available for PDF parsing");
        }
        
        // Note: PDF parsing via REST requires proper multipart handling
        // This is a placeholder - implement with MultipartHttpServletRequest or similar
        throw new RuntimeException("PDF parsing via REST not fully implemented - use direct Python call");
    }
    
    /**
     * Fallback simple matching algorithm (original implementation)
     */
    private Map<String, Object> fallbackSimpleMatching(
            String jdText, 
            String resumeText, 
            int minScoreThreshold
    ) {
        // Simple keyword matching fallback
        String jdLower = jdText.toLowerCase();
        String resumeLower = resumeText.toLowerCase();
        
        // Count matching words (simple approach)
        String[] jdWords = jdLower.split("\\s+");
        Set<String> jdWordSet = new HashSet<>(Arrays.asList(jdWords));
        
        String[] resumeWords = resumeLower.split("\\s+");
        int matches = 0;
        for (String word : resumeWords) {
            if (word.length() > 3 && jdWordSet.contains(word)) {
                matches++;
            }
        }
        
        // Simple score calculation
        int score = Math.min(100, (matches * 10));
        boolean shortlisted = score >= minScoreThreshold;
        
        Map<String, Object> result = new HashMap<>();
        result.put("shortlisted", shortlisted);
        result.put("score", score);
        result.put("reason", shortlisted 
            ? "Resume matches job requirements" 
            : "Resume does not meet minimum score threshold");
        result.put("threshold", minScoreThreshold);
        result.put("fallback", true); // Indicate this is fallback
        
        return result;
    }
    
    /**
     * Execute code and run test cases
     * Returns: {total_tests: int, passed_tests: int, failed_tests: int, score: float, results: []}
     */
    public Map<String, Object> executeCode(Map<String, Object> request) {
        if (!aiServiceEnabled || !isServiceAvailable()) {
            throw new RuntimeException("AI service not available for code execution");
        }
        
        try {
            String url = aiServiceUrl + "/api/execute-code";
            
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(request, headers);
            
            @SuppressWarnings("rawtypes")
            ResponseEntity<Map> response = restTemplate.postForEntity(url, entity, Map.class);
            
            if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                @SuppressWarnings("unchecked")
                Map<String, Object> result = (Map<String, Object>) response.getBody();
                return result;
            }
            
            throw new RuntimeException("Failed to execute code");
        } catch (RestClientException e) {
            throw new RuntimeException("AI service error: " + e.getMessage(), e);
        }
    }
    
    /**
     * Analyze Job Description and extract structured data
     * Returns: {role: string, experience_level: string, experience_years: number, skills: string[]}
     */
    public Map<String, Object> analyzeJobDescription(String jobDescription) {
        if (!aiServiceEnabled || !isServiceAvailable()) {
            // Return default fallback
            Map<String, Object> fallback = new HashMap<>();
            fallback.put("role", "Software Developer");
            fallback.put("experience_level", null);
            fallback.put("experience_years", null);
            fallback.put("skills", new ArrayList<>());
            fallback.put("fallback", true);
            return fallback;
        }
        
        try {
            String url = aiServiceUrl + "/api/analyze-jd";
            
            Map<String, Object> request = new HashMap<>();
            request.put("job_description", jobDescription);
            
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(request, headers);
            
            @SuppressWarnings("rawtypes")
            ResponseEntity<Map> response = restTemplate.postForEntity(url, entity, Map.class);
            
            if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                @SuppressWarnings("unchecked")
                Map<String, Object> result = (Map<String, Object>) response.getBody();
                return result;
            }
            
            throw new RuntimeException("Failed to analyze job description");
        } catch (RestClientException e) {
            System.out.println("AI service error for JD analysis: " + e.getMessage());
            // Return fallback on error
            Map<String, Object> fallback = new HashMap<>();
            fallback.put("role", "Software Developer");
            fallback.put("experience_level", null);
            fallback.put("experience_years", null);
            fallback.put("skills", new ArrayList<>());
            fallback.put("fallback", true);
            return fallback;
        }
    }
}

