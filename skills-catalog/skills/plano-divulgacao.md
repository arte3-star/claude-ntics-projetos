---
name: plano-divulgacao
description: >-
  Monta o Plano de Divulgação (também chamado de Plano de Comunicação) de um projeto NTICS,
  cruzando o Termo de Abertura (TAP) com o Perfil Estratégico do Patrocinador (PEP). Entrega
  Identificação, Estratégia, Guia de Linguagem, Mensagens-Chave e a seção-coração "Descrição
  por Atividade" com descrição completa, público prioritário e meta — em projetos multi-PRONAC,
  uma tabela por PRONAC com metas por cidade. Inclui a pesquisa de mídias prioritárias por praça
  (jornais, portais, rádio, TV, universidades e canais locais) para a Assessoria de Imprensa.
  Acione SEMPRE que o usuário disser "plano de divulgação", "plano de comunicação", "monta o
  plano de divulgação/comunicação do projeto X", "plano de mídia do projeto", "faz o plano de
  comunicação pro patrocinador", ou pedir para estruturar como o projeto vai ser divulgado.
  NÃO confundir com plano-mensal (calendário de posts de redes) nem com planejamento-mensal
  (dashboard do escritório).
---

# Plano de Divulgação (= Plano de Comunicação)

"Plano de divulgação" e "plano de comunicação" são o mesmo documento na NTICS: dois nomes para a
mesma entrega. Ele é o **cruzamento do Termo de Abertura (TAP) com o Perfil Estratégico do
Patrocinador (PEP)**. Do TAP vêm as atividades, o público e as metas; do PEP vêm o tom, os termos
recomendados/proibidos, os riscos de reputação e a narrativa prioritária. O plano existe para que
todo mundo (design, redes, assessoria, coordenação, patrocinador) divulgue o projeto de forma
coerente, dentro do escopo, e com material de comprovação por PRONAC para o Ministério da Cultura.

O objetivo desta skill é entregar o plano no nível dos modelos de referência da NTICS (planos 117 e
124), sem inventar nada: se um dado não está no TAP nem no PEP, marque como `[a confirmar]`.

## Antes de escrever: reúna as fontes

Um plano só é bom se cruzar as fontes certas. Colete, nesta ordem:

1. **TAP do projeto** — especialmente a página/aba **Escopo + Indicadores** (atividades, metas,
   cobertura por PRONAC e por cidade) e a página **Comunicação** (réguas, KV, peças, grade de redes).
   Sem o escopo do TAP não há seção 1.5.
2. **PEP de cada patrocinador** — a narrativa prioritária, termos recomendados/proibidos, riscos de
   enquadramento e nível de exposição da marca. Um projeto com dois patrocinadores tem dois PEPs.
   Se o PEP ainda não existe, avise o usuário e ofereça criá-lo antes (é pré-requisito de qualidade).
3. **ATAs/kickoff** — pedidos específicos do patrocinador (tema, entregáveis, restrições) e datas.

Leia as fontes na íntegra antes de montar. Se elas estiverem no ClickUp, use
`clickup_get_document_pages`; no Drive, `read_file_content`.

## Estrutura obrigatória do documento

Siga esta ordem. É a mesma dos planos 117 e 124.

### 1.1 Dados do Projeto (tabela)
Nome oficial · Código NTICS · Edição/Ano · Cliente/Patrocinador (por PRONAC, se multi) ·
Realização/Proponente (com CNPJ) · Cidades de execução · **Datas de execução por cidade**
(mais datas de Talk/pré-evento quando houver; `[a confirmar]` quando não fechado) · Lei de incentivo ·
**PRONACs** · Tipologia · link(s) para o(s) PEP(s).

### Resumo do Projeto + Checklist de origem
Um parágrafo que explica o que é o projeto, quantos PRONACs, patrocinadores, cidades e o fio condutor
temático. Depois, um checklist das fontes usadas (TAP, PEP de cada patrocinador, ATAs).

### 1. ESTRATÉGIA
- **1.1 Objetivo do Plano de Comunicação** — bullets: divulgar (serviço: quando/onde/como),
  mobilizar (escolas, secretarias, comunidade, poder público), dar visibilidade ao patrocinador
  conforme a régua, ancorar a marca no tema, gerar matéria-prima para impacto.
