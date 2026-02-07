package com.iitg.jobassessment.web.dto.assessment;

import java.util.List;

public record AssessmentDetailsResponse(
    String id,
    String title,
    String role,
    String company,
    String description,
    String status,
    Integer duration,
    List<String> requiredSkills,
    Integer minExperience,
    Integer minMatchScore,
    Boolean includeInterview,
    String createdAt
) {
}
