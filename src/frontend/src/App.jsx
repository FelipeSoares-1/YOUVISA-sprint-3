import { useState } from 'react'
import ChatInterface from './components/ChatInterface'
import Dashboard from './components/Dashboard'
import NotificationCenter from './components/NotificationCenter'
import './App.css'

// SVG Icons (inline, no emoji)
const DashboardIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="3" width="7" height="9" rx="1" />
    <rect x="14" y="3" width="7" height="5" rx="1" />
    <rect x="14" y="12" width="7" height="9" rx="1" />
    <rect x="3" y="16" width="7" height="5" rx="1" />
  </svg>
)

const ChatIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
    <path d="M8 10h.01" /><path d="M12 10h.01" /><path d="M16 10h.01" />
  </svg>
)

const BellIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
    <path d="M13.73 21a2 2 0 0 1-3.46 0" />
  </svg>
)

function App() {
  const [currentView, setCurrentView] = useState('dashboard')

  return (
    <div className="app-container">
      <nav className="sidebar">
        <div className="brand">YOUVISA <span className="tag">AI</span></div>
        <button
          className={currentView === 'dashboard' ? 'active' : ''}
          onClick={() => setCurrentView('dashboard')}
        >
          <DashboardIcon />
          Painel de Controle
        </button>
        <button
          className={currentView === 'chat' ? 'active' : ''}
          onClick={() => setCurrentView('chat')}
        >
          <ChatIcon />
          Atendimento Inteligente
        </button>
        <button
          className={currentView === 'notifications' ? 'active' : ''}
          onClick={() => setCurrentView('notifications')}
        >
          <BellIcon />
          Notificações
        </button>
      </nav>

      <main className="main-content">
        {currentView === 'dashboard' && <Dashboard />}
        {currentView === 'chat' && <ChatInterface />}
        {currentView === 'notifications' && <NotificationCenter />}
      </main>
    </div>
  )
}

export default App

