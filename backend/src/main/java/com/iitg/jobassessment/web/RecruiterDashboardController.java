package com.iitg.jobassessment.web;

import com.iitg.jobassessment.entity.Assessment;
import com.iitg.jobassessment.entity.AssessmentStatus;
import com.iitg.jobassessment.repository.ApplicationRepository;
import com.iitg.jobassessment.repository.AssessmentRepository;
import com.iitg.jobassessment.web.dto.recruiter.AssessmentSummary;
import com.iitg.jobassessment.web.dto.recruiter.DashboardStats;
import com.iitg.jobassessment.web.dto.recruiter.RecruiterDashboardResponse;
import java.util.List;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/recruiter")
public class RecruiterDashboardController {
    private final AssessmentRepository assessmentRepository;
    private final ApplicationRepository applicationRepository;

    public RecruiterDashboardController(AssessmentRepository assessmentRepository,
                                        ApplicationRepository applicationRepository) {
        this.assessmentRepository = assessmentRepository;
        this.applicationRepository = applicationRepository;
    }

    @GetMapping("/dashboard")
    public ResponseEntity<RecruiterDashboardResponse> dashboard() {
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
        return ResponseEntity.ok(new RecruiterDashboardResponse(stats, summaries));
    }
}
