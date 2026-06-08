import React, { useState } from 'react';
import { Search, Database, FileText, Calendar, Link as LinkIcon, ExternalLink } from 'lucide-react';
import { Link } from 'react-router-dom';
import api from '../services/api';

const MemorySearch = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(false);
    const [hasSearched, setHasSearched] = useState(false);

    const handleSearch = async (e) => {
        e.preventDefault();
        if (!query.trim()) return;

        setLoading(true);
        try {
            const response = await api.get(`/memory/search?q=${encodeURIComponent(query)}&limit=10`);
            setResults(response.data.results);
            setHasSearched(true);
        } catch (error) {
            console.error('Search failed:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-8 h-full flex flex-col items-center overflow-y-auto animate-fade-in">
            <div className={`w-full max-w-4xl transition-all duration-500 ${hasSearched ? 'mt-0' : 'mt-[15vh]'}`}>
                <div className="text-center mb-10">
                    <div className="w-16 h-16 rounded-3xl bg-polis-600/20 border border-polis-500/30 flex items-center justify-center mx-auto mb-6 shadow-xl shadow-polis-600/10">
                        <Database className="text-polis-400" size={32} />
                    </div>
                    <h1 className="text-4xl font-bold tracking-tight mb-4">Organizational Memory</h1>
                    <p className="text-lg text-white/50">Search across all meetings, documents, and discussions semantically.</p>
                </div>

                <form onSubmit={handleSearch} className="relative group mb-12">
                    <div className="absolute inset-y-0 left-6 flex items-center pointer-events-none text-white/20 group-focus-within:text-polis-400 transition-colors">
                        <Search size={24} />
                    </div>
                    <input
                        type="text"
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        placeholder="Search for projects, decisions, or commitments..."
                        className="w-full pl-16 pr-6 py-6 bg-white/5 border border-white/10 rounded-3xl focus:outline-none focus:border-polis-500/50 focus:ring-1 focus:ring-polis-500/25 transition-all text-xl placeholder:text-white/20 shadow-2xl shadow-black/20"
                    />
                    {loading && (
                        <div className="absolute right-6 top-1/2 -translate-y-1/2">
                            <div className="w-6 h-6 border-2 border-polis-600/30 border-t-polis-600 rounded-full animate-spin" />
                        </div>
                    )}
                </form>

                {hasSearched && (
                    <div className="space-y-6 animate-slide-up">
                        <div className="flex items-center justify-between mb-4 px-2">
                            <h2 className="text-sm font-bold uppercase tracking-[0.2em] text-white/30">Semantic Match Results</h2>
                            <span className="text-xs text-white/20">{results.length} items found</span>
                        </div>

                        {results.length === 0 ? (
                            <div className="text-center py-20 glass-panel-light">
                                <p className="text-white/40">No matching memories found for "{query}"</p>
                            </div>
                        ) : (
                            results.map((res, i) => (
                                <div key={i} className="p-8 glass-panel-light hover:bg-white/[0.03] transition-all group relative overflow-hidden">
                                    <div className="flex justify-between items-start mb-4">
                                        <div className="flex items-center gap-3">
                                            <div className="p-2 rounded-lg bg-surface-700 text-polis-400">
                                                <FileText size={18} />
                                            </div>
                                            <div className="min-w-0">
                                                <p className="text-xs font-bold text-white/40 uppercase tracking-widest truncate">{res.metadata?.filename || 'System Memory'}</p>
                                            </div>
                                        </div>
                                        <div className="text-[10px] font-mono text-white/20">Relevance: {Math.round(res.score * 100)}%</div>
                                    </div>

                                    <p className="text-lg text-white/80 leading-relaxed mb-6">
                                        {res.content}
                                    </p>

                                    {res.metadata?.meeting_id && (
                                        <Link
                                            to={`/meetings/${res.metadata.meeting_id}`}
                                            className="flex items-center gap-2 text-polis-400 text-sm font-bold hover:text-polis-300 transition-colors"
                                        >
                                            <ExternalLink size={14} /> View full discussion context
                                        </Link>
                                    )}

                                    {/* Subtle progress indicator for match score */}
                                    <div className="absolute bottom-0 left-0 h-0.5 bg-polis-500/30" style={{ width: `${res.score * 100}%` }} />
                                </div>
                            ))
                        )}
                    </div>
                )}
            </div>
        </div>
    );
};

export default MemorySearch;
