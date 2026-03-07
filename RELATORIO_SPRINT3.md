# Relatório Técnico — YOUVISA (Sprint 3)

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/caiorcastro/">Caio Rodrigues Castro</a>
- <a href="https://www.linkedin.com/in/digitalmanagerfelipesoares/">Felipe Soares Nascimento</a>
- <a href="https://www.linkedin.com/in/fernando-segregio/">Fernando Miranda Segregio</a>
- <a href="https://www.linkedin.com/in/mralmeida">Mario Roberto Silva de Almeida</a>
- Wellington Nascimento de Brito

---

## 1. Introdução e Contextualização do Problema

A Sprint 3 da plataforma **YOUVISA** consolida a transição do sistema: de uma ferramenta reativa de automação documental (focada apenas no recebimento e extração de dados) para um **orquestrador ativo de acompanhamento e governança de processos de emissão de vistos**.

Anteriormente, o sistema operava como uma "caixa-preta", onde o usuário enviava seus documentos, mas o acompanhamento ficava refém de processos manuais ou atendentes humanos informando o <i>status</i> via canais não-oficiais de mensageria. O objetivo central desta sprint foi estruturar o ciclo de vida do processo de backoffice, traduzindo as mudanças internas em **interfaces de consumo claro para o cliente final** e introduzindo fluxos autônomos por **Inteligência Artificial Generativa**.

Para tal, a arquitetura foi expandida para sustentar três novos pilares de produto:
1. **Rastreabilidade (Auditabilidade)** baseada numa rígida Máquina de Estados.
2. **Sistema Event-driven de Notificações** para alertas transacionais multicanal (E-mail e SMS).
3. **Chatbot Conversacional (Consultora Valéria)** capaz de traduzir em linguagem empática os eventos técnicos do backoffice e blindado por *Guard Rails* de mitigação de riscos de alucinação (LLM).

---

## 2. Decisões Arquiteturais e Componentização Multicamadas

A fim de garantir isolamento de responsabilidades e escalabilidade, optou-se por separar rigidamente a aplicação em camadas específicas de serviços (*Service Layer Pattern*). 

### 2.1 Stack Tecnológico
- **Core do Backend:** *Python 3.12* com framework *FastAPI*. Sendo um framework ASGI, o FastAPI nos fornece o benefício primário da **programação assíncrona (I/O non-blocking)**. Esta escolha técnica é imprescindível para um ecossistema que dialoga com APIs externas demoradas (como chamadas para o motor de LLM Gemimi) e instiga o envio de SMS simulados sem bloquear as demais threads da aplicação, mantendo alta vazão na API (TPS - *Transactions Per Second*).
- **Interface e Painel (Frontend):** _React_ impulsionado pelo compilador _Vite_. O uso de *Single Page Application* (SPA) permite injetar os *States* do processo via API diretamente num `StatusTimeline` ou `Dashboard` sem o recarregamento total da tela, mantendo a experiência do cliente (UX) engajadora e instantânea na verificação da documentação.
- **Motor de PLN e Computação NLU:** O modelo *Gemini 2.5 Flash* da Google, acessado via SDK `google-genai`. Ele age simultaneamente na extração estruturada (Data Parsing de tipagem estrita com _Pydantic_) e na engine de diálogo do Chatbot em tempo real.

---

## 3. Workflow e Lógica Baseada em Máquina de Estados Finitos (FSM)

A espinha dorsal imposta nos requisitos consistiu na abolição do uso de literais caóticos para definir andamento. Introduzimos a classe `ProcessStatus` (uma classe *ENUM*) que transita compulsoriamente pelas vias operacionais em `workflow_service.py`.

### 3.1 Transições Legais Determinísticas
Nenhum atributo de status da base de dados sofre inferência direta ou injeção forçada acidental (evitando corrupção lógica). Os estados são fechados no ciclo:
1. **`RECEBIDO`**: Gatilho base no momento do recebimento do payload do upload de documento.
2. **`EM_ANALISE`**: Onde rodam as lógicas assíncronas de validações via OpenCV documentais ou checagens pela equipe técnica.
3. **`PENDENTE_DOCS`**: Estado limitador (parada). Necessita intervenção proativa obrigatória do usuário no front-end para reupload em virtude de ilegibilidade ou página faltante.
4. **`APROVADO`**: Todos metadados e checagens deram positivo, avançando ao trâmite consular de direito.
5. **`REPROVADO`**: Rejeição definitiva da jornada por motivos como inautenticidade detectada.
6. **`FINALIZADO`**: Visto homologado e pacote impresso ou digital enviado.

Apenas requisições que acionem o método `transition(doc_id, event)` conseguem reescrever o status do usuário, desde que respeitem os nós mapeados no `VALID_TRANSITIONS` (ex: a transição de `RECEBIDO` para `FINALIZADO` geraria por si próprio um bloqueio de arquitetura / exceção em código).

### 3.2 Auditabilidade em Coleções (History Store)
Como prova irrefutável de avanço de processos com datas críveis, toda e qualquer transação FSM confirmada instiga um append para um Array imutável interno (representando num banco documento-orientado ou JSONB num Postgres). Este histórico armazena Timestamp no formato ISO-8601, Status A, Status B, Razão, e o método de gatilho, permitindo reversões (rollbacks) orgânicas ou relatórios precisos do SLA da consultoria.

