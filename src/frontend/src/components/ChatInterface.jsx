import { useState } from 'react'
import axios from 'axios'

export default function ChatInterface() {
    const [messages, setMessages] = useState([
        { role: 'bot', text: 'Olá! Sou o assistente virtual YOUVISA. Envie seus documentos ou tire dúvidas sobre vistos.' }
    ])
    const [input, setInput] = useState('')
    const [isLoading, setIsLoading] = useState(false)

    const sendMessage = async () => {
        if (!input.trim()) return

        const userMsg = { role: 'user', text: input }
        setMessages(prev => [...prev, userMsg])
        setInput('')
        setIsLoading(true)

        try {
            // Call Backend API
            const response = await axios.post('http://localhost:8000/api/chat/', {
                message: userMsg.text
            })

            setMessages(prev => [...prev, { role: 'bot', text: response.data.response }])
        } catch (error) {
            setMessages(prev => [...prev, { role: 'bot', text: 'Desculpe, tive um erro de conexão.' }])
        } finally {
            setIsLoading(false)
        }
    }

    return (
        <div className="chat-interface card">
            <div className="messages-area">
                {messages.map((msg, idx) => (
                    <div key={idx} className={`message ${msg.role}`}>
                        {msg.text}
                    </div>
                ))}
                {isLoading && <div className="message bot">Digitando...</div>}
            </div>
            <div className="input-area">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                    placeholder="Digite sua mensagem..."
                />
                <button className="send-btn" onClick={sendMessage}>Enviar</button>
            </div>
        </div>
    )
}
