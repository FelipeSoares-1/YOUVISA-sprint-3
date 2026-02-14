import { useState, useEffect } from 'react'
import axios from 'axios'
import FileUpload from './FileUpload'
import StatusTimeline from './StatusTimeline'

// SVG Icons
const BellIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
        <path d="M13.73 21a2 2 0 0 1-3.46 0" />
    </svg>
)

const FileIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
        <polyline points="14 2 14 8 20 8" />
    </svg>
)

const InboxIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="22 12 16 12 14 15 10 15 8 12 2 12" />
        <path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z" />
    </svg>
)

export default function Dashboard() {
    const [documents, setDocuments] = useState([])
    const [notifications, setNotifications] = useState([])
    const [loading, setLoading] = useState(false)
    const [showNotifications, setShowNotifications] = useState(false)

    const fetchDocuments = async () => {
        try {
            const res = await axios.get('http://localhost:8000/api/documents/')
            setDocuments(res.data)
        } catch (err) { /* silent */ }
    }

    const fetchNotifications = async () => {
        try {
            const res = await axios.get('http://localhost:8000/api/notifications/')
            setNotifications(res.data)
        } catch (err) { /* silent */ }
    }

    useEffect(() => {
        fetchDocuments()
        fetchNotifications()
        const interval = setInterval(() => {
            fetchDocuments()
            fetchNotifications()
        }, 3000)
        return () => clearInterval(interval)
    }, [])

    const handleUploadSuccess = () => {
        fetchDocuments()
        fetchNotifications()
    }

    const handleTransition = async (docId, event) => {
        setLoading(true)
        try {
            await axios.post(`http://localhost:8000/api/documents/${docId}/transition?event=${event}`)
            fetchDocuments()
            fetchNotifications()
        } catch (err) {
            alert("Erro na transição: " + (err.response?.data?.detail || err.message))
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="dashboard">
            {/* Header */}
            <div className="page-header">
                <h1>Painel de Acompanhamento</h1>
                <button
                    className="notification-toggle"
                    onClick={() => setShowNotifications(!showNotifications)}
                    aria-label="Abrir notificações"
                >
                    <BellIcon />
                    Notificações
                    {notifications.length > 0 && (
                        <span className="notification-badge">{notifications.length}</span>
                    )}
                </button>
            </div>

            {/* Notifications Panel */}
            {showNotifications && (
                <div className="card notification-panel" style={{ marginBottom: 'var(--space-lg)' }}>
                    <h3>Central de Notificações</h3>
                    {notifications.length === 0 ? (
                        <div className="empty-state">
                            <InboxIcon />
                            <p>Nenhuma notificação ainda</p>
                        </div>
                    ) : (
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', maxHeight: '260px', overflowY: 'auto' }}>
                            {notifications.slice().reverse().map((notif, idx) => (
                                <div key={idx} className="notification-item">
                                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.2rem' }}>
                                        <span className="event-type">{notif.event_type}</span>
                                        <span className="time">{new Date(notif.sent_at).toLocaleTimeString()}</span>
                                    </div>
                                    <p className="message-text">{notif.message}</p>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            )}

            {/* Upload */}
            <div className="card">
                <h3>Novo Processo</h3>
                <FileUpload onUploadSuccess={handleUploadSuccess} />
            </div>

            {/* Processes */}
            <div className="card">
                <h3>Seus Processos</h3>
                {documents.length === 0 ? (
                    <div className="empty-state">
                        <InboxIcon />
                        <p>Nenhum processo iniciado</p>
                    </div>
                ) : (
                    <div>
                        {documents.map(doc => (
                            <div key={doc.id} className="process-card">
                                <div className="process-header">
                                    <div className="filename"><FileIcon /> {doc.filename}</div>
                                    <span className="update-time">
                                        {new Date(doc.updated_at).toLocaleTimeString()}
                                    </span>
                                </div>
                                <div className="doc-id">ID: {doc.id}</div>

                                <StatusTimeline status={doc.status} history={doc.history} />

                                {/* Admin Controls */}
                                <div className="admin-controls">
                                    <span className="label">Admin</span>

                                    {doc.status === 'RECEBIDO' && (
                                        <button className="btn-default" disabled={loading}
                                            onClick={() => handleTransition(doc.id, 'START_ANALYSIS')}>
                                            Iniciar Análise
                                        </button>
                                    )}

                                    {doc.status === 'EM_ANALISE' && (
                                        <>
                                            <button className="btn-success" disabled={loading}
                                                onClick={() => handleTransition(doc.id, 'APPROVE')}>
                                                Aprovar
                                            </button>
                                            <button className="btn-warning" disabled={loading}
                                                onClick={() => handleTransition(doc.id, 'REQUEST_DOCS')}>
                                                Solicitar Docs
                                            </button>
                                            <button className="btn-danger" disabled={loading}
                                                onClick={() => handleTransition(doc.id, 'REJECT')}>
                                                Reprovar
                                            </button>
                                        </>
                                    )}

                                    {doc.status === 'PENDENTE_DOCS' && (
                                        <button className="btn-default" disabled={loading}
                                            onClick={() => handleTransition(doc.id, 'RETRY_UPLOAD')}>
                                            Reenviar
                                        </button>
                                    )}

                                    {doc.status === 'APROVADO' && (
                                        <button className="btn-accent" disabled={loading}
                                            onClick={() => handleTransition(doc.id, 'FINALIZE')}>
                                            Finalizar
                                        </button>
                                    )}

                                    {(doc.status === 'REPROVADO' || doc.status === 'FINALIZADO') && (
                                        <span className="btn-ghost">Processo encerrado</span>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    )
}