---

## 4. Integrações Event-Driven e Serviço de Mensageria

O código atende ao paradigma *Event-Driven Architecture (EDA)* em simbiose com o Padrão Observador. O `workflow_service` não sabe despachar e-mails. Quando ocorre uma mutação na Máquina de Estados, ele invoca instintivamente o hook de notificação do `notification_service.py` injetando como contexto o `event_type` atual. 

Dentro deste limitador sistêmico existem as `CHANNEL_RULES`: regras de negócio duras limitando *O Que* será mandando por *Qual* canal.
- Eventos transicionais neutros (Ex: *Processo Iniciado*) ativam comunicações silenciosas usando apenas a simulação SMTP (E-mail).
- Eventos bloqueantes (Ex: Transição para `PENDENTE_DOCS`) acionam a urgência, preenchendo as chamadas simuladas multi-fator de via Twilio/Zenvia, disparando assim E-mails acompanhados por um SMS emergencial contendo CTAs *(Call To Action)* imediatos para destravamento do fluxo.

---

## 5. Governança, Contenção e Extração por Inteligência Artificial (Guard Rails)

Sendo o trato imigratório um setor extremamente delicado, a aplicação incorreta de LLMs numa funcionalidade de "Consulta de Status" resultaria facilmente na quebra da expectativa do cliente corporativo e, como consequência direta, responsabilidade contratual/jurídica (como prometer aprovação equivocadamente de visto).

O sistema repondeu ao pressuposto implementando *Guard Rails* triplos (Controles de Risco IA):
1. **Modelagem de Prompting de Instruções Severas (System Instruction):**  
   Antes do usuário falar a primeira linha, o pipeline backend anexa o `Contexto do Processo Atual` (seu status fixo em código, o ID referencial, etc.) e ordena inequivocamente que a *"Consultora Virtual Valéria"*: **(a)** NUNCA estipule, em hipótese alguma, prazos fechados nem datas de fim; **(b)** NUNCA assevere "garantias" sobre o deferimento antes de se enxergar a string estrita `APROVADO` no objeto JSON retorcionado da máquina; e **(c)** que deve recusar educadamente o conselho sobre temas arbitrários fora da seara de passaportes e documentação internacional.  

2. **Gerenciamento de Janela de Memória (Memory Windowing e Tokenização):**  
   O repositório em `ai_service.py` não joga o *dump* de DB da sessão toda ao cérebro do LLM. Aplica o *Slicing* (`chat_history[-10:]`), onde apenas as 10 turnos recursivas finais sobem no cabeçalho POST para o Google Cloud/Vertex. Isso mitiga a fadiga matemática da rede neural (evitando a IA se "perder") e otimiza de sobremaneira o consumo financeiro de faturamento do projeto por requisição (Token Costing Control).

3. **Filtragem e Bloqueio em Nível de Saída (Filtros Determinísticos e Fallbacks):**
   A camada blindada final. Independentemente quão boa for a resposta gerada após passar no prompt, toda e qualquer variável de *raw_return* do bot sofre uma regex/limpeza por Python estruturado antes de descer para o JSON da resposta HTTP. A função local `apply_guardrails(text, status)` confronta cada milissegundo as sentenças produzidas com o array predatório de  `BLOCKED_PHRASES` (que abrigam sub-strings como *"em breve será aprovado"*, *"garanto"*, *"com certeza"*, *"prazo de"*, *"amanhã"*).

   Se a função detectar que a engine LLM produziu uma das frases probididas acima — violando as diretrizes —, todo o processamento recém-gerado é rasgado em backend, rodando rotas para injetar no lugar um Mapeamento Estático Seguro (`SAFE_FALLBACK`) aprovado formalmente e por jurídico; ou seja: o usuário final visualiza um alerta pré-concebido e frio, totalmente controlado. Adicionalmente, também entra em jogo o **"Modo Mock"**. Caso o sistema falhe no ping externo ao Gemini Cloud, ou enfrente a preterição de chaves `gemini_api_key` nos `Environments` locais, a IA entra em standby e provê todas as funções como uma árvore de respostas lógicas simuladas, atestando a robustez zero-downtime (*Graceful Degradation*).

---

## 6. Parecer Final e Considerações de Implementação

A entrega da Sprint 3 converte a promessa de automatização do "Projeto YOUVISA" num modelo de negócio viável e escalona a plataforma rumo ao amadurecimento como PaaS (Plataforma como Serviço). Validando os requisitos essenciais, observamos com êxito a entrega funcional de transições atômicas entre os status, resguardo em auditoria técnica rigorosa para clientes e acionistas, além um Chatbot assertivo que serve como alicerce do relacionamento da marca com o tomador dos serviços. O código e a engenharia propostos cumprem substancialmente 100% dos limites orientados do Desafio FIAP Sprint 3, preparando assim os pilares para potenciais escalonamentos futuros com integração de APIs consulares diretas ou infraestrutura escalável (CI/CD nativa de contêineres e persistência em Big Data para análises avançadas de tempos de retenção FSM).
