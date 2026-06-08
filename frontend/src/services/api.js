/**
 * Polis API Client — Axios-based service for all backend calls.
 */

import axios from 'axios';

const api = axios.create({
    baseURL: '/api',
    timeout: 60000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor — attach auth token
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('polis_token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Response interceptor — handle errors
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            localStorage.removeItem('polis_token');
        }
        return Promise.reject(error);
    }
);

// ---- API Methods ----

export const uploadFile = (file, onProgress) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        onUploadProgress: onProgress,
    });
};

export const analyzeDocument = (documentId) =>
    api.post('/analyze', { document_id: documentId });

export const sendChatMessage = (message, conversationId = null) =>
    api.post('/chat', { message, conversation_id: conversationId });

export const searchMemory = (query, limit = 10) =>
    api.get('/memory/search', { params: { q: query, limit } });

export const healthCheck = () => api.get('/health');

export default api;
