import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, MessageSquare, Database, PlusCircle, Settings, LogOut, ChevronLeft, ChevronRight } from 'lucide-react';

const Layout = ({ children }) => {
    const [collapsed, setCollapsed] = React.useState(false);

    const navItems = [
        { icon: <LayoutDashboard size={20} />, label: 'Dashboard', path: '/' },
        { icon: <MessageSquare size={20} />, label: 'Chat', path: '/chat' },
        { icon: <Database size={20} />, label: 'Memory', path: '/memory' },
        { icon: <PlusCircle size={20} />, label: 'Upload', path: '/upload' },
    ];

    return (
        <div className="flex min-h-screen bg-surface-900 text-white overflow-hidden">
            {/* Sidebar */}
            <aside
                className={`relative z-20 flex flex-col glass-panel border-y-0 border-l-0 rounded-none transition-all duration-300 ease-in-out ${collapsed ? 'w-20' : 'w-64'
                    }`}
            >
                {/* Logo */}
                <div className="p-6 flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-polis-600 flex items-center justify-center flex-shrink-0">
                        <span className="font-bold text-white">P</span>
                    </div>
                    {!collapsed && <span className="text-xl font-bold tracking-tight">Polis</span>}
                </div>

                {/* Navigation */}
                <nav className="flex-1 px-3 py-6 space-y-1">
                    {navItems.map((item) => (
                        <NavLink
                            key={item.path}
                            to={item.path}
                            className={({ isActive }) =>
                                `flex items-center gap-3 px-3 py-3 rounded-xl transition-all duration-200 ${isActive
                                    ? 'bg-polis-600 text-white shadow-lg shadow-polis-600/20'
                                    : 'text-white/50 hover:bg-white/5 hover:text-white'
                                }`
                            }
                        >
                            <div className="flex-shrink-0">{item.icon}</div>
                            {!collapsed && <span className="font-medium">{item.label}</span>}
                        </NavLink>
                    ))}
                </nav>

                {/* User / Settings Footer */}
                <div className="p-4 border-t border-white/10 space-y-1">
                    {!collapsed && (
                        <div className="px-2 py-3 flex items-center gap-3 mb-2">
                            <div className="w-8 h-8 rounded-full bg-surface-700 border border-white/10" />
                            <div className="overflow-hidden">
                                <p className="text-sm font-medium truncate">Admin User</p>
                                <p className="text-xs text-white/40 truncate">admin@polis.ai</p>
                            </div>
                        </div>
                    )}
                    <button className="w-full flex items-center gap-3 px-3 py-3 rounded-xl text-white/50 hover:bg-white/5 hover:text-white transition-all duration-200">
                        <Settings size={20} />
                        {!collapsed && <span className="font-medium">Settings</span>}
                    </button>
                    <button className="w-full flex items-center gap-3 px-3 py-3 rounded-xl text-red-400/50 hover:bg-red-500/10 hover:text-red-400 transition-all duration-200">
                        <LogOut size={20} />
                        {!collapsed && <span className="font-medium">Logout</span>}
                    </button>
                </div>

                {/* Collapse Toggle */}
                <button
                    onClick={() => setCollapsed(!collapsed)}
                    className="absolute -right-3 top-1/2 -translate-y-1/2 w-6 h-6 bg-surface-800 border border-white/10 rounded-full flex items-center justify-center text-white/50 hover:text-white hover:bg-surface-700 transition-all"
                >
                    {collapsed ? <ChevronRight size={14} /> : <ChevronLeft size={14} />}
                </button>
            </aside>

            {/* Main Content Area */}
            <main className="flex-1 relative flex flex-col h-screen overflow-y-auto pt-4 pr-4 pb-4">
                <div className="glass-panel flex-1 overflow-hidden flex flex-col">
                    {children}
                </div>
            </main>

            {/* Ambient background gradient */}
            <div className="fixed inset-0 -z-10 pointer-events-none">
                <div className="absolute top-0 left-1/4 w-96 h-96 bg-polis-600/10 rounded-full blur-[128px]" />
                <div className="absolute bottom-0 right-1/4 w-80 h-80 bg-polis-400/5 rounded-full blur-[100px]" />
            </div>
        </div>
    );
};

export default Layout;
