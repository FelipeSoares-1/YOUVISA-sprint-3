# Fluxo de Estados - YOUVISA

```mermaid
stateDiagram-v2
    [*] --> RECEBIDO: Upload do Documento
    RECEBIDO --> EM_ANALISE: Validação Automática (CV/IA)
    EM_ANALISE --> PENDENTE_DOCS: Falta de Informação/Ilegível
    EM_ANALISE --> APROVADO: Tudo OK
    EM_ANALISE --> REPROVADO: Fraude Detectada/Ineligível
    
    PENDENTE_DOCS --> RECEBIDO: Reenvio do Documento
    
    APROVADO --> [*]
    REPROVADO --> [*]

    note right of RECEBIDO
        O cliente enviou o arquivo.
        Aguardando processamento.
    end note

    note right of EM_ANALISE
        IA está lendo e 
        CV está validando.
    end note
```

## Transições e Gatilhos

| Origem | Destino | Gatilho | Ação do Sistema |
|---|---|---|---|
| `*` | `RECEBIDO` | Upload via API | Registrar data, Notificar "Recebido" |
| `RECEBIDO` | `EM_ANALISE` | Job de Processamento | Iniciar validação CV + IA |
| `EM_ANALISE` | `APROVADO` | IA Confidence > 80% | Notificar aprovação, Gerar Voucher |
| `EM_ANALISE` | `PENDENTE_DOCS` | IA Confidence < 80% | Notificar erro, Solicitar reenvio |
| `EM_ANALISE` | `REPROVADO` | Fraude/Invalidez | Notificar negativa, Encerrar |
