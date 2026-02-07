import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Landing from './pages/Landing';
import Login from './pages/Login';
import Signup from './pages/Signup';
import RecruiterDashboard from './pages/RecruiterDashboard';
import CandidateDashboard from './pages/CandidateDashboard';
import CreateAssessment from './pages/CreateAssessment';
import RecruiterAssessmentDetails from './pages/RecruiterAssessmentDetails';
import RecruiterCandidateDetails from './pages/RecruiterCandidateDetails';
import ApplyAssessment from './pages/ApplyAssessment';
import AssessmentDetails from './pages/AssessmentDetails';
import TakeAssessment from './pages/TakeAssessment';
import Interview from './pages/Interview';
import Results from './pages/Results';
import Leaderboard from './pages/Leaderboard';
import RecruiterProfile from './pages/RecruiterProfile';
import CandidateProfile from './pages/CandidateProfile';

interface User {
  id: string;
  email: string;
  role: 'recruiter' | 'candidate';
  name: string;
}

function App() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  const handleLogin = (userData: User) => {
    setUser(userData);
    localStorage.setItem('user', JSON.stringify(userData));
  };

  const handleUserUpdate = (updates: Partial<User>) => {
    setUser(prev => {
      if (!prev) return prev;
      const updated = { ...prev, ...updates };
      localStorage.setItem('user', JSON.stringify(updated));
      return updated;
    });
  };

  const handleLogout = () => {
    setUser(null);
    localStorage.removeItem('user');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-pulse text-gray-600">Loading...</div>
      </div>
    );
  }

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={user ? <Navigate to={user.role === 'recruiter' ? '/recruiter' : '/candidate'} /> : <Login onLogin={handleLogin} />} />
        <Route path="/signup" element={user ? <Navigate to={user.role === 'recruiter' ? '/recruiter' : '/candidate'} /> : <Signup onLogin={handleLogin} />} />

        <Route path="/recruiter" element={user?.role === 'recruiter' ? <RecruiterDashboard user={user} onLogout={handleLogout} /> : <Navigate to="/login" />} />
        <Route path="/recruiter/create" element={user?.role === 'recruiter' ? <CreateAssessment user={user} onLogout={handleLogout} /> : <Navigate to="/login" />} />
        <Route path="/recruiter/assessment/:assessmentId" element={user?.role === 'recruiter' ? <RecruiterAssessmentDetails user={user} onLogout={handleLogout} /> : <Navigate to="/login" />} />
        <Route path="/recruiter/assessment/:assessmentId/candidate/:candidateId" element={user?.role === 'recruiter' ? <RecruiterCandidateDetails user={user} onLogout={handleLogout} /> : <Navigate to="/login" />} />
        <Route path="/recruiter/results/:assessmentId" element={user?.role === 'recruiter' ? <Results user={user} onLogout={handleLogout} /> : <Navigate to="/login" />} />
        <Route path="/recruiter/leaderboard/:assessmentId" element={user?.role === 'recruiter' ? <Leaderboard user={user} onLogout={handleLogout} /> : <Navigate to="/login" />} />
        <Route path="/recruiter/profile" element={user?.role === 'recruiter' ? <RecruiterProfile user={user} onLogout={handleLogout} onUpdateUser={handleUserUpdate} /> : <Navigate to="/login" />} />

        <Route path="/candidate" element={user?.role === 'candidate' ? <CandidateDashboard user={user} onLogout={handleLogout} /> : <Navigate to="/login" />} />
        <Route path="/candidate/assessment/:assessmentId/details" element={user?.role === 'candidate' ? <AssessmentDetails user={user} onLogout={handleLogout} /> : <Navigate to="/login" />} />
        <Route path="/candidate/apply/:assessmentId" element={user?.role === 'candidate' ? <ApplyAssessment user={user} onLogout={handleLogout} /> : <Navigate to="/login" />} />
        <Route path="/candidate/assessment/:assessmentId" element={user?.role === 'candidate' ? <TakeAssessment user={user} onLogout={handleLogout} /> : <Navigate to="/login" />} />
        <Route path="/candidate/interview/:assessmentId" element={user?.role === 'candidate' ? <Interview user={user} onLogout={handleLogout} /> : <Navigate to="/login" />} />
        <Route path="/candidate/profile" element={user?.role === 'candidate' ? <CandidateProfile user={user} onLogout={handleLogout} onUpdateUser={handleUserUpdate} /> : <Navigate to="/login" />} />

        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;
