package com.iitg.jobassessment.web.dto.assessment;

import java.util.List;

public record ApplyAssessmentRequest(
    String candidateId,
    String name,
    String email,
    Integer experienceYears,
    List<String> skills,
    String resumeSummary,
    String resumeFileName
) {
}
