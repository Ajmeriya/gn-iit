package com.iitg.jobassessment.web.dto.assessment;

import java.util.List;

public record CreateAssessmentRequest(
    String title,
    String role,
    String company,
    String description,
    Integer duration,
    Integer questions,
    QuestionConfigRequest questionConfig,
    List<String> requiredSkills,
    Integer minExperience,
    Integer minMatchScore,
    Boolean includeInterview
) {
}
