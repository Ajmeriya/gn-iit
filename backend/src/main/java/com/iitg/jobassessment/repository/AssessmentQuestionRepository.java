package com.iitg.jobassessment.repository;

import com.iitg.jobassessment.entity.AssessmentQuestion;
import java.util.List;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

public interface AssessmentQuestionRepository extends JpaRepository<AssessmentQuestion, UUID> {
    List<AssessmentQuestion> findByAssessmentId(UUID assessmentId);
}
