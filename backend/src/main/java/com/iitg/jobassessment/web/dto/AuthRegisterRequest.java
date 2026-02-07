package com.iitg.jobassessment.web.dto;

public record AuthRegisterRequest(String name, String email, String password, String role) {
}
