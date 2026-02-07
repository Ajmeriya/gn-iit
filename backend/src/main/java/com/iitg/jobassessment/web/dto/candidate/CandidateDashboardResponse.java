package com.iitg.jobassessment.web.dto.candidate;

import com.iitg.jobassessment.web.dto.assessment.ApplicationResponse;
import com.iitg.jobassessment.web.dto.assessment.AssessmentListItemResponse;
import java.util.List;

public record CandidateDashboardResponse(
    List<AssessmentListItemResponse> assessments,
    List<ApplicationResponse> applications,
    List<String> completedAssessmentIds
) {
}
