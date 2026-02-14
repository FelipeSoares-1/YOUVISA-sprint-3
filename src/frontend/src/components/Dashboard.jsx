import { useState, useEffect } from 'react'
import axios from 'axios'
import FileUpload from './FileUpload'
import StatusTimeline from './StatusTimeline'

export default function Dashboard() {
    const [documents, setDocuments] = useState([])
    const [notifications, setNotifications] = useState([])
    const [loading, setLoading] = useState(false)
    const [showNotifications, setShowNotifications] = useState(false)

    const fetchDocuments = async () => {
        try {
            const res = await axios.get('http://localhost:8000/api/documents/')
            setDocuments(res.data)
        } catch (err) {
            console.error(err)
        }
    }

    const fetchNotifications = async () => {
        try {
            const res = await axios.get('http://localhost:8000/api/notifications/')
            setNotifications(res.data)
        } catch (err) {
            console.error(err)
        }
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
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                <h1>Painel de Acompanhamento</h1>
                <button
                    className="notification-bell"
                    onClick={() => setShowNotifications(!showNotifications)}
                    style={{
                        background: 'rgba(99, 102, 241, 0.2)',
                        border: '1px solid rgba(99, 102, 241, 0.4)',
                        color: 'white',
                        padding: '0.5rem 1rem',
                        borderRadius: '8px',
                        cursor: 'pointer',
                        position: 'relative',
                        fontSize: '0.9em'
                    }}
                >
                    🔔 Notificações
                    {notifications.length > 0 && (
                        <span style={{
                            position: 'absolute',
                            top: '-6px',
                            right: '-6px',
                            background: '#ef4444',
                            color: 'white',
                            borderRadius: '50%',
                            width: '20px',
                            height: '20px',
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            fontSize: '0.7em',
                            fontWeight: 'bold'
                        }}>
                            {notifications.length}
                        </span>
                    )}
                </button>
            </div>

            {/* Notifications Panel */}
            {showNotifications && (
                <div className="card" style={{
                    marginBottom: '1.5rem',
                    border: '1px solid rgba(99, 102, 241, 0.3)',
                    maxHeight: '300px',
                    overflowY: 'auto'
                }}>
                    <h3 style={{ marginBottom: '1rem' }}>📧 Central de Notificações</h3>
                    {notifications.length === 0 ? (
                        <p style={{ color: '#94a3b8' }}>Nenhuma notificação ainda.</p>
                    ) : (
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                            {notifications.slice().reverse().map((notif, idx) => (
                                <div key={idx} style={{
                                    background: 'rgba(255,255,255,0.03)',
                                    padding: '0.8rem 1rem',
                                    borderRadius: '6px',
                                    borderLeft: '3px solid var(--accent)',
                                    fontSize: '0.85em'
                                }}>
                                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.3rem' }}>
                                        <strong style={{ color: '#c4b5fd' }}>{notif.event_type}</strong>
                                        <span style={{ color: '#64748b', fontSize: '0.8em' }}>
                                            {new Date(notif.sent_at).toLocaleTimeString()}
                                        </span>
                                    </div>
                                    <p style={{ margin: 0, color: '#cbd5e1' }}>{notif.message}</p>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            )}

            <div className="card">
                <h3>Novo Processo</h3>
                <FileUpload onUploadSuccess={handleUploadSuccess} />
            </div>

            <div className="card">
                <h3>Seus Processos</h3>
                {documents.length === 0 ? (
                    <p style={{ color: '#94a3b8' }}>Nenhum processo iniciado.</p>
                ) : (
                    <div className="processes-list">
                        {documents.map(doc => (
                            <div key={doc.id} className="process-item" style={{
                                background: 'rgba(255,255,255,0.03)',
                                padding: '1.5rem',
                                borderRadius: '8px',
                                marginBottom: '1rem',
                                border: '1px solid rgba(255,255,255,0.05)'
                            }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                                    <strong>📄 {doc.filename}</strong>
                                    <span style={{ color: '#94a3b8', fontSize: '0.8em' }}>
                                        Atualizado: {new Date(doc.updated_at).toLocaleTimeString()}
                                    </span>
                                </div>
                                <div style={{ fontSize: '0.75em', color: '#64748b', marginBottom: '0.8rem' }}>
                                    ID: {doc.id}
                                </div>

                                <StatusTimeline status={doc.status} history={doc.history} />

                                {/* Admin Controls */}
                                <div className="admin-controls" style={{
                                    marginTop: '1rem',
                                    borderTop: '1px solid rgba(255,255,255,0.1)',
                                    paddingTop: '1rem',
                                    display: 'flex',
                                    gap: '0.5rem',
                                    fontSize: '0.9em',
                                    flexWrap: 'wrap'
                                }}>
                                    <span style={{ color: '#64748b' }}>[Admin] Ações:</span>
                                    {doc.status === 'RECEBIDO' && (
                                        <button disabled={loading} onClick={() => handleTransition(doc.id, 'START_ANALYSIS')}>
                                            ▶ Iniciar Análise
                                        </button>
                                    )}
                                    {doc.status === 'EM_ANALISE' && (
                                        <>
                                            <button disabled={loading} onClick={() => handleTransition(doc.id, 'APPROVE')} style={{ color: '#34d399' }}>✓ Aprovar</button>
                                            <button disabled={loading} onClick={() => handleTransition(doc.id, 'REQUEST_DOCS')} style={{ color: '#facc15' }}>⚠ Solicitar Docs</button>
                                            <button disabled={loading} onClick={() => handleTransition(doc.id, 'REJECT')} style={{ color: '#ef4444' }}>✕ Reprovar</button>
                                        </>
                                    )}
                                    {doc.status === 'PENDENTE_DOCS' && (
                                        <button disabled={loading} onClick={() => handleTransition(doc.id, 'RETRY_UPLOAD')}>↻ Reenviar</button>
                                    )}
                                    {doc.status === 'APROVADO' && (
                                        <button disabled={loading} onClick={() => handleTransition(doc.id, 'FINALIZE')} style={{ color: '#818cf8' }}>🏁 Finalizar</button>
                                    )}
                                    {(doc.status === 'REPROVADO' || doc.status === 'FINALIZADO') && (
                                        <span style={{ color: '#94a3b8', fontStyle: 'italic' }}>Processo encerrado</span>
                                    )}
                                </div>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            <style>{`
        button {
          background: rgba(255,255,255,0.1);
          border: none;
          color: white;
          padding: 0.3rem 0.8rem;
          border-radius: 4px;
          cursor: pointer;
          transition: background 0.2s;
        }
        button:hover { background: rgba(255,255,255,0.2); }
        button:disabled { opacity: 0.5; cursor: not-allowed; }
      `}</style>
        </div>
    )
}
