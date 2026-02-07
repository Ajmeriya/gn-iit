export type AuthUser = {
  id: string;
  email: string;
  role: 'recruiter' | 'candidate';
  name: string;
};

const API_BASE_URL = (import.meta as any).env?.VITE_API_BASE_URL || 'http://localhost:8080';

const handleResponse = async (response: Response) => {
  if (response.ok) {
    return response.json();
  }

  let message = 'Request failed';
  try {
    const body = await response.json();
    if (body?.message) message = body.message;
  } catch {
    // ignore
  }

  throw new Error(message);
};

export const login = async (payload: { email: string; password: string }): Promise<AuthUser> => {
  const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  return handleResponse(response);
};

export const register = async (payload: { name: string; email: string; password: string; role: 'recruiter' | 'candidate' }): Promise<AuthUser> => {
  const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  return handleResponse(response);
};

export type RecruiterAssessmentSummary = {
  id: string;
  title: string;
  role: string;
  status: 'active' | 'draft' | 'closed';
  createdAt: string | null;
  candidateCount: number;
};

export type RecruiterDashboardStats = {
  activeAssessments: number;
  totalCandidates: number;
  topPerformers: number;
};

export type RecruiterDashboardResponse = {
  stats: RecruiterDashboardStats;
  assessments: RecruiterAssessmentSummary[];
};

export const getRecruiterDashboard = async (): Promise<RecruiterDashboardResponse> => {
  const response = await fetch(`${API_BASE_URL}/api/recruiter/dashboard`);
  return handleResponse(response);
};

export type CreateAssessmentPayload = {
  title: string;
  role: string;
  company: string;
  description?: string;
  duration: number;
  questions: number;
  questionConfig?: {
    mcqCount: number;
    mcqTimeMinutes: number;
    descriptiveCount: number;
    descriptiveTimeMinutes: number;
    dsaCount: number;
    dsaTimeMinutes: number;
  };
  requiredSkills: string[];
  minExperience: number;
  minMatchScore: number;
  includeInterview: boolean;
};

