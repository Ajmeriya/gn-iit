package com.iitg.jobassessment.repository;

import com.iitg.jobassessment.entity.AssessmentCompletion;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

public interface AssessmentCompletionRepository extends JpaRepository<AssessmentCompletion, UUID> {
    List<AssessmentCompletion> findByAssessmentId(UUID assessmentId);

    Optional<AssessmentCompletion> findByAssessmentIdAndCandidateId(UUID assessmentId, UUID candidateId);

    List<AssessmentCompletion> findByCandidateId(UUID candidateId);
}
