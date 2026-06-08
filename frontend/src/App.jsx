import { Routes, Route } from 'react-router-dom';

function App() {
    return (
        <div className="min-h-screen bg-surface-900">
            {/* Ambient background gradient */}
            <div className="fixed inset-0 -z-10">
                <div className="absolute top-0 left-1/4 w-96 h-96 bg-polis-600/10 rounded-full blur-[128px]" />
                <div className="absolute bottom-0 right-1/4 w-80 h-80 bg-polis-400/5 rounded-full blur-[100px]" />
            </div>

            <Routes>
                <Route path="/" element={<PlaceholderHome />} />
            </Routes>
        </div>
    );
}

function PlaceholderHome() {
    return (
        <div className="flex items-center justify-center min-h-screen">
            <div className="text-center animate-fade-in">
                <div className="inline-flex items-center justify-center w-20 h-20 rounded-2xl bg-polis-600/20 border border-polis-500/30 mb-6">
                    <svg className="w-10 h-10 text-polis-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                        <path strokeLinecap="round" strokeLinejoin="round" d="M9.813 15.904 9 18.75l-.813-2.846a4.5 4.5 0 0 0-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 0 0 3.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 0 0 3.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 0 0-3.09 3.09ZM18.259 8.715 18 9.75l-.259-1.035a3.375 3.375 0 0 0-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 0 0 2.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 0 0 2.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 0 0-2.456 2.456ZM16.894 20.567 16.5 21.75l-.394-1.183a2.25 2.25 0 0 0-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 0 0 1.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 0 0 1.423 1.423l1.183.394-1.183.394a2.25 2.25 0 0 0-1.423 1.423Z" />
                    </svg>
                </div>
                <h1 className="text-4xl font-bold text-white mb-3">Polis</h1>
                <p className="text-lg text-white/50 mb-8 max-w-md">
                    AI Operational Intelligence Assistant
                </p>
                <div className="flex items-center justify-center gap-2 text-sm text-white/30">
                    <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse-soft" />
                    System scaffold ready — Components loading in Phase 8
                </div>
            </div>
        </div>
    );
}

export default App;
