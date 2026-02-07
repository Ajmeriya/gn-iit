package com.iitg.jobassessment.repository;

import com.iitg.jobassessment.entity.AssessmentSubmission;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

public interface AssessmentSubmissionRepository extends JpaRepository<AssessmentSubmission, UUID> {
    List<AssessmentSubmission> findByAssessmentId(UUID assessmentId);

    Optional<AssessmentSubmission> findByAssessmentIdAndCandidateId(UUID assessmentId, UUID candidateId);

    List<AssessmentSubmission> findByCandidateId(UUID candidateId);
}
