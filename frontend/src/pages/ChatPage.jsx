import React, { useState, useEffect, useRef } from 'react';
import { Send, User, Sparkles, Loader2, Database, AlertCircle } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { sendChatMessage } from '../services/api';

const ChatInterface = () => {
    const [messages, setMessages] = useState([
        { role: 'assistant', content: 'Hello! I am Polis. How can I help you today? I have access to all your organizational memory and analyzed discussions.', created_at: new Date().toISOString() }
    ]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [conversationId, setConversationId] = useState('new');
    const scrollRef = useRef(null);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [messages, loading]);

    const handleSend = async (e) => {
        e.preventDefault();
        if (!input.trim() || loading) return;

        const userMessage = { role: 'user', content: input, created_at: new Date().toISOString() };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setLoading(true);

        try {
            const response = await sendChatMessage(input, conversationId);
            const assistantMessage = {
                role: 'assistant',
                content: response.data.response,
                created_at: new Date().toISOString()
            };
            setMessages(prev => [...prev, assistantMessage]);
            setConversationId(response.data.conversation_id);
        } catch (error) {
            console.error('Chat error:', error);
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: 'I encountered an error processing your request. Please check if the backend is running and your API keys are configured.',
                error: true,
                created_at: new Date().toISOString()
            }]);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-full overflow-hidden">
            {/* Header */}
            <div className="p-6 border-b border-white/10 flex items-center justify-between bg-white/[0.01]">
                <div className="flex items-center gap-4">
                    <div className="w-10 h-10 rounded-xl bg-polis-600/20 flex items-center justify-center text-polis-400 border border-polis-500/30">
                        <Sparkles size={20} />
                    </div>
                    <div>
                        <h2 className="font-bold tracking-tight">Intelligence Chat</h2>
                        <p className="text-xs text-white/40 flex items-center gap-1">
                            <Database size={10} />
                            Connected to Organizational Memory
                        </p>
                    </div>
                </div>
                <div className="flex gap-2">
                    <button
                        onClick={() => {
                            setMessages([{ role: 'assistant', content: 'Started a new conversation. How can I help?', created_at: new Date().toISOString() }]);
                            setConversationId('new');
                        }}
                        className="px-3 py-1.5 text-xs font-semibold bg-white/5 hover:bg-white/10 rounded-lg transition-colors"
                    >
                        New Session
                    </button>
                </div>
            </div>

            {/* Messages */}
            <div
                ref={scrollRef}
                className="flex-1 overflow-y-auto p-6 space-y-8 scroll-smooth"
            >
                {messages.map((msg, idx) => (
                    <div
                        key={idx}
                        className={`flex gap-4 animate-fade-in ${msg.role === 'assistant' ? 'max-w-[90%]' : 'max-w-[90%] ml-auto flex-row-reverse'}`}
                    >
                        <div className={`w-10 h-10 rounded-xl flex-shrink-0 flex items-center justify-center border transition-all ${msg.role === 'assistant'
                                ? 'bg-surface-800 border-white/10 text-polis-400'
                                : 'bg-polis-600 border-polis-500/50 text-white'
                            }`}>
                            {msg.role === 'assistant' ? <Sparkles size={18} /> : <User size={18} />}
                        </div>

                        <div className={`space-y-2 ${msg.role === 'user' ? 'text-right' : ''}`}>
                            <div className={`p-4 rounded-2xl text-base leading-relaxed ${msg.role === 'assistant'
                                    ? (msg.error ? 'bg-red-500/10 border border-red-500/20 text-red-200' : 'bg-white/5 border border-white/10 text-white/90')
                                    : 'bg-polis-600 text-white shadow-xl shadow-polis-600/10'
                                }`}>
                                {msg.error && <AlertCircle className="inline-block mr-2 mb-1" size={16} />}
                                <ReactMarkdown className="prose prose-invert max-w-none prose-p:leading-relaxed prose-pre:bg-black/30">
                                    {msg.content}
                                </ReactMarkdown>
                            </div>
                            <p className="text-[10px] text-white/20 font-mono">
                                {new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                            </p>
                        </div>
                    </div>
                ))}
                {loading && (
                    <div className="flex gap-4 animate-pulse">
                        <div className="w-10 h-10 rounded-xl bg-surface-800 border border-white/10 flex items-center justify-center text-polis-400">
                            <Loader2 className="animate-spin" size={18} />
                        </div>
                        <div className="p-4 rounded-2xl bg-white/5 border border-white/10 w-32 h-14" />
                    </div>
                )}
            </div>

            {/* Input */}
            <div className="p-6 bg-white/[0.01] border-t border-white/10">
                <form onSubmit={handleSend} className="relative group">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Ask anything about your organization, meetings, or decisions..."
                        className="w-full pl-6 pr-14 py-5 bg-white/5 border border-white/10 rounded-2xl focus:outline-none focus:border-polis-500/50 focus:ring-1 focus:ring-polis-500/25 transition-all text-lg placeholder:text-white/20"
                    />
                    <button
                        type="submit"
                        disabled={!input.trim() || loading}
                        className={`absolute right-3 top-1/2 -translate-y-1/2 p-3 rounded-xl transition-all ${input.trim() && !loading
                                ? 'bg-polis-600 text-white hover:bg-polis-500 hover:scale-105 active:scale-95 shadow-lg shadow-polis-600/20'
                                : 'bg-white/5 text-white/20'
                            }`}
                    >
                        <Send size={24} />
                    </button>
                </form>
                <p className="mt-4 text-[11px] text-center text-white/20 uppercase tracking-[0.2em] font-medium">
                    Polis AI Brain • GPT-4o Enhanced
                </p>
            </div>
        </div>
    );
};

export default ChatInterface;
