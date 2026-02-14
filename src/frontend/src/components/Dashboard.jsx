import { useState, useEffect } from 'react'
import axios from 'axios'
import FileUpload from './FileUpload'
import StatusTimeline from './StatusTimeline'

export default function Dashboard() {
    const [documents, setDocuments] = useState([])
    const [loading, setLoading] = useState(false)

    const fetchDocuments = async () => {
        try {
            const res = await axios.get('http://localhost:8000/api/documents/')
            setDocuments(res.data)
        } catch (err) {
            console.error(err)
        }
    }

    useEffect(() => {
        fetchDocuments()
        const interval = setInterval(fetchDocuments, 2000) // Poll for updates
        return () => clearInterval(interval)
    }, [])

    const handleUploadSuccess = (newDoc) => {
        // Immediate feedback
        fetchDocuments()
    }

    const handleTransition = async (docId, event) => {
        setLoading(true)
        try {
            await axios.post(`http://localhost:8000/api/documents/${docId}/transition?event=${event}`)
            fetchDocuments()
        } catch (err) {
            alert("Erro na transição: " + err.response?.data?.detail)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="dashboard">
            <h1 style={{ marginBottom: '2rem' }}>Painel de Acompanhamento</h1>

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
                            <div key={doc.filename} className="process-item" style={{
                                background: 'rgba(255,255,255,0.03)',
                                padding: '1.5rem',
                                borderRadius: '8px',
                                marginBottom: '1rem',
                                border: '1px solid rgba(255,255,255,0.05)'
                            }}>
                                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '1rem' }}>
                                    <strong>{doc.filename}</strong>
                                    <span style={{ color: '#94a3b8', fontSize: '0.8em' }}>
                                        Atualizado: {new Date(doc.updated_at).toLocaleTimeString()}
                                    </span>
                                </div>

                                <StatusTimeline status={doc.status} />

                                {/* ADMIN CONTROLS (Demo Only) */}
                                <div className="admin-controls" style={{
                                    marginTop: '1rem',
                                    borderTop: '1px solid rgba(255,255,255,0.1)',
                                    paddingTop: '1rem',
                                    display: 'flex',
                                    gap: '0.5rem',
                                    fontSize: '0.9em'
                                }}>
                                    <span style={{ color: '#64748b' }}>[Admin Demo] Ações:</span>
                                    {doc.status === 'RECEBIDO' && (
                                        <button onClick={() => handleTransition(doc.id || Object.keys(documents).find(key => documents[key] === doc), 'START_ANALYSIS')}>
                                            ▶ Iniciar Análise
                                        </button>
                                    )}
                                    {doc.status === 'EM_ANALISE' && (
                                        <>
                                            <button onClick={() => handleTransition(doc.id || "manual_fix", 'APPROVE')} style={{ color: '#34d399' }}>✓ Aprovar</button>
                                            <button onClick={() => handleTransition(doc.id || "manual_fix", 'REQUEST_DOCS')} style={{ color: '#facc15' }}>⚠ Solicitar Docs</button>
                                            <button onClick={() => handleTransition(doc.id || "manual_fix", 'REJECT')} style={{ color: '#ef4444' }}>✕ Reprovar</button>
                                        </>
                                    )}
                                    {doc.status === 'PENDENTE_DOCS' && (
                                        <button onClick={() => handleTransition(doc.id || "manual_fix", 'RETRY_UPLOAD')}>↻ Reenviar</button>
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
        }
        button:hover { background: rgba(255,255,255,0.2); }
      `}</style>
        </div>
    )
}
