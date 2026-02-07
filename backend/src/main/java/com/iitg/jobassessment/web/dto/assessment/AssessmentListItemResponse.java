package com.iitg.jobassessment.web.dto.assessment;

public record AssessmentListItemResponse(
    String id,
    String title,
    String role,
    String company,
    String status,
    Integer duration,
    Integer questions,
    Boolean includeInterview,
    String createdAt
) {
}
