package com.iitg.jobassessment.repository;

import com.iitg.jobassessment.entity.InterviewCompletion;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

public interface InterviewCompletionRepository extends JpaRepository<InterviewCompletion, UUID> {
    List<InterviewCompletion> findByAssessmentId(UUID assessmentId);

    Optional<InterviewCompletion> findByAssessmentIdAndCandidateId(UUID assessmentId, UUID candidateId);

    List<InterviewCompletion> findByCandidateId(UUID candidateId);
}
