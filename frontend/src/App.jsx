import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import MeetingAnalysis from './pages/MeetingAnalysis';
import FileUpload from './pages/FileUpload';
import ChatPage from './pages/ChatPage';
import MemoryPage from './pages/MemoryPage';

function App() {
    return (
        <BrowserRouter>
            <Layout>
                <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/meetings/:id" element={<MeetingAnalysis />} />
                    <Route path="/upload" element={<FileUpload />} />
                    <Route path="/chat" element={<ChatPage />} />
                    <Route path="/memory" element={<MemoryPage />} />
                </Routes>
            </Layout>
        </BrowserRouter>
    );
}

export default App;
