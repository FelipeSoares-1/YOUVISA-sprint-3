# Enterprise Challenge — Sprint 1 — YOUVISA

FIAP — Fase 3 — Além das Fronteiras Digitais: Chips Neuromórficos  
Período: 09/10/2025 a 05/11/2025

Status: Entrega pendente  
Prazo de entrega: Quarta-feira, 05 de Novembro de 2025, às 23h59

---

## 1) CHALLENGE YOUVISA — Introdução

Olá, turma.

Vamos iniciar um novo desafio em parceria com a empresa YOUVISA, que atua na criação de soluções inovadoras de inteligência cognitiva voltadas para automação de atendimentos, integração de múltiplos canais de comunicação digitais e otimização de processos de emissão de vistos e serviços consulares. O objetivo é que vocês desenvolvam uma proposta de solução voltada para uma plataforma inteligente de atendimento multicanal, integrando chatbots, análise de dados e automação.

A proposta do desafio é aplicar os conhecimentos adquiridos no curso a um problema real, considerando o contexto em que a YOUVISA atua, ajudando empresas a automatizar interações, personalizar atendimentos e melhorar a experiência do usuário final.

Vocês deverão planejar e apresentar uma solução que considere automação de processos inteligente, reconhecimento e validação de documentos por meio de visão computacional, front-end com opções no menu, processamento de linguagem natural, integração entre canais digitais, permitindo que atendimentos iniciados em um meio (como WhatsApp ou site) possam ser continuados em outro (como e-mail ou aplicativo), garantindo continuidade e consistência na experiência do usuário, segurança de dados e experiência do usuário.

Nesta primeira Sprint, deverá ser entregue a documentação inicial do projeto, incluindo levantamento de tecnologias em UML, desenho da arquitetura da solução, fluxos de chatbot no Telegram como um diferencial opcional (com integração desejável à API do WhatsApp, caso seja possível) e definição da estrutura de encaminhamento para atendimento humano quando necessário.

---

## 2) CONTEXTO

A YOUVISA é uma empresa especializada em soluções digitais que unem Inteligência Artificial, RPA (Robotic Process Automation), chatbots, processamento de linguagem natural e integração em cloud para oferecer suporte a operações de atendimento e automação corporativa.

Entre os principais focos deste Challenge proposto pela empresa estão:

- Automatização de interações via chatbots inteligentes e multicanais (WhatsApp, Telegram, Web, entre outros);
- Personalização do atendimento por meio de análise de dados do cliente;
- Otimização de processos internos com integração entre sistemas, com criação de front-ends minimalistas e funcionais para a gestão de tais processos;
- Redução de custos operacionais com automação de tarefas repetitivas;
- Segurança e privacidade de dados em interações digitais;
- Apoio à tomada de decisão com relatórios e insights preditivos.

O desafio proposto para a turma tem como objetivo simular esse contexto, permitindo que vocês desenvolvam uma proposta inicial de solução para a plataforma inteligente de atendimento YOUVISA, desde a definição do escopo até a arquitetura de dados e tecnologias.

---

## 3) OBJETIVOS

Nesta primeira Sprint, os alunos deverão apresentar a documentação inicial do projeto, incluindo levantamento de tecnologias em UML, projeto da arquitetura da solução, estrutura de encaminhamento para atendimento humano quando necessário e, como diferencial opcional, fluxos de chatbot no Telegram (com integração desejável à API do WhatsApp). A entrega foca em demonstrar clareza de planejamento, coerência técnica e integração com os conteúdos do curso.

Principais objetivos:

- Definir como o chatbot e a plataforma multicanal serão estruturados (fluxos de mensagens, integração com APIs, análise de linguagem natural);
- Identificar quais dados serão coletados (histórico de atendimento, intenções do usuário, entre outros) e como serão analisados;
- Estruturar uma primeira arquitetura técnica considerando cloud, APIs e serviços de NLP;
- Garantir que a proposta esteja alinhada com segurança da informação e privacidade dos usuários;
- Propor um plano inicial de desenvolvimento baseado nos conteúdos estudados no curso;
- Trabalho em equipe: colaboração integrada, com responsabilidades compartilhadas e solução coletiva.

---

## 4) REQUISITOS TÉCNICOS E FUNCIONAIS

A proposta técnica deverá demonstrar domínio conceitual e coerência na definição da arquitetura da solução, considerando:

