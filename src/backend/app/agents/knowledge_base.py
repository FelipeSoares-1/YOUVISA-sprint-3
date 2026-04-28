"""
Base de conhecimento real sobre processos consulares para o assistente Valéria.
Fontes: Embaixada EUA no Brasil, VFS Global, Itamaraty, Ministério das Relações Exteriores.
"""

# ---------------------------------------------------------------------------
# Visto Americano B1/B2
# ---------------------------------------------------------------------------
VISTO_AMERICANO = {
    "tipo": "Visto Americano B1/B2 (Turismo e Negócios)",
    "documentos_obrigatorios": [
        "Passaporte válido (com pelo menos 6 meses de validade além da viagem)",
        "Formulário DS-160 preenchido e confirmado online (ceac.state.gov)",
        "Confirmação impressa do DS-160 (código de barras)",
        "Comprovante de pagamento da taxa MRV (US$ 185)",
        "Comprovante de agendamento no CASV impresso",
        "Foto 5x5cm ou 5x7cm, fundo branco, sem óculos, sem sorriso",
    ],
    "documentos_recomendados": [
        "Extratos bancários dos últimos 3 a 6 meses",
        "Comprovante de renda (holerite, pró-labore, declaração IR)",
        "Declaração de Imposto de Renda mais recente",
        "Comprovante de vínculo empregatício (carta do empregador em inglês)",
        "Comprovante de matrícula (para estudantes)",
        "Documentos de imóveis ou bens que comprovem vínculos com o Brasil",
        "Certidão de casamento e documentos de filhos (para comprovar laços familiares)",
        "Reserva de hotel e passagem (não comprar antes da aprovação)",
        "Passaporte(s) anterior(es) com vistos",
    ],
    "etapas": [
        "1. Preencher o DS-160 online (ceac.state.gov)",
        "2. Pagar a taxa MRV de US$ 185",
        "3. Agendar atendimento no CASV (Centro de Atendimento ao Solicitante de Visto)",
        "4. Comparecer ao CASV para coleta biométrica (impressões digitais e foto)",
        "5. Agendar e comparecer à entrevista no Consulado Americano",
        "6. Aguardar a decisão — geralmente 3 a 5 dias úteis após a entrevista",
    ],
    "prazos": {
        "agendamento_entrevista": "Varia por demanda — de 1 semana a vários meses em períodos de alta procura",
        "entrega_passaporte": "3 a 10 dias úteis após aprovação na entrevista",
        "validade_visto": "Geralmente 10 anos para brasileiros (múltiplas entradas)",
        "ds160_antecedencia": "O código DS-160 deve ser inserido no CASV com pelo menos 3 dias úteis antes da entrevista",
    },
    "motivos_recusa_comuns": [
        "Seção 214(b): não comprovação de vínculos suficientes com o Brasil",
        "Falta de renda ou patrimônio comprovados",
        "Inconsistências nas informações do DS-160",
        "Viagens anteriores com overstay (ficou mais tempo que o permitido nos EUA)",
        "Histórico de recusas sem documentação adicional",
    ],
    "dicas": [
        "Apresente documentos que comprovem que você voltará ao Brasil (emprego, família, imóvel)",
        "Não mencione intenção de trabalhar nos EUA durante a entrevista B1/B2",
        "Fale com segurança e brevidade na entrevista — o cônsul decide em poucos minutos",
        "Ter conta bancária com saldo consistente ajuda muito",
    ],
}

# ---------------------------------------------------------------------------
# Visto Schengen (Europa)
# ---------------------------------------------------------------------------
VISTO_SCHENGEN = {
    "tipo": "Visto Schengen — Curta Estadia (até 90 dias em 180)",
    "quem_precisa": "Brasileiros NÃO precisam de visto Schengen para turismo/negócios até 90 dias. Precisam para estadias longas, trabalho ou estudo.",
    "etias": {
        "o_que_e": "ETIAS é a autorização eletrônica de viagem para a Europa, obrigatória para brasileiros a partir do último trimestre de 2026.",
        "custo": "€7 euros, válida por 3 anos com múltiplas entradas",
        "solicitacao": "Online, aprovação geralmente em minutos/horas",
    },
    "documentos_para_entrada": [
        "Passaporte válido (pelo menos 3 meses após a data de retorno)",
        "Seguro viagem Schengen obrigatório — cobertura mínima de €30.000 para despesas médicas",
        "Comprovante de hospedagem (hotel, Airbnb, carta convite)",
        "Passagem de ida e volta dentro do período de 90 dias",
        "Comprovante financeiro — média de €70/dia por pessoa",
    ],
    "documentos_visto_longa_estadia": [
        "Passaporte válido",
        "Formulário de solicitação preenchido",
        "2 fotos 3,5x4,5cm fundo branco",
        "Seguro saúde válido no país de destino",
        "Comprovante de meios financeiros suficientes",
        "Comprovante de moradia no país de destino",
        "Carta de aceite (para estudos) ou contrato de trabalho",
        "Antecedentes criminais apostilados",
    ],
    "prazos": {
        "processamento": "Até 15 dias úteis para visto Schengen padrão (pode chegar a 30-60 dias em alta temporada)",
        "antecedencia_solicitacao": "Solicitar com no mínimo 15 dias de antecedência, recomendado 1-3 meses antes",
    },
    "dicas": [
        "O seguro viagem é OBRIGATÓRIO — sem ele a entrada pode ser negada",
        "Para Portugal: desde abril de 2026 todas as solicitações são presenciais no Brasil",
        "Compre passagens e hospedagem com política de cancelamento até ter o visto",
    ],
}

