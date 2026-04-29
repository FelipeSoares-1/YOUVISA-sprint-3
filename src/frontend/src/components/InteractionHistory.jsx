import { useState, useEffect, useCallback } from 'react'
import axios from 'axios'

const API = 'http://localhost:8000/api'

const INTENT_META = {
  STATUS_QUERY:    { label: 'Status',       color: '#6366f1', bg: 'rgba(99,102,241,0.12)' },
  MISSING_DOCS:    { label: 'Docs',          color: '#f59e0b', bg: 'rgba(245,158,11,0.12)' },
  NEXT_STEP:       { label: 'Próximo Passo', color: '#06b6d4', bg: 'rgba(6,182,212,0.12)' },
  DEADLINE:        { label: 'Prazo',         color: '#a78bfa', bg: 'rgba(167,139,250,0.12)' },
  APPROVAL_STATUS: { label: 'Aprovação',     color: '#10b981', bg: 'rgba(16,185,129,0.12)' },
  DOCUMENT_INFO:   { label: 'Documento',     color: '#f472b6', bg: 'rgba(244,114,182,0.12)' },
  GREETING:        { label: 'Saudação',      color: '#94a3b8', bg: 'rgba(148,163,184,0.12)' },
  HELP:            { label: 'Ajuda',         color: '#fb923c', bg: 'rgba(251,146,60,0.12)'  },
  GENERAL:         { label: 'Geral',         color: '#64748b', bg: 'rgba(100,116,139,0.12)' },
}

function IntentBadge({ intent, confidence }) {
  const meta = INTENT_META[intent] || INTENT_META.GENERAL
  return (
    <span style={{
      display: 'inline-flex', alignItems: 'center', gap: '0.3rem',
      fontSize: '0.7rem', fontWeight: 600, letterSpacing: '0.04em',
      padding: '0.18rem 0.55rem', borderRadius: '4px',
      color: meta.color, background: meta.bg,
      border: `1px solid ${meta.color}30`,
    }}>
      {meta.label}
      <span style={{ opacity: 0.7, fontWeight: 400 }}>
        {Math.round(confidence * 100)}%
      </span>
    </span>
  )
}

