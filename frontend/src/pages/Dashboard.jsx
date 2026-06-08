import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { Calendar, Clock, FileText, ChevronRight, AlertTriangle, CheckCircle2, User } from 'lucide-react';
import api from '../services/api';

const Dashboard = () => {
    const [meetings, setMeetings] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchMeetings = async () => {
            try {
                const response = await api.get('/meetings');
                setMeetings(response.data);
            } catch (error) {
                console.error('Failed to fetch meetings:', error);
            } finally {
                setLoading(false);
            }
        };
        fetchMeetings();
    }, []);

    if (loading) {
        return (
            <div className="flex-1 flex items-center justify-center">
                <div className="flex flex-col items-center gap-4">
                    <div className="w-12 h-12 border-4 border-polis-600/30 border-t-polis-600 rounded-full animate-spin" />
                    <p className="text-white/40 font-medium">Loading intelligence dashboard...</p>
                </div>
            </div>
        );
    }

    return (
        <div className="p-8 h-full flex flex-col overflow-y-auto">
            <header className="mb-10 animate-fade-in">
                <h1 className="text-3xl font-bold text-white mb-2 tracking-tight">Intelligence Dashboard</h1>
                <p className="text-white/50">Overview of recent discussions and operational insights.</p>
            </header>

            <div className="grid grid-cols-1 gap-4 animate-slide-up">
                {meetings.length === 0 ? (
                    <div className="p-12 glass-panel-light flex flex-col items-center justify-center text-center">
                        <div className="w-16 h-16 rounded-2xl bg-white/5 flex items-center justify-center mb-4">
                            <FileText size={32} className="text-white/20" />
                        </div>
                        <h3 className="text-xl font-semibold mb-2">No meetings analyzed yet</h3>
                        <p className="text-white/40 max-w-sm mb-6">Upload a transcript or audio recording to generate operational intelligence.</p>
                        <Link to="/upload" className="btn-primary">Get Started</Link>
                    </div>
                ) : (
                    meetings.map((meeting) => (
                        <Link
                            key={meeting.id}
                            to={`/meetings/${meeting.id}`}
                            className="p-6 glass-panel-light flex items-center gap-6 hover:bg-white/[0.05] transition-all group"
                        >
                            <div className="w-12 h-12 rounded-xl bg-polis-600/20 flex items-center justify-center text-polis-400 border border-polis-500/30">
                                <FileText size={24} />
                            </div>

                            <div className="flex-1 min-w-0">
                                <h3 className="font-semibold text-lg truncate group-hover:text-polis-400 transition-colors uppercase tracking-wide">
                                    {meeting.title}
                                </h3>
                                <div className="flex items-center gap-4 mt-2 text-sm text-white/40">
                                    <span className="flex items-center gap-1.5">
                                        <Calendar size={14} />
                                        {new Date(meeting.created_at).toLocaleDateString()}
                                    </span>
                                    <span className="flex items-center gap-1.5">
                                        <Clock size={14} />
                                        {new Date(meeting.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                    </span>
                                    <span className="flex items-center gap-1.5 capitalize">
                                        <User size={14} />
                                        {meeting.source?.replace('application/', '') || 'Transcript'}
                                    </span>
                                </div>
                            </div>

                            {/* Status Pills (Mocked based on generic risk level) */}
                            <div className="hidden md:flex gap-2">
                                <span className="badge-severity-high">3 Risks</span>
                                <span className="badge-severity-low">8 Tasks</span>
                            </div>

                            <div className="text-white/20 group-hover:text-polis-400 transition-all group-hover:translate-x-1">
                                <ChevronRight size={20} />
                            </div>
                        </Link>
                    ))
                )}
            </div>
        </div>
    );
};

export default Dashboard;
