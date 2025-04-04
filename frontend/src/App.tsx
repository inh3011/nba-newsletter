import React, { useState } from 'react';
import axios from 'axios';
import { Mail, ShoppingBasket as Basketball, CheckCircle2, Loader2 } from 'lucide-react';

interface Team {
  id: number;
  name: string;
  abbreviation: string;
}

interface User {
  email: string;
  teams: Team[];
  players: any[];
  created_at: string;
  updated_at: string;
}

const App: React.FC = () => {
  const [email, setEmail] = useState('');
  const [step, setStep] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [teams, setTeams] = useState<Team[]>([]);
  const [selectedTeams, setSelectedTeams] = useState<number[]>([]);
  const [user, setUser] = useState<User | null>(null);

  const handleSubscribe = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Subscribe user
      const response = await axios.post('/api/users/subscribe', { email });
      if (!response.data.success) {
        setError(response.data.error || response.data.message);
        return;
      }

      // Fetch user data to get current team selections
      const userResponse = await axios.get(`/api/users/subscribe/${encodeURIComponent(email)}`);
      if (userResponse.data.success) {
        setUser(userResponse.data.data);
        // Set the selected teams from user data
        setSelectedTeams(userResponse.data.data.teams.map((team: Team) => team.id));
      }

      // Fetch available teams
      const { data: { data } } = await axios.get('/api/teams');
      if (!data) {
        setError('Failed to load teams data');
        return;
      }
      setTeams(data);
      setStep(2);
    } catch (err: any) {
      setError(err.response?.data?.error || err.response?.data?.message || 'Something went wrong. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleTeamToggle = (teamId: number) => {
    setSelectedTeams(prev =>
      prev.includes(teamId)
        ? prev.filter(id => id !== teamId)
        : [...prev, teamId]
    );
  };

  const handleTeamsSubmit = async () => {
    setLoading(true);
    setError('');

    try {
      const response = await axios.patch(`/api/users/${encodeURIComponent(email)}/teams`, [...selectedTeams]);
      if (!response.data.success) {
        setError(response.data.error || response.data.message);
        return;
      }
      setStep(3);
    } catch (err: any) {
      setError(err.response?.data?.error || err.response?.data?.message || 'Failed to save team preferences. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="w-full max-w-[400px] mx-auto">
        {error && (
          <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
            {error}
          </div>
        )}

        {step === 1 && (
          <div className="bg-white rounded-xl shadow-lg p-6 space-y-6">
            <div className="text-center">
              <div className="bg-blue-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <Basketball className="w-8 h-8 text-blue-600" />
              </div>
              <h1 className="text-2xl font-bold text-gray-900">NBA Newsletter</h1>
              <p className="text-gray-600 mt-2">Get the latest updates from your favorite teams</p>
            </div>

            <form onSubmit={handleSubscribe} className="space-y-4">
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="Enter your email"
                  className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                  disabled={loading}
                />
              </div>
              <button
                type="submit"
                disabled={loading}
                className="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:bg-blue-400 flex items-center justify-center"
              >
                {loading ? (
                  <Loader2 className="w-5 h-5 animate-spin" />
                ) : (
                  'Subscribe'
                )}
              </button>
            </form>
          </div>
        )}

        {step === 2 && (
          <div className="bg-white rounded-xl shadow-lg p-6 space-y-6">
            <div className="text-center">
              <h2 className="text-2xl font-bold text-gray-900">Select Your Teams</h2>
              <p className="text-gray-600 mt-2">Choose your favorite NBA teams to follow</p>
            </div>

            <div className="space-y-3">
              {teams.map(team => (
                <label
                  key={team.id}
                  className={`flex items-center p-3 rounded-lg border cursor-pointer ${
                    selectedTeams.includes(team.id)
                      ? 'border-blue-500 bg-blue-50 text-blue-700'
                      : 'border-gray-200 hover:border-blue-500 hover:bg-blue-50'
                  } transition-colors`}
                >
                  <input
                    type="checkbox"
                    checked={selectedTeams.includes(team.id)}
                    onChange={() => handleTeamToggle(team.id)}
                    className="w-4 h-4 text-blue-600 rounded border-gray-300 focus:ring-blue-500"
                  />
                  <span className="ml-3">{team.full_name}</span>
                </label>
              ))}
            </div>

            <button
              onClick={handleTeamsSubmit}
              disabled={selectedTeams.length === 0 || loading}
              className="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center"
            >
              {loading ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                'Save Preferences'
              )}
            </button>
          </div>
        )}

        {step === 3 && (
          <div className="bg-white rounded-xl shadow-lg p-6 text-center space-y-4">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto">
              <CheckCircle2 className="w-8 h-8 text-green-600" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900">You're All Set!</h2>
            <p className="text-gray-600">
              Thank you for subscribing. You'll start receiving updates about your favorite teams soon!
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;