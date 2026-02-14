import React from 'react'

// SVG Icons for each step
const CheckIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="20 6 9 17 4 12" />
  </svg>
)

const InboxIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="22 12 16 12 14 15 10 15 8 12 2 12" />
    <path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z" />
  </svg>
)

const SearchIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
  </svg>
)

const AlertIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z" />
    <line x1="12" y1="9" x2="12" y2="13" /><line x1="12" y1="17" x2="12.01" y2="17" />
  </svg>
)

const ShieldCheckIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
    <polyline points="9 12 12 15 16 10" />
  </svg>
)

const FlagIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z" />
    <line x1="4" y1="22" x2="4" y2="15" />
  </svg>
)

const XCircleIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="10" /><line x1="15" y1="9" x2="9" y2="15" /><line x1="9" y1="9" x2="15" y2="15" />
  </svg>
)

const STEPS = [
  { id: 'RECEBIDO', label: 'Recebido', icon: <InboxIcon /> },
  { id: 'EM_ANALISE', label: 'Em Análise', icon: <SearchIcon /> },
  { id: 'PENDENTE_DOCS', label: 'Pendente', icon: <AlertIcon /> },
  { id: 'APROVADO', label: 'Aprovado', icon: <ShieldCheckIcon /> },
  { id: 'FINALIZADO', label: 'Finalizado', icon: <FlagIcon /> }
]

export default function StatusTimeline({ status, history = [] }) {
  const getCurrentStepIndex = () => {
    if (status === 'REPROVADO') return 1
    return STEPS.findIndex(s => s.id === status)
  }

  const currentIdx = getCurrentStepIndex()

  return (
    <div style={{
      margin: '0.75rem 0',
      padding: '1.25rem',
      background: 'rgba(0, 0, 0, 0.25)',
      borderRadius: 'var(--radius-lg)',
      border: '1px solid var(--border-subtle)'
    }}>
      {/* Steps Track */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        position: 'relative',
        paddingBottom: '0.5rem'
      }}>
        {/* Connection Line */}
        <div style={{
          position: 'absolute',
          top: '18px',
          left: '24px',
          right: '24px',
          height: '2px',
          background: 'var(--border-subtle)',
          zIndex: 0
        }} />
        {/* Progress Line */}
        <div style={{
          position: 'absolute',
          top: '18px',
          left: '24px',
          width: currentIdx >= 0 ? `${(currentIdx / (STEPS.length - 1)) * 100}%` : '0%',
          maxWidth: 'calc(100% - 48px)',
          height: '2px',
          background: status === 'REPROVADO' ? 'var(--danger)' : 'var(--accent-gradient)',
          zIndex: 1,
          transition: 'width 0.5s ease'
        }} />

        {STEPS.map((step, idx) => {
          const isCompleted = idx < currentIdx
          const isCurrent = idx === currentIdx
          const isRejected = status === 'REPROVADO' && idx === 1

          let circleStyle = {
            width: '36px',
            height: '36px',
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            border: '2px solid var(--border-subtle)',
            background: 'var(--bg-secondary)',
            transition: 'all 0.3s ease',
            position: 'relative',
            zIndex: 2,
            color: 'var(--text-muted)'
          }

          if (isCompleted) {
            circleStyle = {
              ...circleStyle,
              background: 'var(--accent)',
              borderColor: 'var(--accent)',
              color: 'white',
              boxShadow: '0 0 12px var(--accent-glow)'
            }
          }

          if (isCurrent && !isRejected) {
            circleStyle = {
              ...circleStyle,
              borderColor: 'var(--accent)',
              color: 'var(--accent-light)',
              boxShadow: '0 0 16px var(--accent-glow)',
              animation: 'pulse 2s infinite'
            }
          }

          if (isRejected) {
            circleStyle = {
              ...circleStyle,
              borderColor: 'var(--danger)',
              color: 'var(--danger)',
              boxShadow: '0 0 12px rgba(239, 68, 68, 0.3)'
            }
          }

          return (
            <div key={step.id} style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: '0.4rem',
              opacity: (idx <= currentIdx || isCurrent) ? 1 : 0.35,
              transition: 'opacity 0.3s'
            }}>
              <div style={circleStyle}>
                {isCompleted ? <CheckIcon /> : isRejected ? <XCircleIcon /> : step.icon}
              </div>
              <span style={{
                fontSize: '0.7rem',
                color: isCurrent ? 'var(--text-primary)' : 'var(--text-muted)',
                fontWeight: isCurrent ? 600 : 400,
                fontFamily: 'var(--font-display)',
                letterSpacing: '0.01em'
              }}>
                {step.label}
              </span>
            </div>
          )
        })}
      </div>

      {/* Rejected banner */}
      {status === 'REPROVADO' && (
        <div style={{
          textAlign: 'center',
          color: 'var(--danger)',
          marginTop: '0.75rem',
          fontWeight: 600,
          fontSize: '0.85rem',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '0.4rem'
        }}>
          <XCircleIcon /> Documentação Reprovada — Contate o Suporte
        </div>
      )}

      {/* History Log */}
      {history.length > 1 && (
        <div style={{
          marginTop: '0.75rem',
          paddingTop: '0.75rem',
          borderTop: '1px solid var(--border-subtle)'
        }}>
          <div style={{
            fontSize: '0.7rem',
            color: 'var(--text-muted)',
            marginBottom: '0.4rem',
            fontWeight: 600,
            textTransform: 'uppercase',
            letterSpacing: '0.06em',
            fontFamily: 'var(--font-display)'
          }}>
            Histórico
          </div>
          {history.map((entry, idx) => (
            <div key={idx} style={{
              fontSize: '0.73rem',
              color: 'var(--text-secondary)',
              padding: '0.15rem 0',
              display: 'flex',
              gap: '0.5rem'
            }}>
              <span style={{ color: 'var(--accent-light)', fontFamily: 'monospace', fontSize: '0.68rem' }}>
                {new Date(entry.timestamp).toLocaleTimeString()}
              </span>
              <span style={{ color: 'var(--text-accent)' }}>{entry.to_status}</span>
              {entry.description && (
                <span style={{ color: 'var(--text-muted)' }}>— {entry.description}</span>
              )}
            </div>
          ))}
        </div>
      )}

      <style>{`
                @keyframes pulse {
                    0%, 100% { box-shadow: 0 0 8px var(--accent-glow); }
                    50% { box-shadow: 0 0 24px var(--accent-glow); }
                }
            `}</style>
    </div>
  )
}
