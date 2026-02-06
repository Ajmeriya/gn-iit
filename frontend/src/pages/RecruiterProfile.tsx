import { useMemo, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft, Building2, LogOut, Save, Pencil, UserCircle, Zap } from 'lucide-react';
import ThemeToggle from '../components/ThemeToggle';

interface User {
  id: string;
  email: string;
  role: 'recruiter' | 'candidate';
  name: string;
}

interface RecruiterProfileProps {
  user: User;
  onLogout: () => void;
  onUpdateUser: (updates: Partial<User>) => void;
}

type RecruiterProfile = {
  name: string;
  email: string;
  companyName: string;
  title: string;
  phone: string;
  website: string;
  location: string;
  bio: string;
};

const getProfileKey = (userId: string) => `recruiter-profile-${userId}`;

export default function RecruiterProfile({ user, onLogout, onUpdateUser }: RecruiterProfileProps) {
  const navigate = useNavigate();
  const storedProfile = useMemo(() => {
    const raw = localStorage.getItem(getProfileKey(user.id));
    if (!raw) return null;
    try {
      return JSON.parse(raw) as RecruiterProfile;
    } catch {
      return null;
    }
  }, [user.id]);

  const [isEditing, setIsEditing] = useState(false);
  const [saved, setSaved] = useState(false);
  const [profile, setProfile] = useState<RecruiterProfile>({
    name: storedProfile?.name || user.name,
    email: storedProfile?.email || user.email,
    companyName: storedProfile?.companyName || 'HireIQ',
    title: storedProfile?.title || 'Recruiter',
    phone: storedProfile?.phone || '',
    website: storedProfile?.website || '',
    location: storedProfile?.location || '',
    bio: storedProfile?.bio || ''
  });

  const handleChange = (field: keyof RecruiterProfile, value: string) => {
    setProfile(prev => ({ ...prev, [field]: value }));
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
              onClick={() => navigate('/recruiter')}
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
                <h1 className="text-2xl font-bold text-gray-900">Recruiter Profile</h1>
                <p className="text-gray-600">Manage your company profile details</p>
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
              <label className="block text-sm font-semibold text-gray-700 mb-2">Name</label>
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
              <label className="block text-sm font-semibold text-gray-700 mb-2">Company Name</label>
              <div className="relative">
                <Building2 className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  value={profile.companyName}
                  onChange={(e) => handleChange('companyName', e.target.value)}
                  readOnly={!isEditing}
                  className="w-full pl-11 pr-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
                />
              </div>
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Title</label>
              <input
                value={profile.title}
                onChange={(e) => handleChange('title', e.target.value)}
                readOnly={!isEditing}
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Phone</label>
              <input
                value={profile.phone}
                onChange={(e) => handleChange('phone', e.target.value)}
                readOnly={!isEditing}
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Website</label>
              <input
                value={profile.website}
                onChange={(e) => handleChange('website', e.target.value)}
                readOnly={!isEditing}
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
              />
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Location</label>
              <input
                value={profile.location}
                onChange={(e) => handleChange('location', e.target.value)}
                readOnly={!isEditing}
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition"
              />
            </div>
            <div className="md:col-span-2">
              <label className="block text-sm font-semibold text-gray-700 mb-2">Bio</label>
              <textarea
                value={profile.bio}
                onChange={(e) => handleChange('bio', e.target.value)}
                readOnly={!isEditing}
                rows={4}
                className="w-full px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition resize-none"
                placeholder="Share a short description about your company..."
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
