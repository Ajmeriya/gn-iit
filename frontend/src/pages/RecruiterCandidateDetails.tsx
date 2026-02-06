import { useNavigate, useParams } from 'react-router-dom';
import { ArrowLeft, FileText, LogOut, UserCircle, Zap } from 'lucide-react';
import ThemeToggle from '../components/ThemeToggle';
import { getApplicationsForAssessment, getAssessmentSubmissionForCandidate } from '../data/storage';

interface User {
  id: string;
  email: string;
  role: 'recruiter' | 'candidate';
  name: string;
}

interface RecruiterCandidateDetailsProps {
  user: User;
  onLogout: () => void;
}

export default function RecruiterCandidateDetails({ user, onLogout }: RecruiterCandidateDetailsProps) {
  const navigate = useNavigate();
  const { assessmentId, candidateId } = useParams();
  const candidates = assessmentId ? getApplicationsForAssessment(assessmentId) : [];
  const candidate = candidates.find(item => item.candidateId === candidateId);
  const submission = assessmentId && candidateId ? getAssessmentSubmissionForCandidate(assessmentId, candidateId) : undefined;

  const staticCandidates = {
    'static-shortlist-1': {
      name: 'Ishaan Verma',
      email: 'ishaan.verma@example.com',
      experienceYears: 3,
      skills: ['React', 'TypeScript', 'Tailwind'],
      resumeFileName: 'Ishaan_Verma_Resume.pdf',
      resumeSummary: 'Frontend developer with 3 years experience building performant React applications.'
    },
    'static-shortlist-2': {
      name: 'Nisha Rao',
      email: 'nisha.rao@example.com',
      experienceYears: 2,
      skills: ['Node.js', 'React', 'MongoDB'],
      resumeFileName: 'Nisha_Rao_Resume.pdf',
      resumeSummary: 'Full-stack engineer focused on MERN stack and API integrations.'
    },
    'static-shortlist-3': {
      name: 'Rahul Iyer',
      email: 'rahul.iyer@example.com',
      experienceYears: 4,
      skills: ['React', 'Redux', 'Jest'],
      resumeFileName: 'Rahul_Iyer_Resume.pdf',
      resumeSummary: 'Senior frontend engineer with strong testing and state management experience.'
    },
    'static-1': {
      name: 'Aarav Mehta',
      email: 'aarav.mehta@example.com',
      experienceYears: 3,
      skills: ['React', 'TypeScript', 'REST APIs'],
      resumeFileName: 'Aarav_Mehta_Resume.pdf',
      resumeSummary: 'React developer focused on scalable design systems.'
    },
    'static-2': {
      name: 'Diya Sharma',
      email: 'diya.sharma@example.com',
      experienceYears: 1,
      skills: ['HTML', 'CSS', 'JavaScript'],
      resumeFileName: 'Diya_Sharma_Resume.pdf',
      resumeSummary: 'Junior frontend developer with strong fundamentals.'
    },
    'static-3': {
      name: 'Kabir Patel',
      email: 'kabir.patel@example.com',
      experienceYears: 2,
      skills: ['React', 'Next.js', 'Tailwind'],
      resumeFileName: 'Kabir_Patel_Resume.pdf',
      resumeSummary: 'Frontend developer focused on fast, responsive web apps.'
    },
    'static-interview-1': {
      name: 'Neha Kapoor',
      email: 'neha.kapoor@example.com',
      experienceYears: 3,
      skills: ['React', 'Redux', 'TypeScript'],
      resumeFileName: 'Neha_Kapoor_Resume.pdf',
      resumeSummary: 'UI engineer with experience in scalable frontend systems.'
    },
    'static-interview-2': {
      name: 'Sahil Nair',
      email: 'sahil.nair@example.com',
      experienceYears: 1,
      skills: ['HTML', 'CSS', 'JavaScript'],
      resumeFileName: 'Sahil_Nair_Resume.pdf',
      resumeSummary: 'Entry-level developer with strong fundamentals.'
    },
    'static-interview-3': {
      name: 'Riya Sen',
      email: 'riya.sen@example.com',
      experienceYears: 2,
      skills: ['React', 'Node.js', 'MongoDB'],
      resumeFileName: 'Riya_Sen_Resume.pdf',
      resumeSummary: 'Full-stack developer with MERN experience.'
    }
  } as const;

  const staticSubmission = {
    questions: [
      {
        id: '1',
        type: 'mcq' as const,
        question: 'What is the purpose of React hooks?',
        options: [
          'To add state and lifecycle features to functional components',
          'To style React components',
          'To handle routing in React',
          'To manage API calls'
        ],
        correctAnswer: 'To add state and lifecycle features to functional components'
      },
      {
        id: '2',
        type: 'subjective' as const,
        question: 'Explain the concept of Virtual DOM in React and how it improves performance.'
      },
      {
        id: '3',
        type: 'coding' as const,
        question: 'Write a function that reverses a string without using built-in reverse methods.'
      }
    ],
    answers: {
      '1': 'To add state and lifecycle features to functional components',
      '2': 'Virtual DOM is a lightweight copy of the real DOM. React diffs changes and updates only necessary parts, improving performance.',
      '3': 'function reverseString(str){ let out=""; for(let i=str.length-1;i>=0;i--){ out+=str[i]; } return out; }'
    }
  };

  const staticInterviewSubmission = {
    result: candidateId === 'static-interview-2' ? 'failed' as const : 'passed' as const,
    score: candidateId === 'static-interview-2' ? 49 : 84,
    questions: [
      {
        id: 'i1',
        question: 'Tell me about a challenging project you worked on and how you handled it.'
      },
      {
        id: 'i2',
        question: 'How do you approach debugging a complex UI issue?'
      },
      {
        id: 'i3',
        question: 'Explain a time you had to collaborate with a difficult stakeholder.'
      }
    ],
    answers: {
      i1: 'I led a dashboard migration, identified bottlenecks, and broke work into incremental releases with testing.',
      i2: 'I isolate the issue, check state changes, and use browser devtools to track layout and event handlers.',
      i3: 'I set expectations early, documented requirements, and shared weekly progress updates to align.'
    }
  };

  const staticCandidate = candidateId ? staticCandidates[candidateId as keyof typeof staticCandidates] : undefined;
  const displayCandidate = candidate ?? (staticCandidate
    ? {
        id: candidateId || 'static',
        candidateId: candidateId || 'static',
        name: staticCandidate.name,
        email: staticCandidate.email,
        experienceYears: staticCandidate.experienceYears,
        skills: staticCandidate.skills,
        resumeFileName: staticCandidate.resumeFileName,
        resumeSummary: staticCandidate.resumeSummary,
        status: 'shortlisted' as const,
        score: 80,
        createdAt: new Date().toISOString()
      }
    : undefined);
  const isStaticShortlist = candidateId?.startsWith('static-shortlist');
  const isStaticInterview = candidateId?.startsWith('static-interview');
  const shouldUseStaticSubmission = Boolean(staticCandidate) && !isStaticShortlist && !isStaticInterview;
  const displaySubmission = submission ?? (shouldUseStaticSubmission ? {
    result: candidateId === 'static-2' ? 'failed' as const : 'passed' as const,
    score: candidateId === 'static-2' ? 54 : 82,
    questions: staticSubmission.questions,
    answers: staticSubmission.answers
  } : undefined);
  const displayInterviewSubmission = isStaticInterview ? staticInterviewSubmission : undefined;
  const displayAnswers = displaySubmission?.answers as Record<string, any> | undefined;
  const interviewAnswers = displayInterviewSubmission?.answers as Record<string, string> | undefined;

  if (!displayCandidate) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center px-6">
        <div className="bg-white border border-gray-100 rounded-2xl shadow-lg p-8 max-w-lg w-full text-center">
          <div className="text-2xl font-bold text-gray-900 mb-2">Candidate Not Found</div>
          <p className="text-gray-600 mb-6">We couldn't find the candidate details.</p>
          <button
            onClick={() => navigate(`/recruiter/assessment/${assessmentId}`)}
            className="px-6 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold transition"
          >
            Back to Assessment
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <button
              onClick={() => navigate(`/recruiter/assessment/${assessmentId}`)}
              className="text-gray-600 hover:text-gray-900 transition"
            >
              <ArrowLeft className="w-6 h-6" />
            </button>
            <div className="flex items-center space-x-2">
              <Zap className="w-8 h-8 text-blue-600" />
              <span className="text-2xl font-bold text-gray-900">HireIQ</span>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <ThemeToggle />
            <button
              onClick={() => navigate('/recruiter/profile')}
              className="text-gray-700 font-medium hover:text-blue-600 transition"
            >
              {user.name}
            </button>
            <button
              onClick={onLogout}
              className="flex items-center space-x-2 px-4 py-2 text-gray-700 hover:text-red-600 transition"
            >
              <LogOut className="w-5 h-5" />
              <span>Logout</span>
            </button>
          </div>
        </div>
      </nav>

      <div className="max-w-4xl mx-auto px-6 py-8">
        <div className="bg-white rounded-2xl shadow-md border border-gray-100 p-8">
          <div className="flex items-center space-x-3 mb-6">
            <UserCircle className="w-8 h-8 text-blue-600" />
            <div>
              <h1 className="text-2xl font-bold text-gray-900">{displayCandidate.name}</h1>
              <p className="text-gray-600">{displayCandidate.email}</p>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-6">
            <div>
              <div className="text-sm text-gray-600">Experience</div>
              <div className="text-lg font-semibold text-gray-900">{displayCandidate.experienceYears} years</div>
            </div>
            <div>
              <div className="text-sm text-gray-600">AI Result</div>
              <div className={`text-lg font-semibold ${displayCandidate.status === 'shortlisted' ? 'text-green-600' : 'text-red-600'}`}>
                {displayCandidate.status === 'shortlisted' ? 'Accepted' : 'Rejected'}
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Score</div>
              <div className="text-lg font-semibold text-gray-900">{displayCandidate.score}%</div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Applied On</div>
              <div className="text-lg font-semibold text-gray-900">{new Date(displayCandidate.createdAt).toLocaleDateString()}</div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Assessment Result</div>
              <div className={`text-lg font-semibold ${displaySubmission?.result === 'passed' ? 'text-green-600' : displaySubmission?.result === 'failed' ? 'text-red-600' : 'text-gray-400'}`}>
                {displaySubmission?.result ? displaySubmission.result : 'Not submitted'}
              </div>
            </div>
            <div>
              <div className="text-sm text-gray-600">Assessment Score</div>
              <div className="text-lg font-semibold text-gray-900">{displaySubmission ? `${displaySubmission.score}%` : '-'}</div>
            </div>
            {displayInterviewSubmission && (
              <>
                <div>
                  <div className="text-sm text-gray-600">AI Interview Result</div>
                  <div className={`text-lg font-semibold ${displayInterviewSubmission.result === 'passed' ? 'text-green-600' : 'text-red-600'}`}>
                    {displayInterviewSubmission.result}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-gray-600">AI Interview Score</div>
                  <div className="text-lg font-semibold text-gray-900">{displayInterviewSubmission.score}%</div>
                </div>
              </>
            )}
          </div>

          <div className="mt-6">
            <div className="text-sm text-gray-600 mb-2">Skills</div>
            <div className="flex flex-wrap gap-2">
              {displayCandidate.skills.map((skill) => (
                <span key={skill} className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-sm">
                  {skill}
                </span>
              ))}
            </div>
          </div>

          <div className="mt-6">
            <div className="flex items-center space-x-2 mb-2">
              <FileText className="w-5 h-5 text-blue-600" />
              <span className="text-sm font-semibold text-gray-700">Resume</span>
            </div>
            <div className="text-gray-700">{displayCandidate.resumeFileName || 'Not uploaded'}</div>
            {displayCandidate.resumeSummary && (
              <div className="mt-2 text-sm text-gray-600">{displayCandidate.resumeSummary}</div>
            )}
          </div>

          {displaySubmission && (
            <div className="mt-8">
              <div className="flex items-center space-x-2 mb-4">
                <FileText className="w-5 h-5 text-blue-600" />
                <span className="text-sm font-semibold text-gray-700">Assessment Responses</span>
              </div>
              <div className="space-y-4">
                {displaySubmission.questions.map((question, index) => (
                  <div key={question.id} className="border border-gray-200 rounded-xl p-4">
                    <div className="text-xs font-semibold text-gray-500 mb-1">Question {index + 1} · {question.type.toUpperCase()}</div>
                    <div className="text-gray-900 font-semibold mb-3">{question.question}</div>
                    <div className="bg-gray-50 rounded-lg p-3">
                      <div className="text-xs font-semibold text-gray-500 mb-2">Candidate Answer</div>
                      <div className="text-gray-800 whitespace-pre-wrap">
                        {displayAnswers?.[question.id] ? displayAnswers[question.id] : 'No answer provided.'}
                      </div>
                    </div>
                    {question.type === 'mcq' && question.options && (
                      <div className="mt-3 text-sm text-gray-600">
                        <div className="font-semibold text-gray-500 mb-1">Options</div>
                        <ul className="list-disc list-inside space-y-1">
                          {question.options.map((option) => (
                            <li key={option}>
                              {option}
                              {question.correctAnswer === option && (
                                <span className="ml-2 text-green-600 font-semibold">(Correct)</span>
                              )}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {displayInterviewSubmission && (
            <div className="mt-8">
              <div className="flex items-center space-x-2 mb-4">
                <FileText className="w-5 h-5 text-blue-600" />
                <span className="text-sm font-semibold text-gray-700">AI Interview Responses</span>
              </div>
              <div className="space-y-4">
                {displayInterviewSubmission.questions.map((question, index) => (
                  <div key={question.id} className="border border-gray-200 rounded-xl p-4">
                    <div className="text-xs font-semibold text-gray-500 mb-1">Question {index + 1}</div>
                    <div className="text-gray-900 font-semibold mb-3">{question.question}</div>
                    <div className="bg-gray-50 rounded-lg p-3">
                      <div className="text-xs font-semibold text-gray-500 mb-2">Candidate Answer</div>
                      <div className="text-gray-800 whitespace-pre-wrap">
                        {interviewAnswers?.[question.id] || 'No answer provided.'}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
