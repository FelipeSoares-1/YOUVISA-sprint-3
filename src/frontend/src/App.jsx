import { useState } from 'react'
import ChatInterface from './components/ChatInterface'
import Dashboard from './components/Dashboard'
import './App.css'

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
          Painel de Controle
        </button>
        <button
          className={currentView === 'chat' ? 'active' : ''}
          onClick={() => setCurrentView('chat')}
        >
          Atendimento Inteligente
        </button>
      </nav>

      <main className="main-content">
        {currentView === 'dashboard' ? <Dashboard /> : <ChatInterface />}
      </main>
    </div>
  )
}

export default App