# ---------------------------------------------------------------------------
# Passaporte Brasileiro
# ---------------------------------------------------------------------------
PASSAPORTE_BRASILEIRO = {
    "tipo": "Passaporte Ordinário Brasileiro",
    "documentos_necessarios": [
        "RG (Carteira de Identidade) original",
        "CPF",
        "Título de Eleitor ou comprovante de quitação eleitoral",
        "Certidão de nascimento ou casamento (para solicitação de novo passaporte)",
        "Passaporte anterior (em caso de renovação, mesmo se vencido há até 2 anos)",
        "Taxa de expedição paga (R$ 257,25 para adultos)",
    ],
    "etapas": [
        "1. Agendar atendimento no site da Polícia Federal (www.gov.br/pf)",
        "2. Pagar a taxa GRU (Guia de Recolhimento da União)",
        "3. Comparecer à Polícia Federal com os documentos originais",
        "4. Coleta de dados biométricos (foto, assinatura, impressões digitais)",
        "5. Aguardar entrega — pelo correio ou retirada na PF",
    ],
    "prazos": {
        "processamento_normal": "6 dias úteis",
        "processamento_urgente": "1 dia útil (taxa adicional de R$ 257,25 — total R$ 514,50)",
        "validade": "10 anos para maiores de 18 anos / 5 anos para menores",
        "renovacao_recomendada": "Solicitar com pelo menos 6 meses antes do vencimento (muitos países exigem 6 meses de validade)",
    },
    "dicas": [
        "Muitos países exigem que o passaporte tenha pelo menos 6 meses de validade além da data de retorno",
        "O passaporte pode ser renovado mesmo antes de vencer",
        "Em caso de urgência comprovada (viagem em menos de 10 dias), é possível solicitar atendimento prioritário",
        "Menores de 18 anos precisam dos dois pais presentes ou autorização notarial",
    ],
}

# ---------------------------------------------------------------------------
# Visto Reino Unido (ETA)
# ---------------------------------------------------------------------------
VISTO_REINO_UNIDO = {
    "tipo": "ETA — Electronic Travel Authorisation (Reino Unido)",
    "status_2025": "Desde 8 de janeiro de 2025 o ETA é obrigatório para brasileiros visitarem o Reino Unido.",
    "documentos": [
        "Passaporte biométrico válido",
        "E-mail para confirmação",
        "Cartão de crédito/débito para pagamento",
    ],
    "processo": [
        "1. Solicitar online pelo app 'UK ETA' (iOS/Android) ou site oficial gov.uk",
        "2. Pagar £10 (aproximadamente R$77)",
        "3. Aprovação geralmente em minutos a 3 dias úteis",
        "4. ETA fica vinculado ao passaporte — não é um documento físico",
    ],
    "validade": "2 anos ou até o passaporte vencer (o que ocorrer primeiro), múltiplas entradas",
    "estadia_maxima": "6 meses por visita",
    "dicas": [
        "O ETA NÃO é um visto — é uma autorização eletrônica pré-viagem",
        "Para trabalho, estudo ou estadia longa é necessário visto específico",
        "Solicite o ETA com pelo menos 72h de antecedência",
    ],
}

# ---------------------------------------------------------------------------
# Vistos Brasil para Estrangeiros (atualização 2025)
# ---------------------------------------------------------------------------
VISTO_BRASIL_ESTRANGEIROS = {
    "nota": "A partir de 10 de abril de 2025, Brasil voltou a exigir visto de turista de cidadãos dos EUA, Canadá e Austrália.",
    "processo_estrangeiros": [
        "Solicitar e-Visa no site VFS Global (brazil.vfsevisa.com)",
        "Taxa: US$ 80,90 (aprox. R$479)",
        "Prazo: até 15 dias úteis",
        "Estadia máxima: 90 dias",
    ],
    "isencoes_ativas": "Cidadãos do Reino Unido, União Europeia e Japão ainda são isentos de visto para turismo.",
}

