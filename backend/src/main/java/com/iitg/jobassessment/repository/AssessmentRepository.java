package com.iitg.jobassessment.repository;

import com.iitg.jobassessment.entity.Assessment;
import com.iitg.jobassessment.entity.AssessmentStatus;
import java.util.List;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

public interface AssessmentRepository extends JpaRepository<Assessment, UUID> {
    List<Assessment> findByStatus(AssessmentStatus status);
}
