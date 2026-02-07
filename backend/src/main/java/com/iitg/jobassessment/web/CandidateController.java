package com.iitg.jobassessment.web;

import com.iitg.jobassessment.entity.AssessmentCompletion;
import com.iitg.jobassessment.entity.InterviewCompletion;
import com.iitg.jobassessment.repository.ApplicationRepository;
import com.iitg.jobassessment.repository.AssessmentCompletionRepository;
import com.iitg.jobassessment.repository.InterviewCompletionRepository;
import com.iitg.jobassessment.repository.AssessmentRepository;
import com.iitg.jobassessment.web.dto.assessment.ApplicationResponse;
import com.iitg.jobassessment.web.dto.assessment.AssessmentListItemResponse;
import com.iitg.jobassessment.web.dto.candidate.CandidateCompletionsResponse;
import com.iitg.jobassessment.web.dto.candidate.CandidateDashboardResponse;
import java.util.List;
import java.util.Locale;
import java.util.UUID;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.http.HttpStatus;

@RestController
@RequestMapping("/api/candidates")
public class CandidateController {
    private final ApplicationRepository applicationRepository;
    private final AssessmentCompletionRepository assessmentCompletionRepository;
    private final InterviewCompletionRepository interviewCompletionRepository;
    private final AssessmentRepository assessmentRepository;

    public CandidateController(ApplicationRepository applicationRepository,
                               AssessmentCompletionRepository assessmentCompletionRepository,
                               InterviewCompletionRepository interviewCompletionRepository,
                               AssessmentRepository assessmentRepository) {
        this.applicationRepository = applicationRepository;
        this.assessmentCompletionRepository = assessmentCompletionRepository;
        this.interviewCompletionRepository = interviewCompletionRepository;
        this.assessmentRepository = assessmentRepository;
    }

    @GetMapping("/{candidateId}/dashboard")
    public ResponseEntity<CandidateDashboardResponse> getDashboard(@PathVariable String candidateId) {
        UUID id = parseId(candidateId);

        List<AssessmentListItemResponse> assessments = assessmentRepository.findAll().stream()
            .map(assessment -> new AssessmentListItemResponse(
                assessment.getId().toString(),
                assessment.getTitle(),
                assessment.getRole(),
                assessment.getCompany(),
                assessment.getStatus().name().toLowerCase(Locale.ROOT),
                assessment.getDuration(),
                assessment.getQuestions(),
                assessment.getIncludeInterview(),
                assessment.getCreatedAt() != null ? assessment.getCreatedAt().toString() : null
            ))
            .toList();

        List<ApplicationResponse> applications = applicationRepository.findByCandidateId(id)
            .stream()
            .map(application -> new ApplicationResponse(
                application.getId().toString(),
                application.getAssessment().getId().toString(),
                application.getCandidate().getId().toString(),
                application.getName(),
                application.getEmail(),
                application.getExperienceYears(),
                application.getSkills(),
                application.getResumeSummary(),
                application.getResumeFileName(),
                application.getStatus().name().toLowerCase(Locale.ROOT),
                application.getScore(),
                application.getCreatedAt() != null ? application.getCreatedAt().toString() : null
            ))
            .toList();

        List<String> completedAssessmentIds = assessmentCompletionRepository.findByCandidateId(id)
            .stream()
            .map(completion -> completion.getAssessment().getId().toString())
            .toList();

        return ResponseEntity.ok(new CandidateDashboardResponse(assessments, applications, completedAssessmentIds));
    }

    @GetMapping("/{candidateId}/applications")
    public ResponseEntity<List<ApplicationResponse>> getApplications(@PathVariable String candidateId) {
        UUID id = parseId(candidateId);
        List<ApplicationResponse> response = applicationRepository.findByCandidateId(id)
            .stream()
            .map(application -> new ApplicationResponse(
                application.getId().toString(),
                application.getAssessment().getId().toString(),
                application.getCandidate().getId().toString(),
                application.getName(),
                application.getEmail(),
                application.getExperienceYears(),
                application.getSkills(),
                application.getResumeSummary(),
                application.getResumeFileName(),
                application.getStatus().name().toLowerCase(Locale.ROOT),
                application.getScore(),
                application.getCreatedAt() != null ? application.getCreatedAt().toString() : null
            ))
            .toList();
        return ResponseEntity.ok(response);
    }

    @GetMapping("/{candidateId}/assessment-completions")
    public ResponseEntity<CandidateCompletionsResponse> getAssessmentCompletions(@PathVariable String candidateId) {
        UUID id = parseId(candidateId);
        List<String> assessmentIds = assessmentCompletionRepository.findByCandidateId(id)
            .stream()
            .map(AssessmentCompletion::getAssessment)
            .map(assessment -> assessment.getId().toString())
            .toList();
        return ResponseEntity.ok(new CandidateCompletionsResponse(assessmentIds));
    }

    @GetMapping("/{candidateId}/interview-completions")
    public ResponseEntity<CandidateCompletionsResponse> getInterviewCompletions(@PathVariable String candidateId) {
        UUID id = parseId(candidateId);
        List<String> assessmentIds = interviewCompletionRepository.findByCandidateId(id)
            .stream()
            .map(InterviewCompletion::getAssessment)
            .map(assessment -> assessment.getId().toString())
            .toList();
        return ResponseEntity.ok(new CandidateCompletionsResponse(assessmentIds));
    }

    private UUID parseId(String id) {
        try {
            return UUID.fromString(id);
        } catch (IllegalArgumentException ex) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Invalid id");
        }
    }
}
