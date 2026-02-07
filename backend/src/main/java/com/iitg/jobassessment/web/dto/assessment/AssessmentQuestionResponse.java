package com.iitg.jobassessment.web.dto.assessment;

import java.util.List;

public record AssessmentQuestionResponse(
    String id,
    String type,
    String question,
    List<String> options,
    String correctAnswer,
    List<TestCaseResponse> testCases
) {
}
