package com.iitg.jobassessment.web.dto.recruiter;

public record AssessmentSummary(
    String id,
    String title,
    String role,
    String status,
    String createdAt,
    int candidateCount
) {
}
