import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
    ChevronLeft, Calendar, User, FileText, CheckCircle2,
    AlertTriangle, Flame, ShieldAlert, BookOpen, Layers,
    BarChart3, Download, Share2, MoreVertical
} from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import api from '../services/api';

const MeetingAnalysis = () => {
    const { id } = useParams();
    const [meeting, setMeeting] = useState(null);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState('summary');

    useEffect(() => {
        const fetchMeeting = async () => {
            try {
                const response = await api.get(`/meetings/${id}`);
                setMeeting(response.data);
            } catch (error) {
                console.error('Failed to fetch meeting details:', error);
            } finally {
                setLoading(false);
            }
        };
        fetchMeeting();
    }, [id]);

    if (loading) {
        return (
            <div className="flex-1 flex items-center justify-center">
                <div className="flex flex-col items-center gap-4">
                    <div className="w-12 h-12 border-4 border-polis-600/30 border-t-polis-600 rounded-full animate-spin" />
                    <p className="text-white/40 font-medium">Extracting intelligence findings...</p>
                </div>
            </div>
        );
    }

    if (!meeting) return <div>Meeting not found</div>;

    const tabs = [
        { id: 'summary', label: 'Executive Summary', icon: <BookOpen size={18} /> },
        { id: 'tasks', label: 'Action Items', icon: <CheckCircle2 size={18} /> },
        { id: 'risks', label: 'Risks & Blockers', icon: <ShieldAlert size={18} /> },
        { id: 'contradictions', label: 'Contradictions', icon: <Flame size={18} /> },
        { id: 'transcript', label: 'Transcript', icon: <FileText size={18} /> },
    ];

    return (
        <div className="h-full flex flex-col overflow-hidden bg-white/[0.01]">
            {/* Header */}
            <header className="p-6 border-b border-white/10 flex items-center justify-between">
                <div className="flex items-center gap-6">
                    <Link to="/" className="p-2 hover:bg-white/5 rounded-full transition-colors text-white/50 hover:text-white">
                        <ChevronLeft size={24} />
                    </Link>
                    <div>
                        <h1 className="text-2xl font-bold tracking-tight uppercase truncate max-w-xl">{meeting.title}</h1>
                        <div className="flex items-center gap-4 mt-1 text-sm text-white/40">
                            <span className="flex items-center gap-1.5"><Calendar size={14} /> {new Date(meeting.date || meeting.created_at).toLocaleDateString()}</span>
                            <span className="flex items-center gap-1.5"><User size={14} /> {meeting.speaker_mapping ? Object.keys(meeting.speaker_mapping).length : 0} Participants</span>
                        </div>
                    </div>
                </div>
                <div className="flex gap-3">
                    <button className="btn-secondary py-2 flex items-center gap-2"><Download size={18} /> Export</button>
                    <button className="btn-secondary py-2 px-3"><Share2 size={18} /></button>
                    <button className="btn-secondary py-2 px-3"><MoreVertical size={18} /></button>
                </div>
            </header>

            {/* Navigation Tabs */}
            <nav className="flex px-8 border-b border-white/10 bg-white/[0.005]">
                {tabs.map((tab) => (
                    <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`flex items-center gap-2 px-6 py-4 text-sm font-semibold transition-all relative ${activeTab === tab.id ? 'text-polis-400' : 'text-white/40 hover:text-white/60'
                            }`}
                    >
                        {tab.icon}
                        {tab.label}
                        {activeTab === tab.id && (
                            <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-polis-500 shadow-[0_0_12px_rgba(37,99,235,0.8)]" />
                        )}
                    </button>
                ))}
            </nav>

            {/* Content Area */}
            <div className="flex-1 overflow-y-auto p-8 animate-fade-in">
                {activeTab === 'summary' && (
                    <div className="max-w-4xl space-y-10">
                        {meeting.summaries?.map((s, i) => (
                            <section key={i} className="animate-slide-up">
                                <div className="flex items-center gap-3 mb-6">
                                    <div className="w-1 h-8 bg-polis-500 rounded-full" />
                                    <h2 className="text-2xl font-bold tracking-wide">EXECUTIVE SUMMARY</h2>
                                </div>
                                <div className="prose prose-invert prose-lg max-w-none text-white/80 leading-relaxed">
                                    <ReactMarkdown>{s.content}</ReactMarkdown>
                                </div>
                            </section>
                        ))}

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pt-10">
                            <div className="glass-panel-light p-6 border-l-4 border-amber-500/50">
                                <h3 className="text-amber-400 font-bold mb-3 flex items-center gap-2 uppercase tracking-widest text-xs">
                                    <Flame size={14} /> Critical Contradictions
                                </h3>
                                <p className="text-2xl font-bold">{meeting.contradictions?.length || 0}</p>
                                <p className="text-white/40 text-sm mt-1">Requiring immediate resolution</p>
                            </div>
                            <div className="glass-panel-light p-6 border-l-4 border-red-500/50">
                                <h3 className="text-red-400 font-bold mb-3 flex items-center gap-2 uppercase tracking-widest text-xs">
                                    <ShieldAlert size={14} /> High Risks
                                </h3>
                                <p className="text-2xl font-bold">{meeting.risks?.filter(r => r.severity === 'HIGH' || r.severity === 'CRITICAL').length || 0}</p>
                                <p className="text-white/40 text-sm mt-1">Identified blockers and hazards</p>
                            </div>
                        </div>
                    </div>
                )}

                {activeTab === 'tasks' && (
                    <div className="space-y-4 max-w-5xl">
                        {meeting.tasks?.map((t, i) => (
                            <div key={i} className="p-5 glass-panel-light flex items-start gap-5 hover:bg-white/[0.03] transition-all group animate-slide-up" style={{ animationDelay: `${i * 0.05}s` }}>
                                <div className={`mt-1 p-1 rounded-full border-2 ${t.priority === 'CRITICAL' ? 'border-red-500 text-red-500' : 'border-white/20 text-white/20 group-hover:border-polis-500 group-hover:text-polis-500'}`}>
                                    <CheckCircle2 size={18} />
                                </div>
                                <div className="flex-1">
                                    <p className="text-lg font-medium text-white/90 group-hover:text-white transition-colors">{t.description}</p>
                                    <div className="flex flex-wrap gap-4 mt-3 text-xs uppercase tracking-widest font-bold">
                                        <span className="flex items-center gap-1.5 text-white/40 bg-white/5 py-1 px-2 rounded-md">
                                            <User size={12} /> {t.owner || 'Unassigned'}
                                        </span>
                                        <span className={`py-1 px-2 rounded-md ${t.priority === 'CRITICAL' ? 'bg-red-500/10 text-red-400' :
                                                t.priority === 'HIGH' ? 'bg-amber-500/10 text-amber-400' :
                                                    'bg-polis-500/10 text-polis-400'
                                            }`}>
                                            {t.priority} PRIORITY
                                        </span>
                                        {t.deadline && (
                                            <span className="flex items-center gap-1.5 text-white/40 bg-white/5 py-1 px-2 rounded-md lowercase first-letter:uppercase">
                                                Due {t.deadline}
                                            </span>
                                        )}
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}

                {activeTab === 'risks' && (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {meeting.risks?.map((r, i) => (
                            <div key={i} className={`p-6 glass-panel-light border-l-4 transition-all animate-fade-in ${r.severity === 'CRITICAL' || r.severity === 'HIGH' ? 'border-red-500/50' : 'border-amber-500/50'
                                }`}>
                                <div className="flex justify-between items-start mb-4">
                                    <span className="text-[10px] font-black uppercase tracking-[0.2em] text-white/40">{r.category}</span>
                                    <div className={`px-2 py-0.5 rounded text-[10px] font-bold ${r.severity === 'CRITICAL' ? 'bg-red-500 text-white' : 'bg-amber-500/20 text-amber-500'
                                        }`}>
                                        {r.severity}
                                    </div>
                                </div>
                                <p className="text-lg font-semibold mb-4 leading-snug">{r.description}</p>
                                <div className="flex gap-6 text-xs font-bold text-white/30 uppercase tracking-wider">
                                    <div>Likelihood: <span className="text-white/60">{r.likelihood}</span></div>
                                    <div>Impact: <span className="text-white/60">{r.impact}</span></div>
                                </div>
                            </div>
                        ))}
                    </div>
                )}

                {activeTab === 'contradictions' && (
                    <div className="space-y-6 max-w-4xl">
                        {meeting.contradictions?.map((c, i) => (
                            <div key={i} className="p-8 glass-panel-light border border-polis-500/20 bg-polis-500/[0.02] rounded-3xl animate-slide-up">
                                <div className="flex items-center gap-3 mb-4">
                                    <Flame className="text-polis-400" size={24} />
                                    <span className="text-xs font-black uppercase tracking-widest text-polis-400">{c.category} Contradiction</span>
                                </div>
                                <p className="text-xl font-medium text-white/90 leading-relaxed italic">
                                    "{c.explanation}"
                                </p>
                            </div>
                        ))}
                    </div>
                )}

                {activeTab === 'transcript' && (
                    <div className="glass-panel-light p-8 rounded-3xl font-mono text-sm leading-relaxed text-white/60 max-w-5xl mx-auto whitespace-pre-wrap">
                        {meeting.processed_transcript || meeting.raw_transcript}
                    </div>
                )}
            </div>
        </div>
    );
};

export default MeetingAnalysis;
