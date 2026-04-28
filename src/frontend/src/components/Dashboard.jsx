import { useState, useEffect } from 'react'
import axios from 'axios'
import FileUpload from './FileUpload'
import StatusTimeline from './StatusTimeline'

const EVENT_LABELS = {
    'RECEBIDO_TO_EM_ANALISE':      'Recebido → Em Análise',
    'EM_ANALISE_TO_APROVADO':      'Em Análise → Aprovado',
    'EM_ANALISE_TO_REPROVADO':     'Em Análise → Reprovado',
    'EM_ANALISE_TO_PENDENTE_DOCS': 'Em Análise → Pendência de Docs',
    'PENDENTE_DOCS_TO_EM_ANALISE': 'Pendência → Retomada de Análise',
    'APROVADO_TO_FINALIZADO':      'Aprovado → Finalizado',
    'DOCUMENT_UPLOADED':           'Documento Enviado',
    'STATUS_UPDATED':              'Status Atualizado',
    'NOTIFICATION_SENT':           'Notificação Enviada',
}

const translateEvent = (raw) =>
    EVENT_LABELS[raw] || raw.replace(/_/g, ' ').toLowerCase().replace(/\b\w/g, c => c.toUpperCase())

// ─── Ícones ────────────────────────────────────────────────────
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

const ShieldIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
    </svg>
)

const HeartIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" />
    </svg>
)

const ZapIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2" />
    </svg>
)

const BrainIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <path d="M9.5 2A2.5 2.5 0 0 1 12 4.5v15a2.5 2.5 0 0 1-4.96-.44 2.5 2.5 0 0 1-2.96-3.08 3 3 0 0 1-.34-5.58 2.5 2.5 0 0 1 1.32-4.24 2.5 2.5 0 0 1 1.44-4.66z" />
        <path d="M14.5 2A2.5 2.5 0 0 0 12 4.5v15a2.5 2.5 0 0 0 4.96-.44 2.5 2.5 0 0 0 2.96-3.08 3 3 0 0 0 .34-5.58 2.5 2.5 0 0 0-1.32-4.24 2.5 2.5 0 0 0-1.44-4.66z" />
    </svg>
)

const CheckIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="20 6 9 17 4 12" />
    </svg>
)

const UploadIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="16 16 12 12 8 16" /><line x1="12" y1="12" x2="12" y2="21" />
        <path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3" />
    </svg>
)

// ─── Componente Hero ───────────────────────────────────────────
function HeroSection({ hasDocuments }) {
    const pillars = [
        { icon: <HeartIcon />, label: 'Acolhimento', desc: 'Atendimento humano e empático em cada etapa do seu processo.', colorVar: 'var(--amber)',   bgVar: 'var(--hero-pillar-amber)' },
        { icon: <ZapIcon />,   label: 'Agilidade',   desc: 'Processamento inteligente que reduz o tempo de análise.',      colorVar: 'var(--accent)',  bgVar: 'var(--hero-pillar-accent)' },
        { icon: <BrainIcon />, label: 'Inteligência', desc: 'IA Gemini 2.5 analisa seus documentos com precisão e cuidado.', colorVar: 'var(--teal)',   bgVar: 'var(--hero-pillar-teal)' },
    ]

    return (
        <div className="hero-section">
            {/* Decorative glow blobs */}
            <div className="hero-blob hero-blob-accent" />
            <div className="hero-blob hero-blob-amber" />

            {/* Badge de plataforma */}
            <div className="hero-badge">
                <span className="hero-badge-dot" />
                Plataforma de Vistos com IA
            </div>

            {/* Headline */}
            <h2 className="hero-headline">
                <span className="hero-line-1">Seu visto,</span>
                <br />
                <span className="hero-line-2">cuidado com inteligência.</span>
            </h2>

            <p className="hero-desc" style={{ marginBottom: hasDocuments ? '1.75rem' : '2rem' }}>
                Envie seus documentos e acompanhe cada etapa do processo em tempo real.
                Nossa IA e equipe especializada trabalham juntas para tornar tudo mais simples.
            </p>

            {!hasDocuments && (
                <div className="hero-cta-hint">
                    <UploadIcon />
                    Comece enviando um documento ao lado →
                </div>
            )}

            {/* Pillars */}
            <div className="hero-pillars">
                {pillars.map(p => (
                    <div key={p.label} className={`hero-pillar hero-pillar-${p.label.toLowerCase()}`}>
                        <div className="hero-pillar-icon" style={{ color: p.colorVar, background: p.bgVar }}>
                            {p.icon}
                        </div>
                        <div className="hero-pillar-label">{p.label}</div>
                        <div className="hero-pillar-desc">{p.desc}</div>
                    </div>
                ))}
            </div>
        </div>
    )
}

