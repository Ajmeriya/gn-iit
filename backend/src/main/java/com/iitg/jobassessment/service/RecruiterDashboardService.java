package com.iitg.jobassessment.service;

import com.iitg.jobassessment.entity.Assessment;
import com.iitg.jobassessment.entity.AssessmentStatus;
import com.iitg.jobassessment.repository.ApplicationRepository;
import com.iitg.jobassessment.repository.AssessmentRepository;
import com.iitg.jobassessment.web.dto.recruiter.AssessmentSummary;
import com.iitg.jobassessment.web.dto.recruiter.DashboardStats;
import com.iitg.jobassessment.web.dto.recruiter.RecruiterDashboardResponse;
import java.util.List;
import org.springframework.stereotype.Service;

@Service
public class RecruiterDashboardService {
    private final AssessmentRepository assessmentRepository;
    private final ApplicationRepository applicationRepository;

    public RecruiterDashboardService(AssessmentRepository assessmentRepository,
                                     ApplicationRepository applicationRepository) {
        this.assessmentRepository = assessmentRepository;
        this.applicationRepository = applicationRepository;
    }

    public RecruiterDashboardResponse getDashboard() {
        List<Assessment> assessments = assessmentRepository.findAll();

        List<AssessmentSummary> summaries = assessments.stream()
            .map(assessment -> new AssessmentSummary(
                assessment.getId().toString(),
                assessment.getTitle(),
                assessment.getRole(),
                assessment.getStatus().name().toLowerCase(),
                assessment.getCreatedAt() != null ? assessment.getCreatedAt().toString() : null,
                applicationRepository.findByAssessmentId(assessment.getId()).size()
            ))
            .toList();

        int activeCount = (int) assessments.stream()
            .filter(assessment -> assessment.getStatus() == AssessmentStatus.ACTIVE)
            .count();

        int totalCandidates = summaries.stream()
            .mapToInt(AssessmentSummary::candidateCount)
            .sum();

        int topPerformers = 0;
        DashboardStats stats = new DashboardStats(activeCount, totalCandidates, topPerformers);
        return new RecruiterDashboardResponse(stats, summaries);
    }
}
