import React from 'react'

const CheckIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="20 6 9 17 4 12" />
  </svg>
)

const InboxIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <polyline points="22 12 16 12 14 15 10 15 8 12 2 12" />
    <path d="M5.45 5.11 2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z" />
  </svg>
)

const SearchIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" />
  </svg>
)

const AlertIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z" />
    <line x1="12" y1="9" x2="12" y2="13" /><line x1="12" y1="17" x2="12.01" y2="17" />
  </svg>
)

const ShieldCheckIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
    <polyline points="9 12 12 15 16 10" />
  </svg>
)

const FlagIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z" />
    <line x1="4" y1="22" x2="4" y2="15" />
  </svg>
)

const XCircleIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
    <circle cx="12" cy="12" r="10" /><line x1="15" y1="9" x2="9" y2="15" /><line x1="9" y1="9" x2="15" y2="15" />
  </svg>
)

const STEPS = [
  { id: 'RECEBIDO',      label: 'Recebido',  icon: <InboxIcon /> },
  { id: 'EM_ANALISE',    label: 'Em Análise', icon: <SearchIcon /> },
  { id: 'PENDENTE_DOCS', label: 'Pendente',  icon: <AlertIcon /> },
  { id: 'APROVADO',      label: 'Aprovado',  icon: <ShieldCheckIcon /> },
  { id: 'FINALIZADO',    label: 'Finalizado', icon: <FlagIcon /> },
]

const STATUS_LABELS = {
  RECEBIDO:      'Recebido',
  EM_ANALISE:    'Em Análise',
  PENDENTE_DOCS: 'Pendência de Docs',
  APROVADO:      'Aprovado',
  REPROVADO:     'Reprovado',
  FINALIZADO:    'Finalizado',
}

export default function StatusTimeline({ status, history = [] }) {
  const getCurrentStepIndex = () => {
    if (status === 'REPROVADO') return 1
    return STEPS.findIndex(s => s.id === status)
  }

  const currentIdx = getCurrentStepIndex()

  return (
    <div className="timeline-wrapper">
      {/* Track de passos */}
      <div className="timeline-track">

        {/* Linha de fundo */}
        <div className="timeline-line-bg" />

        {/* Linha de progresso */}
        <div
          className="timeline-line-progress"
          style={{
            width: currentIdx >= 0 ? `${(currentIdx / (STEPS.length - 1)) * 100}%` : '0%',
            background: status === 'REPROVADO' ? 'var(--danger)' : 'var(--accent-gradient)',
          }}
        />

        {STEPS.map((step, idx) => {
          const isCompleted = idx < currentIdx
          const isCurrent   = idx === currentIdx
          const isRejected  = status === 'REPROVADO' && idx === 1
          const isFuture    = idx > currentIdx && !isRejected

          return (
            <div
              key={step.id}
              className={`timeline-step ${isCompleted ? 'completed' : ''} ${isCurrent && !isRejected ? 'current' : ''} ${isRejected ? 'rejected' : ''} ${isFuture ? 'future' : ''}`}
            >
              <div className="timeline-circle">
                {isCompleted ? <CheckIcon /> : isRejected ? <XCircleIcon /> : step.icon}
              </div>
              <span className="timeline-label">{step.label}</span>
            </div>
          )
        })}
      </div>

      {/* Banner reprovado */}
      {status === 'REPROVADO' && (
        <div className="timeline-rejected-banner">
          <XCircleIcon /> Documentação Reprovada — Contate o Suporte
        </div>
      )}

      {/* Histórico */}
      {history.length > 1 && (
        <div className="timeline-history">
          <div className="timeline-history-label">Histórico</div>
          {history.map((entry, idx) => (
            <div key={idx} className="timeline-history-row">
              <span className="timeline-history-time">
                {new Date(entry.timestamp).toLocaleTimeString('pt-BR')}
              </span>
              <span className="timeline-history-status">
                {STATUS_LABELS[entry.to_status] || entry.to_status}
              </span>
              {entry.description && (
                <span className="timeline-history-desc">— {entry.description}</span>
              )}
            </div>
          ))}
        </div>
      )}

      <style>{`
        .timeline-wrapper {
          margin: 0.75rem 0;
          padding: 1.25rem;
          background: var(--timeline-bg);
          border-radius: var(--radius-lg);
          border: 1px solid var(--border-subtle);
        }

        .timeline-track {
          display: flex;
          justify-content: space-between;
          position: relative;
          padding-bottom: 0.5rem;
        }

        .timeline-line-bg {
          position: absolute;
          top: 17px; left: 22px; right: 22px;
          height: 2px;
          background: var(--border-subtle);
          z-index: 0;
        }

        .timeline-line-progress {
          position: absolute;
          top: 17px; left: 22px;
          max-width: calc(100% - 44px);
          height: 2px;
          z-index: 1;
          transition: width 0.5s ease;
        }

        .timeline-step {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 0.4rem;
          z-index: 2;
          transition: opacity 0.3s;
        }

        .timeline-step.future { opacity: 0.35; }

        .timeline-circle {
          width: 34px; height: 34px;
          border-radius: 50%;
          display: flex; align-items: center; justify-content: center;
          border: 2px solid var(--border-subtle);
          background: var(--timeline-circle-bg);
          color: var(--text-muted);
          transition: all 0.3s ease;
          position: relative; z-index: 2;
        }

        .timeline-step.completed .timeline-circle {
          background: var(--accent);
          border-color: var(--accent);
          color: white;
          box-shadow: 0 0 10px var(--accent-glow);
        }

        .timeline-step.current .timeline-circle {
          border-color: var(--accent);
          color: var(--accent);
          background: var(--timeline-current-bg);
          box-shadow: 0 0 14px var(--accent-glow);
          animation: timelinePulse 2s infinite;
        }

        .timeline-step.rejected .timeline-circle {
          border-color: var(--danger);
          color: var(--danger);
          background: var(--timeline-rejected-bg);
          box-shadow: 0 0 10px rgba(220,38,38,0.2);
        }

        @keyframes timelinePulse {
          0%, 100% { box-shadow: 0 0 8px  var(--accent-glow); }
          50%       { box-shadow: 0 0 20px var(--accent-glow); }
        }

        .timeline-label {
          font-size: 0.68rem;
          color: var(--text-muted);
          font-weight: 500;
          font-family: var(--font-display);
          letter-spacing: 0.01em;
        }

        .timeline-step.current .timeline-label {
          color: var(--text-primary);
          font-weight: 700;
        }

        .timeline-rejected-banner {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 0.4rem;
          margin-top: 0.75rem;
          color: var(--danger);
          font-weight: 600;
          font-size: 0.83rem;
          font-family: var(--font-display);
        }

        .timeline-history {
          margin-top: 0.75rem;
          padding-top: 0.75rem;
          border-top: 1px solid var(--border-subtle);
        }

        .timeline-history-label {
          font-size: 0.67rem;
          color: var(--text-muted);
          font-weight: 700;
          text-transform: uppercase;
          letter-spacing: 0.07em;
          font-family: var(--font-display);
          margin-bottom: 0.4rem;
        }

        .timeline-history-row {
          display: flex;
          gap: 0.5rem;
          font-size: 0.72rem;
          padding: 0.15rem 0;
          align-items: baseline;
        }

        .timeline-history-time {
          color: var(--accent);
          font-family: monospace;
          font-size: 0.67rem;
          flex-shrink: 0;
        }

        .timeline-history-status {
          color: var(--text-secondary);
          font-weight: 600;
          flex-shrink: 0;
        }

        .timeline-history-desc {
          color: var(--text-muted);
        }
      `}</style>
    </div>
  )
}