- **1.2 Insights** — Território, Públicos, Patrocinador(es), **Riscos de comunicação**, Oportunidades.
  Os riscos saem do PEP (ex.: greenwashing, régua compartilhada, imagem de menores/LGPD, pré-eleitoral).
- **1.3 Porta-vozes e Governança** — porta-vozes autorizados numa tabela (função · nome · cargo ·
  contato), incluindo patrocinador `[a confirmar no kickoff]`, coordenação NTICS, assessoria de
  imprensa e "para quem escalar tema sensível". Depois o **Guia de Linguagem**: tom editorial; quando
  o patrocinador tem causa âncora, incluir uma **narrativa âncora** (parágrafo que traduz a marca no
  projeto), um **princípio-mãe** e uma **linguagem central** (frase-guia); **termos e claims
  permitidos** e **termos/abordagens proibidos** (do PEP); cuidados/compliance (imagem de menores,
  LGPD, régua nunca em post de rede social, sem travessão, siglas abertas na 1ª ocorrência).
- **1.4 Mensagens-Chave** — institucionais (frases prontas), por público (escolas/secretarias,
  professores, estudantes, patrocinador) e provas/evidências (metas + indicadores da Camada 1 do TAP).
- **1.5 Descrição por Atividade (com metas)** — a seção mais importante. Ver regra abaixo.

### 1.5 — a regra que não pode falhar
Esta seção **cruza o Escopo do TAP com o PEP**. Cada atividade recebe: **Atividade · Descrição
completa (texto externo) · Público prioritário · Meta**. A "descrição completa" é um texto pronto
para comunicação externa (o que é a atividade, para quem, com que sentido), não o nome seco.

**Projeto com um só PRONAC:** uma tabela, com colunas de meta por cidade quando houver mais de uma.

**Projeto multi-PRONAC (ex.: 122/118):** **uma tabela por PRONAC**, e dentro de cada tabela
**colunas de meta por cidade**. Cabeçalho sugerido: `Atividade | Descrição completa | Público
prioritário | Meta total | [Cidade 1] | [Cidade 2] | ...`. Assim o leitor vê, de um golpe, o que é
cada atividade, para quem, e quanto se espera em cada praça.

**Classificação MinC e fase:** marque cada atividade como `[ENTREGA MINC]` com o PRONAC ao qual
pertence, ou como "Execução prática" quando não for produto MinC. Isso é o que liga o plano à
comprovação. Quando fizer sentido, acrescente a **fase** de cada atividade (pré-evento nas escolas /
dia do evento / pós). Em projetos grandes, vale ter as duas visões: uma **tabela-resumo** (atividade ·
formato · público · meta por cidade · fase · classificação MinC/PRONAC) e, abaixo, uma **descrição em
parágrafo por atividade** (texto externo pronto), marcando `[ENTREGA MINC]` e citando a atividade pelo
nome exato do MinC.

**Acessibilidade por atividade:** monte uma tabela com uma linha por atividade e colunas Gratuito ·
LIBRAS · Audiodescrição · Monitores · Acessibilidade física · Outro. É exigência das leis de incentivo
e evita retrabalho; puxe do TAP (seção de acessibilidade) e marque `[a confirmar]` o que faltar.
Sinalize itens obrigatórios por PRONAC (ex.: braile na exposição, registro com Libras e audiodescrição).

Regras de meta: os números do TAP são **participações por atividade** (o mesmo aluno participa de
várias atividades) — nunca os some como beneficiários únicos, e diga isso numa observação. Se o
escopo mudou depois do TAP (decisão em reunião), reflita a mudança e marque
`[reconciliar com o Escopo do TAP]`.

### 2. ASSESSORIA DE IMPRENSA (com pesquisa de mídias)
- **2.1 Responsável e fluxo de aprovação** — quem faz a assessoria (nome/agência/contato, se houver)
  e o fluxo de aprovação dos releases (assessoria redige, coordenação revisa, interface com o
  patrocinador, patrocinador aprova, publica), com os prazos de aprovação do PEP.
- **2.2 Estratégia de Imprensa** — objetivo (cobertura local/regional por editoria), critérios
  editoriais, preparação de porta-vozes e Q&A para temas sensíveis.
- **2.3 Mídias por cidade** — resultado da pesquisa (ver próxima seção), **uma tabela por cidade** com
  colunas `Tier | Tipo | Veículos/Canais | Observações`.
