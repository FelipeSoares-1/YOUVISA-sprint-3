import { useState, useRef, useEffect } from 'react'
import axios from 'axios'

// SVG Icons
const SendIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <line x1="22" y1="2" x2="11" y2="13" />
        <polygon points="22 2 15 22 11 13 2 9 22 2" />
    </svg>
)

const BotAvatar = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" style={{ color: 'var(--accent-light)' }}>
        <rect x="3" y="11" width="18" height="10" rx="2" />
        <circle cx="12" cy="5" r="2" />
        <path d="M12 7v4" />
        <line x1="8" y1="16" x2="8" y2="16" />
        <line x1="16" y1="16" x2="16" y2="16" />
    </svg>
)

export default function ChatInterface() {
    const [messages, setMessages] = useState([
        { role: 'bot', text: 'Olá! Sou o assistente virtual YOUVISA. Como posso ajudar com seu processo?' }
    ])
    const [input, setInput] = useState('')
    const [isLoading, setIsLoading] = useState(false)
    const messagesEndRef = useRef(null)

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }

    useEffect(() => {
        scrollToBottom()
    }, [messages])

    const sendMessage = async () => {
        if (!input.trim()) return

        const userMsg = { role: 'user', text: input }
        setMessages(prev => [...prev, userMsg])
        setInput('')
        setIsLoading(true)

        try {
            const response = await axios.post('http://localhost:8000/api/chat/', {
                message: userMsg.text,
                user_id: 'guest'
            })
            setMessages(prev => [...prev, { role: 'bot', text: response.data.response }])
        } catch {
            setMessages(prev => [...prev, { role: 'bot', text: 'Não consegui conectar ao servidor. Tente novamente.' }])
        } finally {
            setIsLoading(false)
        }
    }

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            sendMessage()
        }
    }

    return (
        <div className="chat-interface">
            <div className="chat-header">
                <h2>Atendimento Inteligente</h2>
                <p>Assistente virtual para acompanhamento do seu processo</p>
            </div>

            <div className="messages-area">
                {messages.map((msg, idx) => (
                    <div key={idx} className={`message ${msg.role}`}>
                        {msg.role === 'bot' && (
                            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.4rem', opacity: 0.7 }}>
                                <BotAvatar />
                                <span style={{ fontSize: '0.72rem', fontWeight: 500, color: 'var(--text-muted)' }}>YOUVISA AI</span>
                            </div>
                        )}
                        <div>{msg.text}</div>
                    </div>
                ))}
                {isLoading && (
                    <div className="message bot">
                        <div className="loading-dots">
                            <span></span><span></span><span></span>
                        </div>
                    </div>
                )}
                <div ref={messagesEndRef} />
            </div>

            <div className="input-area">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Digite sua mensagem..."
                    disabled={isLoading}
                    aria-label="Campo de mensagem"
                />
                <button
                    className="send-btn"
                    onClick={sendMessage}
                    disabled={isLoading || !input.trim()}
                    aria-label="Enviar mensagem"
                >
                    <SendIcon />
                    Enviar
                </button>
            </div>
        </div>
    )
}
