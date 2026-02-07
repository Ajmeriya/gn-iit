package com.iitg.jobassessment.web.dto.assessment;

import java.util.List;

public record ApplicationResponse(
    String id,
    String assessmentId,
    String candidateId,
    String name,
    String email,
    Integer experienceYears,
    List<String> skills,
    String resumeSummary,
    String resumeFileName,
    String status,
    Integer score,
    String createdAt
) {
}