export const createAssessment = async (payload: CreateAssessmentPayload): Promise<{ id: string }> => {
  const response = await fetch(`${API_BASE_URL}/api/assessments`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  return handleResponse(response);
};

export type AssessmentDetails = {
  id: string;
  title: string;
  role: string;
  company: string;
  description?: string | null;
  status: 'active' | 'draft' | 'closed';
  duration: number;
  requiredSkills: string[];
  minExperience: number;
  minMatchScore: number;
  includeInterview: boolean;
  createdAt?: string | null;
};

export type AssessmentListItem = {
  id: string;
  title: string;
  role: string;
  company: string;
  status: 'active' | 'draft' | 'closed';
  duration: number;
  questions: number;
  includeInterview: boolean;
  createdAt?: string | null;
};

export type UpdateAssessmentPayload = {
  title?: string;
  role?: string;
  company?: string;
  description?: string;
  status?: 'active' | 'draft' | 'closed';
  duration?: number;
  requiredSkills?: string[];
  minExperience?: number;
  minMatchScore?: number;
  includeInterview?: boolean;
};

export type AssessmentApplication = {
  id: string;
  assessmentId: string;
  candidateId: string;
  name: string;
  email: string;
  experienceYears: number;
  skills: string[];
  resumeSummary?: string | null;
  resumeFileName?: string | null;
  status: 'shortlisted' | 'rejected';
  score: number;
  createdAt?: string | null;
};

export type AssessmentSubmission = {
  assessmentId: string;
  candidateId: string;
  questions: Array<Record<string, any>>;
  answers: Record<string, any>;
  score: number;
  result: 'passed' | 'failed';
  submittedAt?: string | null;
};

export const getAssessmentDetails = async (assessmentId: string): Promise<AssessmentDetails> => {
  const response = await fetch(`${API_BASE_URL}/api/assessments/${assessmentId}`);
  return handleResponse(response);
};

export const getAssessments = async (): Promise<AssessmentListItem[]> => {
  const response = await fetch(`${API_BASE_URL}/api/assessments`);
  return handleResponse(response);
};

export const updateAssessment = async (assessmentId: string, payload: UpdateAssessmentPayload): Promise<AssessmentDetails> => {
  const response = await fetch(`${API_BASE_URL}/api/assessments/${assessmentId}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  return handleResponse(response);
};

export const getAssessmentApplications = async (assessmentId: string): Promise<AssessmentApplication[]> => {
  const response = await fetch(`${API_BASE_URL}/api/assessments/${assessmentId}/applications`);
  return handleResponse(response);
};

export const getAssessmentSubmissions = async (assessmentId: string): Promise<AssessmentSubmission[]> => {
  const response = await fetch(`${API_BASE_URL}/api/assessments/${assessmentId}/submissions`);
  return handleResponse(response);
};

export const getCandidateApplications = async (candidateId: string): Promise<AssessmentApplication[]> => {
  const response = await fetch(`${API_BASE_URL}/api/candidates/${candidateId}/applications`);
  return handleResponse(response);
};

export const getCandidateAssessmentCompletions = async (candidateId: string): Promise<{ assessmentIds: string[] }> => {
  const response = await fetch(`${API_BASE_URL}/api/candidates/${candidateId}/assessment-completions`);
  return handleResponse(response);
};

export const getCandidateInterviewCompletions = async (candidateId: string): Promise<{ assessmentIds: string[] }> => {
  const response = await fetch(`${API_BASE_URL}/api/candidates/${candidateId}/interview-completions`);
  return handleResponse(response);
};

export type CandidateDashboardResponse = {
  assessments: AssessmentListItem[];
  applications: AssessmentApplication[];
  completedAssessmentIds: string[];
};

export const getCandidateDashboard = async (candidateId: string): Promise<CandidateDashboardResponse> => {
  const response = await fetch(`${API_BASE_URL}/api/candidates/${candidateId}/dashboard`);
  return handleResponse(response);
};

export type ApplyAssessmentPayload = {
  candidateId: string;
  name: string;
  email: string;
  experienceYears: number;
  skills: string[];
  resumeSummary?: string;
  resumeFileName?: string;
};

export const applyForAssessment = async (assessmentId: string, payload: ApplyAssessmentPayload): Promise<AssessmentApplication> => {
  const response = await fetch(`${API_BASE_URL}/api/assessments/${assessmentId}/applications`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  return handleResponse(response);
};

export type AssessmentQuestion = {
  id: string;
  type: 'mcq' | 'subjective' | 'coding';
  question: string;
  options?: string[];
  correctAnswer?: string | null;
  testCases?: Array<{ input: string; output: string }>;
};

export const getAssessmentQuestions = async (assessmentId: string): Promise<AssessmentQuestion[]> => {
  const response = await fetch(`${API_BASE_URL}/api/assessments/${assessmentId}/questions`);
  return handleResponse(response);
};

export const submitAssessment = async (assessmentId: string, payload: {
  candidateId: string;
  questions: Array<Record<string, any>>;
  answers: Record<string, any>;
}): Promise<AssessmentSubmission> => {
  const response = await fetch(`${API_BASE_URL}/api/assessments/${assessmentId}/submissions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  return handleResponse(response);
};

export const getAssessmentCompletion = async (assessmentId: string, candidateId: string): Promise<{ completed: boolean }> => {
  const response = await fetch(`${API_BASE_URL}/api/assessments/${assessmentId}/completions/${candidateId}`);
  return handleResponse(response);
};

export const markAssessmentCompletion = async (assessmentId: string, candidateId: string): Promise<{ completed: boolean }> => {
  const response = await fetch(`${API_BASE_URL}/api/assessments/${assessmentId}/completions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ candidateId })
  });
  return handleResponse(response);
};

export const getInterviewCompletion = async (assessmentId: string, candidateId: string): Promise<{ completed: boolean }> => {
  const response = await fetch(`${API_BASE_URL}/api/assessments/${assessmentId}/interview-completions/${candidateId}`);
  return handleResponse(response);
};

export const markInterviewCompletion = async (assessmentId: string, candidateId: string): Promise<{ completed: boolean }> => {
  const response = await fetch(`${API_BASE_URL}/api/assessments/${assessmentId}/interview-completions`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ candidateId })
  });
  return handleResponse(response);
};

export const getAssessmentApplication = async (assessmentId: string, candidateId: string): Promise<AssessmentApplication> => {
  const response = await fetch(`${API_BASE_URL}/api/assessments/${assessmentId}/applications/${candidateId}`);
  return handleResponse(response);
};

export const getAssessmentSubmission = async (assessmentId: string, candidateId: string): Promise<AssessmentSubmission> => {
  const response = await fetch(`${API_BASE_URL}/api/assessments/${assessmentId}/submissions/${candidateId}`);
  return handleResponse(response);
};

export type AssessmentAnalytics = {
  assessmentId: string;
  title: string;
  totalCandidates: number;
  averageScore: number;
  topScore: number;
  flaggedCount: number;
  scoreDistribution: Array<{ range: string; count: number }>;
  topCandidates: Array<{ rank: number; candidateId: string; name: string; email: string; score: number }>;
};

export const getAssessmentAnalytics = async (assessmentId: string): Promise<AssessmentAnalytics> => {
  const response = await fetch(`${API_BASE_URL}/api/assessments/${assessmentId}/analytics`);
  return handleResponse(response);
};
