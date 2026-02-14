import { useState } from 'react'
import axios from 'axios'
import FileUpload from './FileUpload'

export default function Dashboard() {
    const [documents, setDocuments] = useState([])

    const handleUploadSuccess = (newDoc) => {
        setDocuments(prev => [newDoc, ...prev])
    }

    return (
        <div className="dashboard">
            <h1 style={{ marginBottom: '2rem' }}>Painel de Controle</h1>

            <div className="card">
                <h3>Novo Documento</h3>
                <p style={{ color: '#94a3b8', marginBottom: '1rem' }}>
                    Arraste documentos para iniciar a análise automática (IA + Vision).
                </p>
                <FileUpload onUploadSuccess={handleUploadSuccess} />
            </div>

            <div className="card">
                <h3>Documentos Processados</h3>
                <div className="doc-list">
                    {documents.length === 0 ? (
                        <p style={{ color: '#94a3b8' }}>Nenhum documento processado ainda.</p>
                    ) : (
                        <table style={{ width: '100%', textAlign: 'left', marginTop: '1rem' }}>
                            <thead>
                                <tr style={{ color: '#94a3b8' }}>
                                    <th>Arquivo</th>
                                    <th>Status</th>
                                    <th>Confiança IA</th>
                                    <th>Automação</th>
                                </tr>
                            </thead>
                            <tbody>
                                {documents.map(doc => (
                                    <tr key={doc.id} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                                        <td style={{ padding: '1rem 0' }}>{doc.filename}</td>
                                        <td>
                                            <span style={{
                                                background: 'rgba(16, 185, 129, 0.2)',
                                                color: '#34d399',
                                                padding: '0.2rem 0.6rem',
                                                borderRadius: '4px',
                                                fontSize: '0.9em'
                                            }}>
                                                {doc.status}
                                            </span>
                                        </td>
                                        <td>{(doc.cv_validation?.confidence * 100).toFixed(0)}%</td>
                                        <td>{doc.automation?.sent ? '✅ Email Enviado' : '❌ Falha'}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    )}
                </div>
            </div>
        </div>
    )
}
