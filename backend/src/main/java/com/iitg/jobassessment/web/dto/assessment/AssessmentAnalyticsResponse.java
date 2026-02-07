package com.iitg.jobassessment.web.dto.assessment;

import java.util.List;

public record AssessmentAnalyticsResponse(
    String assessmentId,
    String title,
    int totalCandidates,
    int averageScore,
    int topScore,
    int flaggedCount,
    List<ScoreDistributionEntry> scoreDistribution,
    List<TopCandidateEntry> topCandidates
) {
}
