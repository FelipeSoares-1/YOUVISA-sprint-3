import { useState, useEffect } from 'react'
import ChatInterface from './components/ChatInterface'
import Dashboard from './components/Dashboard'
import NotificationCenter from './components/NotificationCenter'
import InteractionHistory from './components/InteractionHistory'
import './App.css'

const DashboardIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <rect x="3" y="3" width="7" height="9" rx="1" /><rect x="14" y="3" width="7" height="5" rx="1" />
    <rect x="14" y="12" width="7" height="9" rx="1" /><rect x="3" y="16" width="7" height="5" rx="1" />
  </svg>
)

const BellIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
    <path d="M13.73 21a2 2 0 0 1-3.46 0" />
  </svg>
)

const HistoryIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />
  </svg>
)

const SunIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="5" />
    <line x1="12" y1="1"  x2="12" y2="3"  />
    <line x1="12" y1="21" x2="12" y2="23" />
    <line x1="4.22" y1="4.22"  x2="5.64" y2="5.64"  />
    <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
    <line x1="1"  y1="12" x2="3"  y2="12" />
    <line x1="21" y1="12" x2="23" y2="12" />
    <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
    <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
  </svg>
)

const MoonIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
  </svg>
)

const ValeriaIcon = ({ open }) => (
  open ? (
    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
      <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
    </svg>
  ) : (
    <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
      <path d="M8 10h.01" /><path d="M12 10h.01" /><path d="M16 10h.01" />
    </svg>
  )
)

const NAV_ITEMS = [
  { id: 'dashboard',     label: 'Painel de Controle',      Icon: DashboardIcon },
  { id: 'notifications', label: 'Notificações',            Icon: BellIcon },
  { id: 'history',       label: 'Histórico de Interações', Icon: HistoryIcon },
]

function ThemeToggle({ theme, onToggle }) {
  const isDark = theme === 'dark'
  return (
    <div className="theme-toggle-wrapper">
      <button
        className={`theme-toggle ${isDark ? 'dark' : 'light'}`}
        onClick={onToggle}
        aria-label={isDark ? 'Mudar para tema claro' : 'Mudar para tema escuro'}
      >
        <span className={`theme-icon sun ${!isDark ? 'active' : ''}`}><SunIcon /></span>
        <span className="theme-track">
          <span className="theme-thumb" />
        </span>
        <span className={`theme-icon moon ${isDark ? 'active' : ''}`}><MoonIcon /></span>
      </button>
      <span className="theme-tooltip">
        {isDark ? 'Mudar para tema claro' : 'Mudar para tema escuro'}
      </span>
    </div>
  )
}

function App() {
  const [currentView, setCurrentView] = useState('dashboard')
  const [chatOpen, setChatOpen]       = useState(false)
  const [theme, setTheme]             = useState('light')

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
  }, [theme])

  const toggleTheme = () => setTheme(t => t === 'light' ? 'dark' : 'light')

  return (
    <div className="app-container">
      <nav className="sidebar">
        <div className="brand">
          YOU<span className="tag">VISA</span>
        </div>

        {NAV_ITEMS.map(({ id, label, Icon }) => (
          <button
            key={id}
            className={currentView === id ? 'active' : ''}
            onClick={() => setCurrentView(id)}
          >
            <Icon />
            {label}
          </button>
        ))}

        <div style={{ marginTop: 'auto' }}>
          <ThemeToggle theme={theme} onToggle={toggleTheme} />

          <div style={{
            paddingTop: '1rem',
            borderTop: '1px solid var(--border-subtle)',
            fontSize: '0.69rem', color: 'var(--text-muted)',
            lineHeight: 1.65,
          }}>
            <div style={{ fontWeight: 700, color: 'var(--text-secondary)', marginBottom: '0.2rem' }}>Sprint 4</div>
            <div>Arquitetura Multiagente</div>
            <div>SQLite · Gemini 2.5 Flash</div>
          </div>
        </div>
      </nav>

      <main className="main-content">
        {currentView === 'dashboard'     && <Dashboard />}
        {currentView === 'notifications' && <NotificationCenter />}
        {currentView === 'history'       && <InteractionHistory />}
      </main>

      {/* FAB Valéria */}
      <button
        className={`valeria-fab ${chatOpen ? 'open' : ''}`}
        onClick={() => setChatOpen(!chatOpen)}
        aria-label={chatOpen ? 'Fechar chat com Valéria' : 'Converse com a Valéria'}
      >
        {!chatOpen && <span className="fab-pulse" />}
        <ValeriaIcon open={chatOpen} />
        {!chatOpen && <span className="fab-label">Converse com a Valéria</span>}
      </button>

      {/* Chat Modal */}
      {chatOpen && (
        <div className="chat-overlay">
          <div className="chat-modal">
            <div className="chat-modal-header">
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                <div className="valeria-avatar-mini">
                  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                    <path d="M8 10h.01" /><path d="M12 10h.01" /><path d="M16 10h.01" />
                  </svg>
                </div>
                <div>
                  <div className="chat-modal-title">Valéria</div>
                  <div className="chat-modal-subtitle">Consultora Virtual · YOUVISA</div>
                </div>
              </div>
              <div className="online-dot-wrapper">
                <span className="online-dot" />
                <span style={{ fontSize: '0.72rem', color: 'var(--success)' }}>online</span>
              </div>
            </div>
            <div className="chat-modal-body">
              <ChatInterface />
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default App
