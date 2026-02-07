package com.iitg.jobassessment.entity;

import jakarta.persistence.Embeddable;

@Embeddable
public class TestCase {
    private String inputText;
    private String outputText;

    public String getInputText() {
        return inputText;
    }

    public void setInputText(String inputText) {
        this.inputText = inputText;
    }

    public String getOutputText() {
        return outputText;
    }

    public void setOutputText(String outputText) {
        this.outputText = outputText;
    }
}
