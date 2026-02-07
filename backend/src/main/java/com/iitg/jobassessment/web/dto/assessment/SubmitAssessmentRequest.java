package com.iitg.jobassessment.web.dto.assessment;

import java.util.List;
import java.util.Map;

public record SubmitAssessmentRequest(
    String candidateId,
    List<Map<String, Object>> questions,
    Map<String, Object> answers
) {
}
