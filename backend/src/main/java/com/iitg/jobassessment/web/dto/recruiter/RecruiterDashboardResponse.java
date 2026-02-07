package com.iitg.jobassessment.web.dto.recruiter;

import java.util.List;

public record RecruiterDashboardResponse(DashboardStats stats, List<AssessmentSummary> assessments) {
}
