import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

export const uploadFile = (file, onUploadProgress) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/upload', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
        onUploadProgress,
    });
};

export const analyzeDocument = (documentId) => {
    return api.post(`/analyze?document_id=${documentId}`);
};

export const sendChatMessage = (message, conversationId = 'new') => {
    return api.post('/chat', {
        message,
        conversation_id: conversationId,
    });
};

export default api;