function AgentTrace({ trace }) {
  const [open, setOpen] = useState(false)
  if (!trace || trace.length === 0) return null
  return (
    <div style={{ marginTop: '0.5rem' }}>
      <button
        onClick={() => setOpen(o => !o)}
        style={{
          all: 'unset', cursor: 'pointer', fontSize: '0.72rem',
          color: 'var(--text-muted)', display: 'flex', alignItems: 'center', gap: '0.3rem',
        }}
      >
        <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"
          style={{ transform: open ? 'rotate(90deg)' : 'none', transition: 'transform 0.2s' }}>
          <polyline points="9 18 15 12 9 6" />
        </svg>
        {open ? 'Ocultar' : 'Ver'} trace dos agentes
      </button>
      {open && (
        <div style={{
          marginTop: '0.5rem', padding: '0.75rem',
          background: 'var(--bg-elevated)', borderRadius: '8px',
          border: '1px solid var(--border-subtle)', fontSize: '0.75rem',
          display: 'flex', flexDirection: 'column', gap: '0.5rem',
        }}>
          {trace.map((step, i) => (
            <div key={i} style={{ display: 'flex', gap: '0.75rem', alignItems: 'flex-start' }}>
              <span style={{
                minWidth: '22px', height: '22px', borderRadius: '50%',
                background: 'var(--nav-active-bg)', color: 'var(--accent)',
                display: 'flex', alignItems: 'center', justifyContent: 'center',
                fontSize: '0.65rem', fontWeight: 700, flexShrink: 0,
              }}>{i + 1}</span>
              <div>
                <div style={{ color: 'var(--accent)', fontWeight: 600, marginBottom: '0.15rem' }}>
                  {step.agent}
                </div>
                <div style={{ color: 'var(--text-muted)', lineHeight: 1.5 }}>
                  {Object.entries(step.output || {}).map(([k, v]) => (
                    <span key={k} style={{ marginRight: '0.75rem' }}>
                      <span style={{ color: 'var(--text-secondary)' }}>{k}:</span>{' '}
                      <span>{typeof v === 'boolean' ? (v ? 'sim' : 'não') : String(v ?? '—')}</span>
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

function InteractionCard({ log, isAdminMode }) {
  const ts = new Date(log.timestamp)
  const timeStr = ts.toLocaleString('pt-BR', { hour: '2-digit', minute: '2-digit', day: '2-digit', month: '2-digit' })
  const entities = log.entities || {}
  const hasEntities = Object.values(entities).some(Boolean)

  return (
    <div style={{
      background: 'var(--bg-card)', border: '1px solid var(--border-subtle)',
      borderRadius: '12px', overflow: 'hidden',
      animation: 'ncCardIn 0.3s ease-out both',
    }}>
      {/* Header */}
      <div style={{
        display: 'flex', justifyContent: 'space-between', alignItems: 'center',
        padding: '0.6rem 1rem', background: 'var(--surface-glass)',
        borderBottom: '1px solid var(--border-subtle)',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
          <IntentBadge intent={log.detected_intent} confidence={log.intent_confidence} />
          {log.session_id && (
            <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)', fontFamily: 'monospace' }}>
              sess: {log.session_id.slice(0, 8)}
            </span>
          )}
        </div>
        <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)', fontFamily: 'monospace' }}>
          {timeStr}
        </span>
      </div>

      {/* Body */}
      <div style={{ padding: '0.85rem 1rem' }}>
        {/* User message */}
        <div style={{ marginBottom: '0.65rem' }}>
          <span style={{
            fontSize: '0.7rem', fontWeight: 600, color: 'var(--text-muted)',
            textTransform: 'uppercase', letterSpacing: '0.06em',
          }}>Usuário</span>
          <div style={{
            marginTop: '0.25rem', padding: '0.6rem 0.85rem',
            background: 'rgba(99,102,241,0.08)', borderRadius: '8px',
            borderLeft: '3px solid var(--accent)', fontSize: '0.88rem',
            color: 'var(--text-primary)', lineHeight: 1.55,
          }}>
            {log.user_message}
          </div>
        </div>

        {/* Entities */}
        {hasEntities && (
          <div style={{ marginBottom: '0.65rem', display: 'flex', gap: '0.4rem', flexWrap: 'wrap' }}>
            {Object.entries(entities).map(([k, v]) => v ? (
              <span key={k} style={{
                fontSize: '0.68rem', padding: '0.1rem 0.45rem', borderRadius: '4px',
                background: 'rgba(13,148,136,0.07)', color: 'var(--teal)',
                border: '1px solid rgba(13,148,136,0.18)',
              }}>
                {k}: {v}
              </span>
            ) : null)}
          </div>
        )}

        {/* Response */}
        <div>
          <span style={{
            fontSize: '0.7rem', fontWeight: 600, color: 'var(--text-muted)',
            textTransform: 'uppercase', letterSpacing: '0.06em',
          }}>Valéria</span>
          <div style={{
            marginTop: '0.25rem', padding: '0.6rem 0.85rem',
            background: 'var(--surface-glass)', borderRadius: '8px',
            borderLeft: '3px solid var(--border-subtle)', fontSize: '0.88rem',
            color: 'var(--text-secondary)', lineHeight: 1.6,
          }}>
            {log.response}
          </div>
        </div>

        {/* Agent trace — visível apenas em modo administrador */}
        {isAdminMode && <AgentTrace trace={log.agent_trace} />}
      </div>
    </div>
  )
}

function StatsBar({ logs }) {
  if (!logs.length) return null

  const intentCounts = {}
  let totalConf = 0
  for (const l of logs) {
    intentCounts[l.detected_intent] = (intentCounts[l.detected_intent] || 0) + 1
    totalConf += l.intent_confidence || 0
  }
  const topIntent = Object.entries(intentCounts).sort((a, b) => b[1] - a[1])[0]
  const avgConf = Math.round((totalConf / logs.length) * 100)

  return (
    <div style={{
      display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: '0.75rem',
      marginBottom: '1.25rem',
    }}>
      {[
        { label: 'Interações', value: logs.length, color: 'var(--accent)' },
        { label: 'Intent mais freq.', value: topIntent ? INTENT_META[topIntent[0]]?.label || topIntent[0] : '—', color: 'var(--info)' },
        { label: 'Confiança média', value: `${avgConf}%`, color: 'var(--success)' },
      ].map(s => (
        <div key={s.label} style={{
          background: 'var(--bg-card)', border: '1px solid var(--border-subtle)',
          borderRadius: '10px', padding: '0.85rem 1rem',
        }}>
          <div style={{ fontSize: '1.4rem', fontWeight: 700, color: s.color, fontFamily: 'var(--font-display)' }}>
            {s.value}
          </div>
          <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.1rem' }}>
            {s.label}
          </div>
        </div>
      ))}
    </div>
  )
}

export default function InteractionHistory({ isAdminMode = false }) {
  const [logs, setLogs] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [intentFilter, setIntentFilter] = useState('ALL')

  const load = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const { data } = await axios.get(`${API}/interactions/?limit=200`)
      setLogs(data)
    } catch {
      setError('Não foi possível carregar o histórico. Verifique se o backend está rodando.')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => { load() }, [load])

  const intents = ['ALL', ...Object.keys(INTENT_META)]
  const filtered = intentFilter === 'ALL' ? logs : logs.filter(l => l.detected_intent === intentFilter)

  return (
    <div style={{ maxWidth: '860px', margin: '0 auto' }}>
      {/* Page header */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1.5rem' }}>
        <div>
          <h1 style={{
            fontFamily: 'var(--font-display)', fontSize: '1.75rem', fontWeight: 700,
            letterSpacing: '-0.03em',
            background: 'linear-gradient(135deg, var(--text-primary), var(--text-secondary))',
            WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', backgroundClip: 'text',
          }}>
            Histórico de Interações
          </h1>
          <p style={{ color: 'var(--text-muted)', fontSize: '0.85rem', marginTop: '0.25rem' }}>
            Logs persistidos com intent, entidades e trace dos agentes
          </p>
        </div>
        <button
          onClick={load}
          style={{
            all: 'unset', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '0.4rem',
            padding: '0.5rem 1rem', background: 'var(--bg-card)', border: '1px solid var(--border-subtle)',
            borderRadius: '8px', color: 'var(--text-secondary)', fontSize: '0.82rem',
            transition: 'all 0.2s',
          }}
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"
            style={{ animation: loading ? 'spin 1s linear infinite' : 'none' }}>
            <polyline points="23 4 23 10 17 10" /><polyline points="1 20 1 14 7 14" />
            <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15" />
          </svg>
          Atualizar
        </button>
      </div>

      {/* Admin mode notice */}
      {isAdminMode && (
        <div style={{
          marginBottom: '1rem', padding: '0.6rem 1rem',
          background: 'rgba(217,119,6,0.08)', border: '1px solid rgba(217,119,6,0.25)',
          borderRadius: '8px', fontSize: '0.8rem', color: 'var(--amber)',
          display: 'flex', alignItems: 'center', gap: '0.5rem',
        }}>
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          Modo administrador ativo — agent trace visível
        </div>
      )}

      {/* Stats */}
      <StatsBar logs={logs} />

      {/* Intent filter */}
      <div style={{
        display: 'flex', gap: '0.25rem', flexWrap: 'wrap',
        background: 'var(--bg-card)', border: '1px solid var(--border-subtle)',
        borderRadius: '8px', padding: '4px', marginBottom: '1.25rem',
      }}>
        {intents.map(intent => {
          const meta = intent === 'ALL' ? { label: 'Todos', color: 'var(--text-secondary)', bg: 'transparent' } : INTENT_META[intent]
          const active = intentFilter === intent
          return (
            <button
              key={intent}
              onClick={() => setIntentFilter(intent)}
              style={{
                all: 'unset', cursor: 'pointer', fontSize: '0.78rem', padding: '0.4rem 0.8rem',
                borderRadius: '6px', transition: 'all 0.15s', fontWeight: active ? 600 : 400,
                background: active ? (intent === 'ALL' ? 'var(--nav-active-bg)' : meta.bg) : 'transparent',
                color: active ? (intent === 'ALL' ? 'var(--accent)' : meta.color) : 'var(--text-muted)',
              }}
            >
              {meta.label}
            </button>
          )
        })}
      </div>

      {/* Content */}
      {error && (
        <div style={{
          padding: '1rem', background: 'rgba(239,68,68,0.08)', border: '1px solid rgba(239,68,68,0.2)',
          borderRadius: '10px', color: 'var(--danger)', fontSize: '0.88rem', marginBottom: '1rem',
        }}>
          {error}
        </div>
      )}

      {!loading && filtered.length === 0 && !error && (
        <div style={{ textAlign: 'center', padding: '4rem 2rem', color: 'var(--text-muted)' }}>
          <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.2"
            style={{ marginBottom: '1rem', opacity: 0.3, display: 'block', margin: '0 auto 1rem' }}>
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
          </svg>
          <p style={{ fontSize: '0.9rem' }}>
            {intentFilter === 'ALL' ? 'Nenhuma interação registrada ainda.' : `Nenhuma interação com intent "${INTENT_META[intentFilter]?.label}".`}
          </p>
          <p style={{ fontSize: '0.8rem', marginTop: '0.4rem', opacity: 0.7 }}>
            Inicie uma conversa no Atendimento Inteligente para ver os logs aqui.
          </p>
        </div>
      )}

      <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
        {filtered.map(log => (
          <InteractionCard key={log.id} log={log} isAdminMode={isAdminMode} />
        ))}
      </div>

      <style>{`
        @keyframes spin { to { transform: rotate(360deg); } }
        @keyframes ncCardIn {
          from { opacity: 0; transform: translateY(10px); }
          to   { opacity: 1; transform: translateY(0); }
        }
      `}</style>
    </div>
  )
}
