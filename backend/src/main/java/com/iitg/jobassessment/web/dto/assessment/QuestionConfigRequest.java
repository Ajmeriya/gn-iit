package com.iitg.jobassessment.web.dto.assessment;

public record QuestionConfigRequest(
    Integer mcqCount,
    Integer mcqTimeMinutes,
    Integer descriptiveCount,
    Integer descriptiveTimeMinutes,
    Integer dsaCount,
    Integer dsaTimeMinutes
) {
}