# ---------------------------------------------------------------------------
# FAQ Geral — Processos Consulares
# ---------------------------------------------------------------------------
FAQ_GERAL = {
    "o_que_e_processo_consular": (
        "Um processo consular é o conjunto de etapas necessárias para obter um documento "
        "consular (visto, passaporte, certidão) junto a um consulado ou embaixada. "
        "Na YOUVISA, cuidamos de cada etapa: orientação documental, revisão, envio e acompanhamento."
    ),
    "por_que_visto_negado": [
        "Falta de comprovação de vínculos com o país de origem",
        "Documentação incompleta ou inconsistente",
        "Histórico de violações de visto anteriores",
        "Situação financeira insuficiente",
        "Viagem sem propósito claramente justificado",
    ],
    "o_que_fazer_visto_negado": (
        "Em caso de negativa, é possível: (1) entender o motivo na carta de recusa, "
        "(2) reunir documentação adicional que endereça a objeção, "
        "(3) solicitar novo visto com melhor embasamento documental. "
        "Nossa equipe pode orientar em cada caso."
    ),
    "quanto_custa_servico_youvisa": (
        "Os valores variam conforme o tipo de visto e o país. "
        "Entre em contato com nossa equipe comercial para um orçamento personalizado. "
        "As taxas consulares são pagas diretamente ao consulado e não estão incluídas."
    ),
    "preciso_entrevista": (
        "Depende do visto. O visto americano B1/B2 exige entrevista presencial na maioria dos casos. "
        "Vistos Schengen geralmente exigem comparecimento presencial no VFS Global. "
        "O passaporte brasileiro exige comparecimento à Polícia Federal."
    ),
    "documentos_precisam_traducao": (
        "Para a maioria dos vistos americanos, a entrevista ocorre em inglês mas "
        "documentos em português são aceitos. Para vistos europeus, alguns países exigem "
        "tradução juramentada de documentos específicos. Consulte nossa equipe para seu caso."
    ),
    "posso_viajar_com_passaporte_vencendo": (
        "A maioria dos países exige que o passaporte tenha validade mínima de 6 meses "
        "além da data de retorno. Renove com antecedência de pelo menos 3 a 6 meses."
    ),
}

# ---------------------------------------------------------------------------
# Índice por intent — mapeia qual conhecimento é mais relevante
# ---------------------------------------------------------------------------
KB_BY_INTENT: dict[str, list[str]] = {
    "STATUS_QUERY": [
        "A YOUVISA acompanha seu processo em tempo real. O status é atualizado a cada etapa: "
        "Recebido → Em Análise → Aprovado/Pendente → Finalizado.",
    ],
    "MISSING_DOCS": [
        f"Documentos mais solicitados para visto americano: {', '.join(VISTO_AMERICANO['documentos_obrigatorios'][:4])}.",
        f"Para passaporte brasileiro é preciso: {', '.join(PASSAPORTE_BRASILEIRO['documentos_necessarios'][:3])}.",
        "Para visto Schengen de longa estadia: comprovante financeiro, seguro saúde e carta de aceite/contrato.",
    ],
    "NEXT_STEP": [
        f"Etapas do visto americano: {' → '.join([e.split('. ')[1] for e in VISTO_AMERICANO['etapas']])}.",
        f"Etapas do passaporte brasileiro: {' → '.join([e.split('. ')[1] for e in PASSAPORTE_BRASILEIRO['etapas'][:3]])}.",
    ],
    "DEADLINE": [
        f"Passaporte brasileiro: {PASSAPORTE_BRASILEIRO['prazos']['processamento_normal']} (urgente: {PASSAPORTE_BRASILEIRO['prazos']['processamento_urgente']}).",
        f"Visto americano: entrega do passaporte em {VISTO_AMERICANO['prazos']['entrega_passaporte']} após aprovação.",
        f"Visto Schengen: {VISTO_SCHENGEN['prazos']['processamento']}.",
        f"ETA Reino Unido: {VISTO_REINO_UNIDO['processo'][2]}.",
    ],
    "APPROVAL_STATUS": [
        f"Principais motivos de recusa do visto americano: {'; '.join(VISTO_AMERICANO['motivos_recusa_comuns'][:3])}.",
        FAQ_GERAL["o_que_fazer_visto_negado"],
    ],
    "DOCUMENT_INFO": [
        f"Visto americano B1/B2 — documentos obrigatórios: {', '.join(VISTO_AMERICANO['documentos_obrigatorios'][:3])}.",
        f"Passaporte brasileiro — documentos: {', '.join(PASSAPORTE_BRASILEIRO['documentos_necessarios'][:3])}.",
        f"Schengen — destaque: {VISTO_SCHENGEN['documentos_para_entrada'][1]}.",
        f"ETA Reino Unido: {VISTO_REINO_UNIDO['status_2025']}",
    ],
    "GREETING": [
        "A YOUVISA é uma plataforma de processos consulares com IA. "
        "Ajudamos com vistos americanos, europeus, passaportes e documentação consular em geral.",
    ],
    "HELP": [
        FAQ_GERAL["o_que_e_processo_consular"],
        "Posso responder sobre: documentos necessários, prazos, etapas, motivos de recusa e orientações gerais.",
    ],
    "GENERAL": [
        FAQ_GERAL["o_que_e_processo_consular"],
        "Principais serviços: visto americano B1/B2, visto Schengen, passaporte brasileiro, ETA Reino Unido.",
    ],
}


def get_kb_facts(intent: str) -> list[str]:
    """Retorna fatos da base de conhecimento relevantes para a intent detectada."""
    return KB_BY_INTENT.get(intent, KB_BY_INTENT["GENERAL"])
