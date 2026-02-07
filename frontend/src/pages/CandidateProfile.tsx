import { useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, LogOut, Save, Pencil, Upload, UserCircle, Zap } from 'lucide-react';
import ThemeToggle from '../components/ThemeToggle';

interface User {
  id: string;
  email: string;
  role: 'recruiter' | 'candidate';
  name: string;
}

interface CandidateProfileProps {
  user: User;
  onLogout: () => void;
  onUpdateUser: (updates: Partial<User>) => void;
}

type CandidateProfileState = {
  name: string;
  email: string;
  experienceYears: number;
  skills: string;
  resumeFileName: string;
  resumeSummary: string;
  location: string;
  portfolio: string;
  linkedin: string;
};

const getProfileKey = (userId: string) => `candidate-profile-${userId}`;

export default function CandidateProfile({ user, onLogout, onUpdateUser }: CandidateProfileProps) {
  const navigate = useNavigate();
  const storedProfile = useMemo(() => {
    const raw = localStorage.getItem(getProfileKey(user.id));
    if (!raw) return null;
    try {
      return JSON.parse(raw) as CandidateProfileState;
    } catch {
      return null;
    }
  }, [user.id]);

  const [isEditing, setIsEditing] = useState(false);
  const [saved, setSaved] = useState(false);
  const [profile, setProfile] = useState<CandidateProfileState>({
    name: storedProfile?.name || user.name,
    email: storedProfile?.email || user.email,
    experienceYears: storedProfile?.experienceYears ?? 0,
    skills: storedProfile?.skills || '',
    resumeFileName: storedProfile?.resumeFileName || '',
    resumeSummary: storedProfile?.resumeSummary || '',
    location: storedProfile?.location || '',
    portfolio: storedProfile?.portfolio || '',
    linkedin: storedProfile?.linkedin || ''
  });

  const handleChange = (field: keyof CandidateProfileState, value: string | number) => {
    setProfile(prev => ({ ...prev, [field]: value }));
  };

  const handleResumeUpload = (file: File | null) => {
    if (!file) return;
    if (!file.name.toLowerCase().endsWith('.pdf')) {
      alert('Please upload a PDF file.');
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      alert('Max size is 5MB.');
      return;
    }
    setProfile(prev => ({ ...prev, resumeFileName: file.name }));
  };

  const handleSave = () => {
    localStorage.setItem(getProfileKey(user.id), JSON.stringify(profile));
    onUpdateUser({ name: profile.name, email: profile.email });
    setIsEditing(false);
    setSaved(true);
    setTimeout(() => setSaved(false), 1500);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-4">
            <button
              onClick={() => navigate('/candidate')}
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
            <span className="text-gray-700 font-medium">{user.name}</span>
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

      <div className="max-w-5xl mx-auto px-6 py-8">
        <div className="bg-white rounded-2xl shadow-md border border-gray-100 p-8">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center space-x-3">
              <UserCircle className="w-8 h-8 text-blue-600" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">Candidate Profile</h1>
                <p className="text-gray-600">Manage your personal profile details</p>
              </div>
            </div>
            {isEditing ? (
              <button
                onClick={handleSave}
                className="flex items-center space-x-2 px-5 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-semibold transition"
              >
                <Save className="w-4 h-4" />
                <span>{saved ? 'Saved' : 'Save Changes'}</span>
              </button>
            ) : (
              <button
                onClick={() => setIsEditing(true)}
                className="flex items-center space-x-2 px-5 py-2.5 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 font-semibold transition dark:bg-gray-700 dark:text-gray-100 dark:hover:bg-gray-600"
              >
                <Pencil className="w-4 h-4" />
                <span>Edit</span>
              </button>
            )}
          </div>
          {saved && <div className="mt-2 text-sm text-green-600">Changes saved.</div>}

          <div className="mt-8 grid md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Full Name</label>
              <input
                value={profile.name}
                onChange={(e) => handleChange('name', e.target.value)}
                readOnly={!isEditing}
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Email</label>
              <input
                value={profile.email}
                onChange={(e) => handleChange('email', e.target.value)}
                readOnly={!isEditing}
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Experience (years)</label>
              <input
                type="number"
                min={0}
                max={40}
                value={profile.experienceYears}
                onChange={(e) => handleChange('experienceYears', Math.max(0, Number(e.target.value)))}
                readOnly={!isEditing}
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Skills (comma separated)</label>
              <input
                value={profile.skills}
                onChange={(e) => handleChange('skills', e.target.value)}
                readOnly={!isEditing}
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
                placeholder="React, TypeScript, Node.js"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Location</label>
              <input
                value={profile.location}
                onChange={(e) => handleChange('location', e.target.value)}
                readOnly={!isEditing}
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
                placeholder="City, Country"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Portfolio</label>
              <input
                value={profile.portfolio}
                onChange={(e) => handleChange('portfolio', e.target.value)}
                readOnly={!isEditing}
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
                placeholder="https://your-portfolio.com"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">LinkedIn</label>
              <input
                value={profile.linkedin}
                onChange={(e) => handleChange('linkedin', e.target.value)}
                readOnly={!isEditing}
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
                placeholder="https://linkedin.com/in/username"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Resume (PDF only)</label>
              <label className={`inline-flex items-center space-x-2 px-4 py-2.5 rounded-lg border border-gray-300 ${
                isEditing ? 'cursor-pointer bg-blue-600 text-white border-blue-600' : 'bg-gray-100 text-gray-400 cursor-not-allowed'
              }`}>
                <Upload className="w-4 h-4" />
                <span>{profile.resumeFileName ? 'Replace PDF' : 'Upload PDF'}</span>
                <input
                  type="file"
                  accept="application/pdf"
                  className="hidden"
                  disabled={!isEditing}
                  onChange={(e) => handleResumeUpload(e.target.files?.[0] || null)}
                />
              </label>
              <div className="mt-2 text-sm text-gray-600">{profile.resumeFileName || 'No file chosen'}</div>
              <div className="mt-1 text-xs text-gray-400">Max size 5MB. PDF only.</div>
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-semibold text-gray-700 mb-2">Resume Summary (optional)</label>
              <textarea
                value={profile.resumeSummary}
                onChange={(e) => handleChange('resumeSummary', e.target.value)}
                readOnly={!isEditing}
                rows={4}
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition resize-none"
                placeholder="Brief summary of your experience"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
