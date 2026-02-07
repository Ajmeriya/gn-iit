package com.iitg.jobassessment.web.dto.assessment;

import java.util.Map;
import java.util.List;

public record AssessmentSubmissionResponse(
    String assessmentId,
    String candidateId,
    List<Map<String, Object>> questions,
    Map<String, Object> answers,
    Integer score,
    String result,
    String submittedAt
) {
}
