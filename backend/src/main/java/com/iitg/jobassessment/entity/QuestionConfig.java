package com.iitg.jobassessment.entity;

import jakarta.persistence.Embeddable;

@Embeddable
public class QuestionConfig {
    private Integer mcqCount;
    private Integer mcqTimeMinutes;

    private Integer descriptiveCount;
    private Integer descriptiveTimeMinutes;

    private Integer dsaCount;
    private Integer dsaTimeMinutes;

    public Integer getMcqCount() {
        return mcqCount;
    }

    public void setMcqCount(Integer mcqCount) {
        this.mcqCount = mcqCount;
    }

    public Integer getMcqTimeMinutes() {
        return mcqTimeMinutes;
    }

    public void setMcqTimeMinutes(Integer mcqTimeMinutes) {
        this.mcqTimeMinutes = mcqTimeMinutes;
    }

    public Integer getDescriptiveCount() {
        return descriptiveCount;
    }

    public void setDescriptiveCount(Integer descriptiveCount) {
        this.descriptiveCount = descriptiveCount;
    }

    public Integer getDescriptiveTimeMinutes() {
        return descriptiveTimeMinutes;
    }

    public void setDescriptiveTimeMinutes(Integer descriptiveTimeMinutes) {
        this.descriptiveTimeMinutes = descriptiveTimeMinutes;
    }

    public Integer getDsaCount() {
        return dsaCount;
    }

    public void setDsaCount(Integer dsaCount) {
        this.dsaCount = dsaCount;
    }

    public Integer getDsaTimeMinutes() {
        return dsaTimeMinutes;
    }

    public void setDsaTimeMinutes(Integer dsaTimeMinutes) {
        this.dsaTimeMinutes = dsaTimeMinutes;
    }
}