- **Canais extras e universidades** — podcasts/videocasts, universidades e institutos locais,
  canais oficiais do município, com gatilhos de pauta.

> Não reproduza a seção "Releases" dos modelos antigos. O foco é o plano de divulgação; releases
> ficam de fora a menos que o usuário peça.

## Pesquisa de mídias prioritárias (obrigatória)

Um plano sem imprensa mapeada é meio plano. Para **cada cidade/UF** do projeto, pesquise a mídia
local e regional na web e organize em tiers. Se houver subagentes, dispare uma pesquisa por cidade
em paralelo (mais rápido e cada cidade tem imprensa própria); senão, pesquise em série com WebSearch.

Para cada praça, entregue:
- **Tier 1 — Locais:** jornais, portais, rádios e TVs do próprio município.
- **Tier 2 — Regionais/Estado:** veículos da região e do estado (afiliadas de rede, grandes portais).
- **Tier 3 — Amplificadores/temáticos:** verticais e agendas (educação, cultura, sustentabilidade/ESG,
  o tema do projeto), podcasts e jornalismo digital.
- **Universidades/institutos** no território (comunicação/extensão) para credibilidade e alcance.
- **Canais oficiais do município** (prefeitura, secretarias) para serviço e mobilização.
- **Gatilhos de pauta** — 3 ganchos prontos para vender entrevista, conectando o projeto ao noticiário
  local (educação + cultura + o tema).

Entregue por cidade numa **tabela** `Tier | Tipo | Veículos/Canais | Observações`, para casar com a
seção 2.3. Quando a assessoria contratada for quem faz o mapeamento fino de contatos, registre isso na
coluna Observações (ex.: "a mapear pela assessoria") em vez de inventar nomes.

Inclua o veículo, o tipo (jornal/portal/rádio/TV) e, quando encontrar em fonte pública, o contato de
redação (e-mail/telefone). O que não achar, marque `[PESQUISA — confirmar contato]`. Não invente
e-mails, nomes de jornalistas nem veículos: só entra o que a busca confirmar.

Prompt sugerido para o subagente de cada cidade: "Pesquise a mídia jornalística de <Cidade/UF>:
jornais, portais de notícia, rádios e TVs locais; veículos regionais/estaduais que cobrem a cidade;
verticais de educação, cultura e sustentabilidade; universidades/institutos com assessoria; e canais
oficiais da prefeitura. Devolva em tiers, com veículo, tipo e contato de redação quando público.
Não invente contatos; marque como a confirmar o que não achar."

## Onde salvar

Por padrão, crie a entrega como **página no doc do Termo de Abertura do projeto no ClickUp**
(`clickup_create_document_page` ou `clickup_update_document_page` se já existir uma página
"Plano de Divulgação"), no mesmo doc onde estão o TAP e os PEPs, para tudo ficar junto. Se o usuário
preferir, gere também uma versão em Drive/HTML. Sempre entregue o link clicável ao final.

## Regras de marca NTICS (herdadas)

- Régua institucional: só "Lei Federal de Incentivo à Cultura"; sem logo do Ministério da Cultura e
  sem Governo do Brasil (diretriz pré-eleitoral). Cada PRONAC com régua própria.
- **Nunca** usar a régua institucional em post de rede social.
- Sem travessão em texto publicado; siglas abertas na 1ª ocorrência (ODS, ONU, ESG, RV).
- Números só da fonte canônica (TAP); nunca inventar citação, meta ou contato.
- Cuidado com claims ambientais absolutos quando o patrocinador for sensível (ver riscos no PEP).

## Referências

- Modelos de nível-alvo (ClickUp): "PLANO DE DIVULGAÇÃO - 117", "PLANO DE DIVULGAÇÃO 124" e
  "Plano de Divulgação, Projeto 133 (Workflow)". O 133 é o mais completo: traz Dados do Projeto com
  PRONACs e datas por cidade, narrativa âncora e princípio-mãe no Guia de Linguagem, a tabela-resumo de
  atividades com classificação `[ENTREGA MINC]`/PRONAC e fase, a descrição em parágrafo por atividade,
  a tabela de acessibilidade por atividade, e as mídias por cidade em tabela por Tier. Use-o como base
  estrutural; 117 e 124 ajudam nas mensagens por público.
- Fontes por projeto: TAP (Escopo + Indicadores, Comunicação) + PEP de cada patrocinador (14 seções).
