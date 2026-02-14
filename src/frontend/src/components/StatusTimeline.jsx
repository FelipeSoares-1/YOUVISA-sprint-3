import React from 'react'

const STEPS = [
    { id: 'RECEBIDO', label: 'Recebido' },
    { id: 'EM_ANALISE', label: 'Em Análise' },
    { id: 'PENDENTE_DOCS', label: 'Pendente' },
    { id: 'APROVADO', label: 'Aprovado' }
]

export default function StatusTimeline({ status }) {
    const getCurrentStepIndex = () => {
        if (status === 'REPROVADO') return 1; // Show as stuck in analysis or special state
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
                                {idx < currentIdx ? '✓' : idx + 1}
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

            <style>{`
        .status-timeline {
          margin: 2rem 0;
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
          top: 15px;
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
          opacity: 0.5;
        }
        .step.completed, .step.current {
          opacity: 1;
        }
        .step .circle {
          width: 32px;
          height: 32px;
          border-radius: 50%;
          background: var(--bg-card);
          border: 2px solid rgba(255,255,255,0.2);
          display: flex;
          align-items: center;
          justify-content: center;
          font-weight: bold;
          transition: all 0.3s;
        }
        .step.completed .circle {
          background: var(--accent);
          border-color: var(--accent);
          color: white;
        }
        .step.current .circle {
          border-color: var(--accent);
          box-shadow: 0 0 10px var(--accent-glow);
          color: var(--accent);
        }
        .step.rejected .circle {
          border-color: #ef4444;
          color: #ef4444;
        }
        .rejected-msg {
          text-align: center;
          color: #ef4444;
          margin-top: 1rem;
          font-weight: bold;
        }
      `}</style>
        </div>
    )
}
