import { useEffect, useMemo, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Zap, LogOut, ArrowLeft, TrendingUp, Users, Award, Download, AlertTriangle } from 'lucide-react';
import ThemeToggle from '../components/ThemeToggle';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, PieChart, Pie, Cell } from 'recharts';
import { AssessmentAnalytics, getAssessmentAnalytics } from '../data/api';

interface User {
  id: string;
  email: string;
  role: 'recruiter' | 'candidate';
  name: string;
}

interface ResultsProps {
  user: User;
  onLogout: () => void;
}

export default function Results({ user, onLogout }: ResultsProps) {
  const navigate = useNavigate();
  const { assessmentId } = useParams();
  const [analytics, setAnalytics] = useState<AssessmentAnalytics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const loadAnalytics = async () => {
      if (!assessmentId) return;
      try {
        setLoading(true);
        setError('');
        const response = await getAssessmentAnalytics(assessmentId);
        setAnalytics(response);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load analytics.');
      } finally {
        setLoading(false);
      }
    };

    loadAnalytics();
  }, [assessmentId]);

  const skillData: Array<{ skill: string; score: number; weight: number }> = [];
  const radarData = useMemo(() => skillData.map(item => ({ skill: item.skill, score: item.score })), [skillData]);
  const scoreDistribution = analytics?.scoreDistribution ?? [];
  const categoryBreakdown: Array<{ name: string; value: number; color: string }> = [];
  const topCandidates = analytics?.topCandidates ?? [];
  const fraudDetections: Array<{ candidate: string; issue: string; severity: 'high' | 'medium' | 'low' }> = [];

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

      <div className="max-w-7xl mx-auto px-6 py-8">
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
            {error}
          </div>
        )}
        {loading && (
          <div className="mb-6 text-sm text-gray-500">Loading analytics...</div>
        )}
        <div className="flex justify-between items-start mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Assessment Analytics</h1>
            <p className="text-gray-600">{analytics?.title || 'Assessment'} - Detailed Results</p>
          </div>
          <button className="flex items-center space-x-2 px-6 py-2.5 bg-blue-600 text-white rounded-lg hover:bg-blue-700 font-medium transition shadow-md hover:shadow-lg">
            <Download className="w-5 h-5" />
            <span>Export Report</span>
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100">
            <div className="flex items-center justify-between mb-2">
              <Users className="w-6 h-6 text-blue-600" />
              <span className="text-sm text-gray-600">Total</span>
            </div>
            <div className="text-3xl font-bold text-gray-900">{analytics?.totalCandidates ?? 0}</div>
            <div className="text-sm text-gray-600">Candidates</div>
          </div>
          <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100">
            <div className="flex items-center justify-between mb-2">
              <TrendingUp className="w-6 h-6 text-green-600" />
              <span className="text-sm text-gray-600">Average</span>
            </div>
            <div className="text-3xl font-bold text-gray-900">{analytics?.averageScore ?? 0}%</div>
            <div className="text-sm text-gray-600">Score</div>
          </div>
          <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100">
            <div className="flex items-center justify-between mb-2">
              <Award className="w-6 h-6 text-yellow-600" />
              <span className="text-sm text-gray-600">Top Score</span>
            </div>
            <div className="text-3xl font-bold text-gray-900">{analytics?.topScore ?? 0}%</div>
            <div className="text-sm text-gray-600">Best Performer</div>
          </div>
          <div className="bg-white rounded-xl shadow-md p-6 border border-gray-100">
            <div className="flex items-center justify-between mb-2">
              <AlertTriangle className="w-6 h-6 text-red-600" />
              <span className="text-sm text-gray-600">Flagged</span>
            </div>
            <div className="text-3xl font-bold text-gray-900">{analytics?.flaggedCount ?? 0}</div>
            <div className="text-sm text-gray-600">Suspicious</div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-md border border-gray-100 p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Score Distribution</h2>
            {scoreDistribution.length === 0 ? (
              <div className="text-sm text-gray-500">No score data available.</div>
            ) : (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={scoreDistribution}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="range" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="count" fill="#3B82F6" name="Candidates" />
                </BarChart>
              </ResponsiveContainer>
            )}
          </div>

          <div className="bg-white rounded-xl shadow-md border border-gray-100 p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Average Skills Performance</h2>
            {radarData.length === 0 ? (
              <div className="text-sm text-gray-500">No skill performance data available.</div>
            ) : (
              <ResponsiveContainer width="100%" height={300}>
                <RadarChart data={radarData}>
                  <PolarGrid />
                  <PolarAngleAxis dataKey="skill" />
                  <PolarRadiusAxis angle={90} domain={[0, 100]} />
                  <Radar name="Score" dataKey="score" stroke="#3B82F6" fill="#3B82F6" fillOpacity={0.6} />
                  <Tooltip />
                </RadarChart>
              </ResponsiveContainer>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-md border border-gray-100 p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Category Breakdown</h2>
            {categoryBreakdown.length === 0 ? (
              <div className="text-sm text-gray-500">No category breakdown available.</div>
            ) : (
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={categoryBreakdown}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, value }) => `${name}: ${value}%`}
                    outerRadius={100}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {categoryBreakdown.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            )}
          </div>

          <div className="bg-white rounded-xl shadow-md border border-gray-100 p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Skill Weightage & Performance</h2>
            {skillData.length === 0 ? (
              <div className="text-sm text-gray-500">No skill weightage data available.</div>
            ) : (
              <div className="space-y-4">
                {skillData.map((skill, index) => (
                  <div key={index}>
                    <div className="flex justify-between items-center mb-2">
                      <span className="font-medium text-gray-900">{skill.skill}</span>
                      <div className="flex items-center space-x-3">
                        <span className="text-sm text-gray-600">Weight: {skill.weight}%</span>
                        <span className="font-semibold text-gray-900">{skill.score}%</span>
                      </div>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-blue-600 rounded-full h-2 transition-all"
                        style={{ width: `${skill.score}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-md border border-gray-100 p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Top Performers</h2>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Rank</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Candidate</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Score</th>
                    <th className="px-4 py-3 text-left text-xs font-semibold text-gray-600 uppercase">Time</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {topCandidates.map((candidate) => (
                    <tr key={candidate.rank} className="hover:bg-gray-50">
                      <td className="px-4 py-3">
                        <div className="flex items-center">
                          {candidate.rank <= 3 && (
                            <Award className={`w-5 h-5 mr-2 ${
                              candidate.rank === 1 ? 'text-yellow-500' :
                              candidate.rank === 2 ? 'text-gray-400' :
                              'text-orange-600'
                            }`} />
                          )}
                          <span className="font-semibold">{candidate.rank}</span>
                        </div>
                      </td>
                      <td className="px-4 py-3 font-medium text-gray-900">{candidate.name}</td>
                      <td className="px-4 py-3">
                        <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-semibold">
                          {candidate.score}%
                        </span>
                      </td>
                      <td className="px-4 py-3 text-gray-600">—</td>
                    </tr>
                  ))}
                  {topCandidates.length === 0 && (
                    <tr>
                      <td colSpan={4} className="px-4 py-6 text-center text-sm text-gray-500">
                        No top performers yet.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-md border border-gray-100 p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-6">Fraud Detection Alerts</h2>
            {fraudDetections.length === 0 ? (
              <div className="text-sm text-gray-500">No fraud alerts available.</div>
            ) : (
              <>
                <div className="space-y-3">
                  {fraudDetections.map((detection, index) => (
                    <div
                      key={index}
                      className={`p-4 rounded-lg border-2 ${
                        detection.severity === 'high'
                          ? 'bg-red-50 border-red-200'
                          : detection.severity === 'medium'
                          ? 'bg-orange-50 border-orange-200'
                          : 'bg-yellow-50 border-yellow-200'
                      }`}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="font-semibold text-gray-900 mb-1">{detection.candidate}</div>
                          <div className="text-sm text-gray-700">{detection.issue}</div>
                        </div>
                        <span
                          className={`px-3 py-1 rounded-full text-xs font-semibold ${
                            detection.severity === 'high'
                              ? 'bg-red-100 text-red-700'
                              : detection.severity === 'medium'
                              ? 'bg-orange-100 text-orange-700'
                              : 'bg-yellow-100 text-yellow-700'
                          }`}
                        >
                          {detection.severity.toUpperCase()}
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
                <button className="w-full mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 font-medium transition">
                  Review All Flagged Candidates
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