// ─── Componente principal ──────────────────────────────────────
export default function Dashboard() {
    const [documents, setDocuments] = useState([])
    const [notifications, setNotifications] = useState([])
    const [loading, setLoading] = useState(false)
    const [showNotifications, setShowNotifications] = useState(false)
    const [isAdminMode, setIsAdminMode] = useState(false)

    const fetchDocuments = async () => {
        try {
            const res = await axios.get('http://localhost:8000/api/documents/')
            setDocuments(res.data)
        } catch { /* silencioso */ }
    }

    const fetchNotifications = async () => {
        try {
            const res = await axios.get('http://localhost:8000/api/notifications/')
            setNotifications(res.data)
        } catch { /* silencioso */ }
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
            alert('Erro na transição: ' + (err.response?.data?.detail || err.message))
        } finally {
            setLoading(false)
        }
    }

    const formatFilename = (filename) => {
        if (!filename) return ''
        const parts = filename.split('_')
        if (parts.length > 1 && parts[0].length === 36) return parts.slice(1).join('_')
        return filename
    }

    const approvedCount  = documents.filter(d => d.status === 'APROVADO' || d.status === 'FINALIZADO').length
    const pendingCount   = documents.filter(d => d.status === 'RECEBIDO' || d.status === 'EM_ANALISE').length
    const pendingDocs    = documents.filter(d => d.status === 'PENDENTE_DOCS').length

    return (
        <div className="dashboard">

            {/* ── Cabeçalho ───────────────────────────────────── */}
            <div className="page-header">
                <div style={{ display: 'flex', alignItems: 'center', gap: '1.2rem' }}>
                    <h1>Painel de Acompanhamento</h1>
                    <div
                        className={`admin-switch ${isAdminMode ? 'active' : ''}`}
                        onClick={() => setIsAdminMode(!isAdminMode)}
                        title={isAdminMode ? 'Desativar modo administrador' : 'Ativar modo administrador'}
                    >
                        <div className="switch-track"><div className="switch-thumb" /></div>
                        <span style={{
                            fontWeight: isAdminMode ? 700 : 400,
                            color: isAdminMode ? 'var(--amber)' : 'inherit',
                            fontSize: '0.84rem', fontFamily: 'var(--font-display)',
                        }}>
                            Modo Admin
                        </span>
                    </div>
                </div>

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

            {/* ── Banner Admin ────────────────────────────────── */}
            {isAdminMode && (
                <div className="admin-banner">
                    <ShieldIcon />
                    MODO ADMINISTRADOR ATIVO — avance o status dos processos manualmente pelos cards abaixo
                </div>
            )}

            {/* ── Painel Notificações ─────────────────────────── */}
            {showNotifications && (
                <div className="card notification-panel" style={{ marginBottom: 'var(--space-lg)' }}>
                    <h3>Últimas Notificações</h3>
                    {notifications.length === 0 ? (
                        <div className="empty-state"><InboxIcon /><p>Nenhuma notificação ainda</p></div>
                    ) : (
                        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', maxHeight: '260px', overflowY: 'auto' }}>
                            {notifications.slice().reverse().map((n, i) => (
                                <div key={i} className="notification-item">
                                    <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.15rem' }}>
                                        <span className="event-type">{translateEvent(n.event_type)}</span>
                                        <span className="time">{new Date(n.sent_at).toLocaleTimeString('pt-BR')}</span>
                                    </div>
                                    <p className="message-text">{n.message}</p>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            )}

            {/* ── Hero ────────────────────────────────────────── */}
            <HeroSection hasDocuments={documents.length > 0} />

            {/* ── Stats rápidas (só quando há processos) ──────── */}
            {documents.length > 0 && (
                <div style={{
                    display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)',
                    gap: 'var(--space-md)', marginBottom: 'var(--space-xl)',
                }}>
                    {[
                        { label: 'Processos totais',   value: documents.length, color: 'var(--accent-light)', bg: 'rgba(139,120,245,0.1)' },
                        { label: 'Em andamento',        value: pendingCount,    color: 'var(--amber)',        bg: 'rgba(245,167,58,0.1)' },
                        { label: 'Aprovados',           value: approvedCount,   color: 'var(--teal)',         bg: 'rgba(46,207,207,0.1)' },
                    ].map(s => (
                        <div key={s.label} style={{
                            background: s.bg, border: `1px solid ${s.color}33`,
                            borderRadius: 'var(--radius-lg)', padding: '1.1rem 1.3rem',
                            display: 'flex', flexDirection: 'column', gap: '0.25rem',
                        }}>
                            <span style={{
                                fontFamily: 'var(--font-display)', fontSize: '2rem',
                                fontWeight: 800, color: s.color, lineHeight: 1,
                            }}>{s.value}</span>
                            <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>{s.label}</span>
                        </div>
                    ))}
                </div>
            )}

            {/* ── Grid Principal ──────────────────────────────── */}
            <div className="dashboard-grid">
                <div className="grid-main">

                    {/* Alerta pendência */}
                    {pendingDocs > 0 && (
                        <div style={{
                            display: 'flex', alignItems: 'center', gap: '0.75rem',
                            background: 'rgba(245,167,58,0.08)', border: '1px solid rgba(245,167,58,0.3)',
                            borderRadius: 'var(--radius-md)', padding: '0.85rem 1.1rem',
                            marginBottom: 'var(--space-md)',
                            fontSize: '0.88rem', color: 'var(--amber)',
                            fontFamily: 'var(--font-display)', fontWeight: 600,
                        }}>
                            ⚠ {pendingDocs} processo{pendingDocs > 1 ? 's' : ''} aguardando reenvio de documentos
                        </div>
                    )}

                    <div className="card">
                        <h3>Meus Processos</h3>
                        {documents.length === 0 ? (
                            <div className="empty-state" style={{ padding: '2.5rem' }}>
                                <InboxIcon />
                                <p style={{ marginBottom: '0.4rem', fontWeight: 600 }}>Nenhum processo iniciado</p>
                                <p style={{ fontSize: '0.82rem' }}>
                                    Envie um documento pelo painel ao lado para começar
                                </p>
                            </div>
                        ) : (
                            documents.map(doc => (
                                <div
                                    key={doc.id}
                                    className="process-card"
                                    style={isAdminMode ? {
                                        borderColor: 'rgba(245,167,58,0.22)',
                                        boxShadow: '0 0 0 1px rgba(245,167,58,0.08)',
                                    } : {}}
                                >
                                    <div className="process-header">
                                        <div className="filename"><FileIcon /> {formatFilename(doc.filename)}</div>
                                        <span className="update-time">
                                            Atualizado às {new Date(doc.updated_at).toLocaleTimeString('pt-BR')}
                                        </span>
                                    </div>
                                    <div className="doc-id">Protocolo: {doc.id}</div>

                                    <StatusTimeline status={doc.status} history={doc.history} />

                                    {/* Controles Admin */}
                                    {isAdminMode && (
                                        <div className="admin-controls">
                                            <span className="label">Ações do Administrador</span>
                                            <div className="admin-controls-btns">
                                                {doc.status === 'RECEBIDO' && (
                                                    <button className="btn-default" disabled={loading}
                                                        onClick={() => handleTransition(doc.id, 'START_ANALYSIS')}>
                                                        ▶ Iniciar Análise
                                                    </button>
                                                )}
                                                {doc.status === 'EM_ANALISE' && (<>
                                                    <button className="btn-success" disabled={loading}
                                                        onClick={() => handleTransition(doc.id, 'APPROVE')}>
                                                        ✓ Aprovar
                                                    </button>
                                                    <button className="btn-warning" disabled={loading}
                                                        onClick={() => handleTransition(doc.id, 'REQUEST_DOCS')}>
                                                        ⚠ Solicitar Docs
                                                    </button>
                                                    <button className="btn-danger" disabled={loading}
                                                        onClick={() => handleTransition(doc.id, 'REJECT')}>
                                                        ✕ Reprovar
                                                    </button>
                                                </>)}
                                                {doc.status === 'PENDENTE_DOCS' && (
                                                    <button className="btn-default" disabled={loading}
                                                        onClick={() => handleTransition(doc.id, 'RETRY_UPLOAD')}>
                                                        ↻ Marcar como Reenviado
                                                    </button>
                                                )}
                                                {doc.status === 'APROVADO' && (
                                                    <button className="btn-accent" disabled={loading}
                                                        onClick={() => handleTransition(doc.id, 'FINALIZE')}>
                                                        ⚑ Finalizar Processo
                                                    </button>
                                                )}
                                                {(doc.status === 'REPROVADO' || doc.status === 'FINALIZADO') && (
                                                    <span className="btn-ghost" style={{ padding: '0.4rem 0' }}>Processo encerrado</span>
                                                )}
                                            </div>
                                        </div>
                                    )}
                                </div>
                            ))
                        )}
                    </div>
                </div>

                {/* ── Sidebar: Upload ──────────────────────────── */}
                <div className="grid-sidebar">
                    <div className="card upload-card" style={{ borderColor: 'rgba(139,120,245,0.22)' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: 'var(--space-md)' }}>
                            <div style={{
                                width: '32px', height: '32px', borderRadius: 'var(--radius-md)',
                                background: 'rgba(139,120,245,0.15)', color: 'var(--accent-light)',
                                display: 'flex', alignItems: 'center', justifyContent: 'center',
                            }}>
                                <UploadIcon />
                            </div>
                            <h3 style={{ margin: 0 }}>Novo Processo</h3>
                        </div>
                        <FileUpload onUploadSuccess={handleUploadSuccess} />
                        <div style={{ marginTop: '1rem' }}>
                            {[
                                'Análise automática por IA',
                                'Notificação em tempo real',
                                'Histórico completo salvo',
                            ].map(item => (
                                <div key={item} style={{
                                    display: 'flex', alignItems: 'center', gap: '0.5rem',
                                    fontSize: '0.78rem', color: 'var(--text-muted)',
                                    padding: '0.25rem 0',
                                }}>
                                    <span style={{ color: 'var(--teal)', flexShrink: 0 }}><CheckIcon /></span>
                                    {item}
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
