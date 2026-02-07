package com.iitg.jobassessment.repository;

import com.iitg.jobassessment.entity.Application;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ApplicationRepository extends JpaRepository<Application, UUID> {
    List<Application> findByAssessmentId(UUID assessmentId);

    Optional<Application> findByAssessmentIdAndCandidateId(UUID assessmentId, UUID candidateId);

    List<Application> findByCandidateId(UUID candidateId);
}
