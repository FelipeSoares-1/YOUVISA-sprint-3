import React from 'react'

const STEPS = [
  { id: 'RECEBIDO', label: 'Recebido', icon: '📩' },
  { id: 'EM_ANALISE', label: 'Em Análise', icon: '🔍' },
  { id: 'PENDENTE_DOCS', label: 'Pendente', icon: '⚠️' },
  { id: 'APROVADO', label: 'Aprovado', icon: '✅' },
  { id: 'FINALIZADO', label: 'Finalizado', icon: '🏁' }
]

export default function StatusTimeline({ status, history = [] }) {
  const getCurrentStepIndex = () => {
    if (status === 'REPROVADO') return 1
    return STEPS.findIndex(s => s.id === status)
  }

  const currentIdx = getCurrentStepIndex()

  return (
    <div className="status-timeline">
      <div className="timeline-track">
        {STEPS.map((step, idx) => {
          let className = 'step'
          if (idx < currentIdx) className += ' completed'
          if (idx === currentIdx) className += ' current'
          if (status === 'REPROVADO' && idx === 1) className += ' rejected'

          return (
            <div key={step.id} className={className}>
              <div className="circle">
                {idx < currentIdx ? '✓' : step.icon}
              </div>
              <div className="label">{step.label}</div>
            </div>
          )
        })}
      </div>

      {status === 'REPROVADO' && (
        <div className="rejected-msg">
          ❌ Documentação Reprovada. Consulte o suporte.
        </div>
      )}

      {/* History Log */}
      {history.length > 0 && (
        <div className="history-log">
          <div style={{ fontSize: '0.75em', color: '#64748b', marginBottom: '0.5rem', fontWeight: 'bold' }}>
            📋 Histórico de Transições:
          </div>
          {history.map((entry, idx) => (
            <div key={idx} style={{
              fontSize: '0.75em',
              color: '#94a3b8',
              padding: '0.2rem 0',
              borderBottom: idx < history.length - 1 ? '1px solid rgba(255,255,255,0.03)' : 'none'
            }}>
              <span style={{ color: '#818cf8' }}>
                {new Date(entry.timestamp).toLocaleTimeString()}
              </span>
              {' → '}
              <span style={{ color: '#c4b5fd' }}>{entry.to_status}</span>
              {entry.description && ` — ${entry.description}`}
            </div>
          ))}
        </div>
      )}

      <style>{`
        .status-timeline {
          margin: 1rem 0;
          padding: 1rem;
          background: rgba(0,0,0,0.2);
          border-radius: 12px;
        }
        .timeline-track {
          display: flex;
          justify-content: space-between;
          position: relative;
        }
        .timeline-track::before {
          content: '';
          position: absolute;
          top: 18px;
          left: 0;
          right: 0;
          height: 2px;
          background: rgba(255,255,255,0.1);
          z-index: 0;
        }
        .step {
          position: relative;
          z-index: 1;
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 0.5rem;
          opacity: 0.4;
          transition: opacity 0.3s;
        }
        .step.completed, .step.current {
          opacity: 1;
        }
        .step .circle {
          width: 36px;
          height: 36px;
          border-radius: 50%;
          background: var(--bg-card);
          border: 2px solid rgba(255,255,255,0.2);
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 0.9em;
          transition: all 0.3s;
        }
        .step.completed .circle {
          background: var(--accent);
          border-color: var(--accent);
          color: white;
        }
        .step.current .circle {
          border-color: var(--accent);
          box-shadow: 0 0 12px var(--accent-glow);
          color: var(--accent);
          animation: pulse 2s infinite;
        }
        @keyframes pulse {
          0%, 100% { box-shadow: 0 0 8px var(--accent-glow); }
          50% { box-shadow: 0 0 20px var(--accent-glow); }
        }
        .step.rejected .circle {
          border-color: #ef4444;
          color: #ef4444;
          box-shadow: 0 0 10px rgba(239, 68, 68, 0.4);
        }
        .step .label {
          font-size: 0.75em;
          color: #94a3b8;
        }
        .step.current .label {
          color: white;
          font-weight: bold;
        }
        .rejected-msg {
          text-align: center;
          color: #ef4444;
          margin-top: 1rem;
          font-weight: bold;
        }
        .history-log {
          margin-top: 1rem;
          padding-top: 0.8rem;
          border-top: 1px solid rgba(255,255,255,0.05);
        }
      `}</style>
    </div>
  )
}