- Automação e RPA: uso de fluxos automatizados para gestão de registros;
- NLP e chatbots: integração com bibliotecas e frameworks de processamento de linguagem natural;
- Estrutura de dados: coleta, armazenamento (local ou nuvem) e análise dos dados de interação;
- Infraestrutura de nuvem: integração com serviços cloud (AWS, Azure, Google Cloud) para escalabilidade;
- Segurança e privacidade: estratégias para proteger dados sensíveis e garantir confiabilidade;
- Documentação: organização clara do repositório, arquitetura e justificativas técnicas.

Ferramenta sugerida para desenho da arquitetura: use recursos já explorados em sala ou ferramentas livres de diagramação — https://app.diagrams.net/ (online e grátis).

---

## 5) ENTREGÁVEIS

### 5.1) Proposta técnica documentada via GitHub privado

Primeira etapa do projeto, correspondente à definição do escopo e arquitetura inicial da solução (levantamento das tecnologias mais aderentes). O grupo deve criar um repositório privado no GitHub contendo:

- Justificativa do problema e descrição da solução proposta;
- Definição das tecnologias que serão utilizadas (linguagens, bibliotecas de IA, RPA, NLP, serviços de nuvem, entre outros);
- Esboço da arquitetura da solução (pipeline de dados, fluxos de atendimento, integração entre componentes);
- Explicação da estratégia de coleta e tratamento de dados (simulada ou planejada);
- Plano inicial de desenvolvimento e divisão de responsabilidades entre os membros;
- README claro e bem estruturado com todas as informações acima.

O GitHub deve ser privado e compartilhado apenas com o tutor da turma 2TIAOR, Leonardo (usuário: `leoruiz197`).

Passo a passo para adicionar colaboradores:

1. No topo do menu superior do repositório no GitHub, clique em "Settings";
2. No menu lateral esquerdo, clique em "Collaborators" ou em "Manage Access" (depende se é público ou privado);
3. Clique no botão "Invite a collaborator";
4. Digite o nome de usuário ou e-mail da pessoa que você quer adicionar;
5. Quando aparecer o perfil certo, clique em "Add";
6. A pessoa vai receber um convite — ela precisa aceitar para ter acesso (o convite expira em sete dias). O tutor estará atento para aceitar dentro do prazo.

### 5.2) Regras gerais

- Recomenda-se grupos de 4 a 5 integrantes (trabalho em equipe é fundamental);
- O repositório no GitHub deve ser privado e não poderá sofrer alterações após a data limite de entrega. Se for público, não é necessário adicionar o tutor, porém o trabalho ficará visível a colegas;
- Todos os integrantes devem contribuir e ter responsabilidades definidas;
- A avaliação considerará clareza, viabilidade técnica, coerência das escolhas e organização do repositório;
- Não é necessário desenvolver um código funcional nesta etapa, apenas apresentar uma proposta bem estruturada;
- É permitido o uso de dados simulados e exemplos fictícios para ilustrar a proposta;
- A proposta deve estar documentada em um README no GitHub, com todas as informações listadas.

Dica: para reforçar a importância da colaboração e entender as boas práticas de trabalho em equipe, recomenda-se o curso da Alura “Princípios do trabalho em equipe, relações colaborativas”: https://www.alura.com.br/curso-online-principios-trabalho-equipe-relacao-colaborativa

---

## Grupo

Grupo: 21  
Tamanho do grupo: Mínimo 1 | Máximo 5

Integrantes:

- Fernando Miranda Segregio — `segregio@gmail.com`
- Wellington Nascimento de Brito — `well334@hotmail.com`
- Mário Roberto Silva de Almeida — `marioalmeida1980@gmail.com`
- Caio Rodrigues Castro — `caiorcastro@gmail.com`
- Felipe Soares Nascimento — `consultor.casteliano@gmail.com`

---

## Envio e Avaliação

- Envio: Entrega pendente  
- Avaliação: Avaliação pendente

Prazo de entrega: Quarta-feira, 05 de Novembro de 2025, às 23h59

---

## Observações

- Diferencial opcional: fluxos de chatbot no Telegram (com integração desejável à API do WhatsApp);
- Priorizar segurança de dados, privacidade e continuidade da experiência multicanal;
- Utilizar UML e diagramação da arquitetura para evidenciar integração de componentes e serviços.

