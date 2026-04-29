import { useState, useRef, useEffect } from 'react'
import axios from 'axios'

const INTENT_LABELS = {
  STATUS_QUERY:    'Status',
  MISSING_DOCS:    'Docs pendentes',
  NEXT_STEP:       'Próximo passo',
  DEADLINE:        'Prazo',
  APPROVAL_STATUS: 'Aprovação',
  DOCUMENT_INFO:   'Documento',
  GREETING:        'Saudação',
  HELP:            'Ajuda',
  GENERAL:         'Geral',
}

const INTENT_COLORS = {
  STATUS_QUERY:    '#6366f1',
  MISSING_DOCS:    '#f59e0b',
  NEXT_STEP:       '#06b6d4',
  DEADLINE:        '#a78bfa',
  APPROVAL_STATUS: '#10b981',
  DOCUMENT_INFO:   '#f472b6',
  GREETING:        '#94a3b8',
  HELP:            '#fb923c',
  GENERAL:         '#64748b',
}

const SendIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <line x1="22" y1="2" x2="11" y2="13" /><polygon points="22 2 15 22 11 13 2 9 22 2" />
  </svg>
)

const BotAvatar = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" style={{ color: 'var(--accent-light)' }}>
    <rect x="3" y="11" width="18" height="10" rx="2" /><circle cx="12" cy="5" r="2" />
    <path d="M12 7v4" /><line x1="8" y1="16" x2="8" y2="16" /><line x1="16" y1="16" x2="16" y2="16" />
  </svg>
)

// Session ID persistido no localStorage — mesmo usuário mantém histórico entre recargas
function getSessionId() {
  const key = 'youvisa_session_id'
  let id = localStorage.getItem(key)
  if (!id) {
    id = crypto.randomUUID()
    localStorage.setItem(key, id)
  }
  return id
}

const SESSION_ID = getSessionId()

export default function ChatInterface() {
  const [messages, setMessages] = useState([
    { role: 'bot', text: 'Olá! Sou a Valéria, consultora da YOUVISA. Como posso ajudar com seu processo consular hoje?' }
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async () => {
    if (!input.trim()) return
    const text = input.trim()
    setMessages(prev => [...prev, { role: 'user', text }])
    setInput('')
    setIsLoading(true)

    try {
      const { data } = await axios.post('http://localhost:8000/api/chat/', {
        message: text,
        user_id: SESSION_ID,
      })
      setMessages(prev => [...prev, {
        role: 'bot',
        text: data.response,
        intent: data.detected_intent,
        confidence: data.intent_confidence,
      }])
    } catch {
      setMessages(prev => [...prev, {
        role: 'bot',
        text: 'Não foi possível conectar ao servidor. Verifique se o backend está rodando.',
      }])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage() }
  }

  return (
    <div className="chat-interface">
      <div className="messages-area">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message ${msg.role}`}>
            {msg.role === 'bot' && (
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.4rem' }}>
                <BotAvatar />
                <span style={{ fontSize: '0.7rem', fontWeight: 500, color: 'var(--text-muted)' }}>Valéria · Consultora Virtual</span>
                {msg.intent && (
                  <span style={{
                    fontSize: '0.65rem', fontWeight: 600, padding: '0.1rem 0.4rem',
                    borderRadius: '4px', marginLeft: '0.25rem',
                    color: INTENT_COLORS[msg.intent] || '#64748b',
                    background: (INTENT_COLORS[msg.intent] || '#64748b') + '18',
                    border: `1px solid ${(INTENT_COLORS[msg.intent] || '#64748b')}30`,
                  }}>
                    {INTENT_LABELS[msg.intent] || msg.intent}
                    {msg.confidence != null && (
                      <span style={{ opacity: 0.7, fontWeight: 400, marginLeft: '0.2rem' }}>
                        {Math.round(msg.confidence * 100)}%
                      </span>
                    )}
                  </span>
                )}
              </div>
            )}
            <div>{msg.text}</div>
          </div>
        ))}

        {isLoading && (
          <div className="message bot">
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.4rem' }}>
              <BotAvatar />
              <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>Valéria está digitando...</span>
            </div>
            <div className="loading-dots"><span /><span /><span /></div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-area">
        <input
          type="text"
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Olá, Valéria! Qual o status do meu processo?"
          disabled={isLoading}
          aria-label="Campo de mensagem"
        />
        <button
          className="send-btn"
          onClick={sendMessage}
          disabled={isLoading || !input.trim()}
          aria-label="Enviar"
        >
          <SendIcon />
          Enviar
        </button>
      </div>
    </div>
  )
}
