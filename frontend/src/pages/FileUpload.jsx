import React, { useState, useCallback } from 'react';
import { Upload, FileText, CheckCircle2, AlertCircle, Loader2, X } from 'lucide-react';
import { uploadFile, analyzeDocument } from '../services/api';

const FileUpload = () => {
    const [file, setFile] = useState(null);
    const [status, setStatus] = useState('idle'); // idle, uploading, processing, completed, error
    const [progress, setProgress] = useState(0);
    const [documentId, setDocumentId] = useState(null);
    const [error, setError] = useState(null);

    const handleDragOver = (e) => {
        e.preventDefault();
        e.stopPropagation();
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        const droppedFile = e.dataTransfer.files[0];
        if (droppedFile) setFile(droppedFile);
    };

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile) setFile(selectedFile);
    };

    const clearFile = () => {
        setFile(null);
        setStatus('idle');
        setProgress(0);
        setError(null);
    };

    const startAnalysis = async () => {
        if (!file) return;

        setStatus('uploading');
        try {
            // 1. Upload
            const uploadRes = await uploadFile(file, (e) => {
                const percent = Math.round((e.loaded * 100) / e.total);
                setProgress(percent);
            });

            const docId = uploadRes.data.document_id;
            setDocumentId(docId);

            // 2. Trigger Analysis
            setStatus('processing');
            await analyzeDocument(docId);

            setStatus('completed');
        } catch (err) {
            console.error(err);
            setStatus('error');
            setError(err.response?.data?.detail || 'Failed to process file');
        }
    };

    return (
        <div className="p-8 max-w-4xl mx-auto h-full flex flex-col justify-center animate-fade-in">
            <div className="text-center mb-12">
                <h1 className="text-4xl font-bold mb-4 tracking-tight">Analyze Discussions</h1>
                <p className="text-lg text-white/50">Upload meeting transcripts, audio recordings, or call notes to generate operational intelligence.</p>
            </div>

            <div
                className={`glass-panel p-12 flex flex-col items-center justify-center border-dashed border-2 transition-all ${status === 'idle' ? 'hover:border-polis-500/50 hover:bg-white/[0.02]' : ''
                    } ${file ? 'border-polis-500/40 bg-polis-500/5' : 'border-white/10'}`}
                onDragOver={handleDragOver}
                onDrop={handleDrop}
            >
                {!file && (
                    <div className="text-center">
                        <div className="w-20 h-20 rounded-full bg-polis-600/20 border border-polis-500/30 flex items-center justify-center mx-auto mb-6">
                            <Upload className="text-polis-400" size={32} />
                        </div>
                        <p className="text-xl font-medium mb-2">Drop your file here</p>
                        <p className="text-white/40 mb-8">PDF, Text, Audio, or Word documents</p>
                        <label className="btn-primary cursor-pointer">
                            Browse Files
                            <input type="file" className="hidden" onChange={handleFileChange} />
                        </label>
                    </div>
                )}

                {file && (
                    <div className="w-full">
                        <div className="flex items-center gap-4 p-4 glass-panel-light mb-8">
                            <div className="w-12 h-12 rounded-lg bg-surface-700 flex items-center justify-center text-polis-400">
                                <FileText size={24} />
                            </div>
                            <div className="flex-1 min-w-0">
                                <p className="font-medium truncate">{file.name}</p>
                                <p className="text-sm text-white/40">{(file.size / (1024 * 1024)).toFixed(2)} MB</p>
                            </div>
                            {status === 'idle' && (
                                <button onClick={clearFile} className="p-2 hover:bg-white/10 rounded-full transition-colors text-white/40 hover:text-red-400">
                                    <X size={20} />
                                </button>
                            )}
                        </div>

                        {status === 'idle' && (
                            <button
                                onClick={startAnalysis}
                                className="w-full btn-primary py-4 text-lg"
                            >
                                Start AI Analysis
                            </button>
                        )}

                        {(status === 'uploading' || status === 'processing') && (
                            <div className="space-y-6">
                                <div className="flex justify-between text-sm font-medium">
                                    <span className="flex items-center gap-2">
                                        <Loader2 className="animate-spin text-polis-400" size={16} />
                                        {status === 'uploading' ? `Uploading... ${progress}%` : 'AI Agents analyzing...'}
                                    </span>
                                    <span className="text-white/40 italic">This may take a few minutes</span>
                                </div>
                                <div className="h-2 bg-white/5 rounded-full overflow-hidden">
                                    <div
                                        className="h-full bg-polis-500 transition-all duration-300"
                                        style={{ width: `${status === 'uploading' ? progress : 100}%` }}
                                    />
                                </div>
                            </div>
                        )}

                        {status === 'completed' && (
                            <div className="text-center p-6 bg-green-500/10 border border-green-500/20 rounded-2xl animate-slide-up">
                                <CheckCircle2 className="mx-auto mb-4 text-green-400" size={48} />
                                <h3 className="text-xl font-bold mb-2">Analysis Queued!</h3>
                                <p className="text-white/60 mb-6">Polis is processing the discussion. You can track progress in the dashboard.</p>
                                <Link to="/" className="btn-primary block w-full">Go to Dashboard</Link>
                            </div>
                        )}

                        {status === 'error' && (
                            <div className="text-center p-6 bg-red-500/10 border border-red-500/20 rounded-2xl animate-slide-up">
                                <AlertCircle className="mx-auto mb-4 text-red-400" size={48} />
                                <h3 className="text-xl font-bold mb-2">Analysis Failed</h3>
                                <p className="text-white/60 mb-6">{error}</p>
                                <button onClick={clearFile} className="btn-primary bg-red-600 hover:bg-red-500 border-none w-full">Try Again</button>
                            </div>
                        )}
                    </div>
                )}
            </div>

            <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6 opacity-40">
                <div className="p-4 rounded-xl border border-white/10 text-center">
                    <p className="font-bold text-sm uppercase tracking-widest mb-1">Upload</p>
                    <p className="text-xs">Meeting transcripts or audio recordings</p>
                </div>
                <div className="p-4 rounded-xl border border-white/10 text-center">
                    <p className="font-bold text-sm uppercase tracking-widest mb-1">Analyze</p>
                    <p className="text-xs">Multi-agent intelligence extraction</p>
                </div>
                <div className="p-4 rounded-xl border border-white/10 text-center">
                    <p className="font-bold text-sm uppercase tracking-widest mb-1">Insights</p>
                    <p className="text-xs">Tasks, Risks, and Executive Summary</p>
                </div>
            </div>
        </div>
    );
};

export default FileUpload;
