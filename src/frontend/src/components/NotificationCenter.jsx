import { useState, useEffect } from 'react'
import axios from 'axios'

// SVG Icons
const MailIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <rect x="2" y="4" width="20" height="16" rx="2" />
        <path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7" />
    </svg>
)

const PhoneIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
        <rect x="5" y="2" width="14" height="20" rx="2" ry="2" />
        <line x1="12" y1="18" x2="12.01" y2="18" />
    </svg>
)

const CheckCircleIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
        <polyline points="22 4 12 14.01 9 11.01" />
    </svg>
)

const ServerIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <rect x="2" y="2" width="20" height="8" rx="2" ry="2" />
        <rect x="2" y="14" width="20" height="8" rx="2" ry="2" />
        <line x1="6" y1="6" x2="6.01" y2="6" />
        <line x1="6" y1="18" x2="6.01" y2="18" />
    </svg>
)

const InboxIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="22 12 16 12 14 15 10 15 8 12 2 12" />
        <path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z" />
    </svg>
)

const RefreshIcon = () => (
    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
        <polyline points="23 4 23 10 17 10" />
        <path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10" />
    </svg>
)

export default function NotificationCenter() {
    const [notifications, setNotifications] = useState([])
    const [filter, setFilter] = useState('all') // all, email, sms
    const [loading, setLoading] = useState(true)

    const fetchNotifications = async () => {
        try {
            const res = await axios.get('http://localhost:8000/api/notifications/')
            setNotifications(res.data)
        } catch { /* silent */ }
        finally { setLoading(false) }
    }

    useEffect(() => {
        fetchNotifications()
        const interval = setInterval(fetchNotifications, 3000)
        return () => clearInterval(interval)
    }, [])

    const filtered = filter === 'all'
        ? notifications
        : notifications.filter(n => n.channel === filter)

    const emailCount = notifications.filter(n => n.channel === 'email').length
    const smsCount = notifications.filter(n => n.channel === 'sms').length

    return (
        <div className="notification-center">
            <div className="nc-header">
                <div>
                    <h1>Central de Notificações</h1>
                    <p className="nc-subtitle">Monitoramento de envios simulados de e-mail e SMS</p>
                </div>
                <button className="nc-refresh" onClick={fetchNotifications} aria-label="Atualizar">
                    <RefreshIcon /> Atualizar
                </button>
            </div>

            {/* Stats Row */}
            <div className="nc-stats">
                <div className="nc-stat-card">
                    <div className="nc-stat-icon email"><MailIcon /></div>
                    <div>
                        <div className="nc-stat-value">{emailCount}</div>
                        <div className="nc-stat-label">E-mails Enviados</div>
                    </div>
                </div>
                <div className="nc-stat-card">
                    <div className="nc-stat-icon sms"><PhoneIcon /></div>
                    <div>
                        <div className="nc-stat-value">{smsCount}</div>
                        <div className="nc-stat-label">SMS Enviados</div>
                    </div>
                </div>
                <div className="nc-stat-card">
                    <div className="nc-stat-icon total"><ServerIcon /></div>
                    <div>
                        <div className="nc-stat-value">{notifications.length}</div>
                        <div className="nc-stat-label">Total Disparados</div>
                    </div>
                </div>
            </div>

            {/* Filter Tabs */}
            <div className="nc-filters">
                <button className={filter === 'all' ? 'active' : ''} onClick={() => setFilter('all')}>
                    Todos ({notifications.length})
                </button>
                <button className={filter === 'email' ? 'active' : ''} onClick={() => setFilter('email')}>
                    <MailIcon /> E-mail ({emailCount})
                </button>
                <button className={filter === 'sms' ? 'active' : ''} onClick={() => setFilter('sms')}>
                    <PhoneIcon /> SMS ({smsCount})
                </button>
            </div>

            {/* Notification List */}
            <div className="nc-list">
                {loading ? (
                    <div className="empty-state">
                        <p>Carregando...</p>
                    </div>
                ) : filtered.length === 0 ? (
                    <div className="empty-state">
                        <InboxIcon />
                        <p>Nenhuma notificação registrada</p>
                        <p style={{ fontSize: '0.8rem', marginTop: '0.5rem' }}>
                            Faça upload de um documento para gerar notificações automáticas
                        </p>
                    </div>
                ) : (
                    filtered.slice().reverse().map((notif, idx) => (
                        <div
                            key={notif.id || idx}
                            className={`nc-card ${notif.channel}`}
                            style={{ animationDelay: `${idx * 0.05}s` }}
                        >
                            {/* Card Header */}
                            <div className="nc-card-header">
                                <div className="nc-card-channel">
                                    <span className={`nc-channel-badge ${notif.channel}`}>
                                        {notif.channel === 'email' ? <MailIcon /> : <PhoneIcon />}
                                        {notif.channel === 'email' ? 'E-MAIL' : 'SMS'}
                                    </span>
                                    <span className="nc-delivery-badge">
                                        <CheckCircleIcon />
                                        Entregue
                                    </span>
                                </div>
                                <span className="nc-card-time">
                                    {new Date(notif.sent_at).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                                </span>
                            </div>

                            {/* Email style */}
                            {notif.channel === 'email' && (
                                <div className="nc-email-body">
                                    <div className="nc-email-subject">{notif.subject}</div>
                                    <div className="nc-email-meta">
                                        <div><span className="nc-label">De:</span> {notif.sender}</div>
                                        <div><span className="nc-label">Para:</span> {notif.recipient}</div>
                                    </div>
                                    <div className="nc-email-content">
                                        {notif.body}
                                    </div>
                                    <div className="nc-email-footer">
                                        <span className="nc-provider"><ServerIcon /> {notif.provider}</span>
                                        <span className="nc-event-tag">{notif.event_type}</span>
                                    </div>
                                </div>
                            )}

                            {/* SMS style */}
                            {notif.channel === 'sms' && (
                                <div className="nc-sms-body">
                                    <div className="nc-sms-header">
                                        <div className="nc-sms-sender">{notif.sender}</div>
                                        <div className="nc-sms-recipient">{notif.recipient}</div>
                                    </div>
                                    <div className="nc-sms-bubble">
                                        {notif.body}
                                    </div>
                                    <div className="nc-email-footer">
                                        <span className="nc-provider"><ServerIcon /> {notif.provider}</span>
                                        <span className="nc-event-tag">{notif.event_type}</span>
                                    </div>
                                </div>
                            )}
                        </div>
                    ))
                )}
            </div>
        </div>
    )
}
