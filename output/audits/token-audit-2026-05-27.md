# Token Audit — WAT Framework
**Data:** 2026-05-27  
**Auditor:** Claude Sonnet 4.6 (instância autônoma)  
**Escopo:** Repositório `G:/O meu disco/Claude-NTICS-Projetos` + memória em `~/.claude/projects/`

---

## 1. Custo Base por Conversa (contexto automático)

Arquivos carregados **em toda conversa**, antes de qualquer pergunta do usuário:

| Arquivo | Bytes | Tokens (÷4) | Tipo de carga |
|---|---|---|---|
| `~/.claude/CLAUDE.md` (global) | 300 | 75 | automático (harness) |
| `CLAUDE.md` (projeto) | 6.660 | 1.665 | automático (harness) |
| `MEMORY.md` (índice memória) | 9.574 | **2.394** | system-reminder a cada turno |
| Lista de skills disponíveis | ~12.000 est. | ~3.000 | system-reminder (149 skills listadas) |
| Lista de ferramentas MCP diferidas | ~8.000 est. | ~2.000 | system-reminder (150+ tools listadas) |
| **Total base por conversa** | **~36.534** | **~9.134** | — |

> A lista de skills (149 itens) e tools MCP diferidas (~150 itens) consumem estimados 5.000 tokens fixos via system-reminder a cada conversa. Não são arquivos do repositório, mas são overhead real.

---

## 2. Workflows e SOPs — Inventário Completo

**Total:** 90 arquivos `.md` — **634.432 bytes — 158.608 tokens** (carregados sob demanda)

### Top 10 maiores workflows

| # | Arquivo | Bytes | Tokens |
|---|---|---|---|
| 1 | `workflows/marketing/referencia/leonardo_ai_cookbook.md` | 29.206 | **7.302** |
| 2 | `workflows/marketing/producao/carrosseis/carrossel_projeto_ativo_cliente.md` | 27.801 | **6.950** |
| 3 | `workflows/marketing/producao/carrosseis/carrossel_case_projeto.md` | 20.374 | **5.094** |
| 4 | `workflows/escritorio-projetos/briefing_videomaker.md` | 19.615 | **4.904** |
| 5 | `workflows/knowledge/escritorio_projetos_referencia.md` | 16.502 | **4.126** |
| 6 | `workflows/INDEX.md` | 15.381 | **3.845** |
| 7 | `workflows/marketing/producao/newsletter.md` | 15.224 | **3.806** |
| 8 | `workflows/escritorio-projetos/roteiro_video_completo.md` | 14.149 | **3.537** |
| 9 | `workflows/marketing/referencia/csr_base_conhecimento.md` | 13.688 | **3.422** |
| 10 | `workflows/marketing/producao/artigo_mensal.md` | 13.293 | **3.323** |

**Custo de leitura do `workflows/INDEX.md` como porta de entrada:** 3.845 tokens por invocação de workflow. É o arquivo carregado antes de qualquer SOP.

### Redundâncias identificadas

- `leonardo_ai_cookbook.md` (7.302 tokens) e `leonardo_ai_core.md` (1.989 tokens) cobrem o mesmo domínio. O cookbook é carregado "sob demanda" mas na prática é lido toda vez que há erro de API.
- Três workflows de carrossel somam **20.337 tokens**: `carrossel_projeto_ativo_cliente.md` + `carrossel_case_projeto.md` + `carrossel_educativo.md`. Todos compartilham estrutura de prompt Leonardo AI que poderia viver em um único arquivo de referência.
- `workflows/knowledge/escritorio_projetos_referencia.md` (4.126 tokens) é uma base de conhecimento, não um SOP — nenhuma step-by-step. Poderia ser comprimida em 50%.

---

## 3. Skills — Análise por Complexidade

**Total:** 114 arquivos em `.claude/skills/` — **536.383 bytes — 134.096 tokens**

### Skills de infraestrutura (pesadas, uso raro)

| Skill | Bytes totais | Tokens | Arquivos carregados |
|---|---|---|---|
| `skill-creator/` | 232.134 | **58.034** | 15 arquivos (scripts, agents, refs, viewer) |
| `remotion-best-practices/` | 120.077 | **30.019** | SKILL.md + 5 rules/*.md |

> **`skill-creator`** soma 58K tokens e é claramente uma skill de meta-desenvolvimento, não de produção diária. Nunca aparece como invocada nos workflows do Lucas. Quando invocada, carrega scripts Python, HTML do viewer, agentes comparadores — tudo junto.

> **`remotion-best-practices`** carrega 5 arquivos de regras simultaneamente (transitions, extract-frames, display-captions, audio-visualization, timing = 30K tokens). É uma skill de nicho (produção de vídeo com Remotion/React) raramente usada.

### Skills de produção pesadas (carregam workflow inteiro)

| Skill | SKILL.md | Tokens SKILL.md | Workflow referenciado |
|---|---|---|---|
| `editar-negocio-cultural` | 8.160 | 2.040 | Carrega conteúdo inline |
| `editar-linkedin` | 7.085 | 1.771 | Carrega conteúdo inline |
| `postar-linkedin` | 7.006 | 1.752 | Carrega conteúdo inline |
| `criar-landing-ntics` | 6.946 | 1.737 | Ref. `workflows/landing_v2_ntics.md` |
| `projeto-abrir` | 6.472 | 1.618 | Ref. `workflows/projeto-abrir.md` |
| `projeto-retrospectiva` | 5.107 | 1.277 | Carrega conteúdo inline |

> **Padrão de ineficiência:** skills como `editar-negocio-cultural` e `editar-linkedin` duplicam o conteúdo do workflow dentro do SKILL.md em vez de apenas referenciar o arquivo de workflow. Duplo custo quando ambos são lidos.

---

## 4. Tools Python — Análise de Outputs

**Total:** 224 scripts — **2.122.873 bytes — 530.718 tokens** (código não vai para contexto diretamente)

> Scripts Python **não são carregados no contexto** — só são invocados. O risco é o **output que retornam** ao contexto.

### Scripts com potencial de output verboso

| Script | Bytes | Risco de output |
|---|---|---|
| `tools/content-gen/gerar_carrossel_noticias_v2.py` | 75.175 | ALTO — gera JSON completo de carrossel |
| `tools/content-gen/gerar_educativos_3semanas.py` | 51.564 | ALTO — batch de 3 semanas de conteúdo |
| `tools/airtable/sync_projects.py` | 42.559 | MÉDIO — sync retorna registros Airtable |
| `tools/sync/projeto_sync.py` | 25.381 | MÉDIO — sync ClickUp retorna tarefas |
| `tools/content-gen/gerar_artigo_site.py` | 30.405 | ALTO — artigo completo no stdout |

### `tools/INDEX.md` — o culpado invisível

**20.338 bytes → 5.085 tokens** carregados sempre que o CLAUDE.md instrui a "consultar tools/INDEX.md". É o maior índice de referência do repositório. Contém descrição de 224 scripts com workflows e status — muito mais do que o necessário para navegar.

---

## 5. Memória — Índice e Entradas Individuais

**Total do vault:** 125.255 bytes — **31.314 tokens**

### MEMORY.md (índice injetado a cada turno)

**9.574 bytes — 2.394 tokens** — 46 entradas, todas injetadas via `system-reminder` em **cada turno de cada conversa**. Não é carregado sob demanda — é overhead fixo.

### Entradas mais pesadas (carregadas quando relevantes)

| Arquivo | Bytes | Tokens | Tipo |
|---|---|---|---|
| `projeto_128_cnh_festival_agricultura.md` | 12.327 | 3.082 | projeto ativo |
| `projeto_estacao_samarco_plataforma.md` | 11.467 | 2.867 | projeto ativo |
| `projeto_estacao_samarco_app_gamificado.md` | 8.863 | 2.216 | projeto ativo |
| `projeto_estacao_samarco.md` | 8.578 | 2.145 | projeto ativo |
| `projeto_129_cnh_agrofuturo_escolas.md` | 8.166 | 2.042 | projeto ativo |

> Os 3 arquivos `projeto_estacao_samarco*.md` somam **7.228 tokens** e descrevem o mesmo projeto em 3 facetas diferentes (estrutura geral, plataforma TutorLMS, app gamificado). Poderiam ser consolidados em um único arquivo de projeto com seções.

### Entradas candidatas a remoção/consolidação

- `feedback_claudio_termo_claude.md` (1.397 tokens) — regra trivial, já internalizada
- `feedback_browser_automation.md` — cobre comportamento padrão esperado
- `feedback_ler_antes_de_atualizar.md` — deveria ser instrução no CLAUDE.md, não memória
- `feedback_git_desktop_ini_gdrive.md` — procedimento técnico específico, raramente necessário

---

## 6. Brand Book — Custo de Referência

**Total:** 194.125 bytes — **48.531 tokens** (carregados sob demanda)

| Arquivo | Bytes | Tokens | Frequência de uso |
|---|---|---|---|
| `brand-story.md` | 19.723 | 4.931 | baixa (contexto histórico) |
| `dos-and-donts.md` | 18.626 | 4.657 | baixa (revisão de conteúdo) |
| `tom-de-voz.md` | 14.366 | 3.592 | alta (todo conteúdo NTICS) |
| `mensagens-chave.md` | 13.998 | 3.500 | média |
| `projetos-carrossel.yaml` | 12.706 | 3.177 | alta (carrosseis) |
| `brand-data.yaml` | 5.824 | 1.456 | alta (números/dados) |
| `cores.md` | 9.072 | 2.268 | média (design) |

**Problema:** O CLAUDE.md instrui "consulte `brand-book/data/brand-data.yaml` (números) e `brand-book/02-identidade-verbal/tom-de-voz.md` (tom)" — dois arquivos específicos. Mas na prática, quando há dúvida de branding, o modelo frequentemente carrega todo o diretório `brand-book/`.

**`brand-data.yaml` (1.456 tokens)** + **`tom-de-voz.md` (3.592 tokens)** = 5.048 tokens é o custo mínimo necessário para qualquer conteúdo NTICS.

---

## 7. Padrões de Ineficiência Sistêmica

### 7.1 Contexto Duplicado CLAUDE.md × Workflows

O `CLAUDE.md` do projeto (1.665 tokens) contém:
- Seção "Leonardo AI" com regras e ponteiros
- Seção "Protocolo de Aprendizado" com instruções de captura
- Seção "Verificação antes de declarar sucesso" com regras por ferramenta

Esses mesmos temas aparecem nos workflows de marketing e nos SKILL.md. Estimativa de duplicação: **~400 tokens de contexto sobrepostos** entre CLAUDE.md e os workflows mais frequentes.

### 7.2 Índices sobrecarregados

| Índice | Bytes | Tokens | Problema |
|---|---|---|---|
| `tools/INDEX.md` | 20.338 | 5.085 | Descreve 224 scripts com workflow, API e status |
| `workflows/INDEX.md` | 15.381 | 3.845 | 90 SOPs listados com descrições longas |
| `SecondBrain/INDEX.md` | 9.991 | 2.498 | Gateway para o vault — carregado antes de qualquer consulta |

Os índices foram projetados para serem "portas de entrada" mas na prática o modelo os lê inteiros antes de navegar para o arquivo específico. Custo médio de overhead por operação: **~11.428 tokens** (soma dos 3 índices).

### 7.3 Skills de nicho com payload enorme

`remotion-best-practices` (30K tokens) e `skill-creator` (58K tokens) são invocados raramente mas carregam payload massivo. Se invocadas por acidente ou por ambiguidade de nome, adicionam 88K tokens ao contexto.

### 7.4 MEMORY.md cresce sem poda

Com 46 entradas e 2.394 tokens fixos por conversa, o índice de memória já representa um custo constante significativo. Tende a crescer com o tempo sem que entradas antigas sejam consolidadas ou removidas.

---

## Sumário de Custo Estimado por Componente

| Componente | Bytes totais | Tokens totais | Custo/conversa típica |
|---|---|---|---|
| Contexto fixo (CLAUDE.md + MEMORY.md) | 16.534 | 4.134 | **100% — sempre** |
| System-reminders (skills + tools MCP) | ~20.000 est. | ~5.000 | **100% — sempre** |
| workflows/INDEX.md (porta de entrada) | 15.381 | 3.845 | ~60% das conversas |
| tools/INDEX.md | 20.338 | 5.085 | ~40% das conversas |
| Workflow ativo médio (top 10 avg.) | 16.000 | 4.000 | ~80% das conversas |
| Skill SKILL.md (média) | 4.500 | 1.125 | por invocação |
| Brand book mínimo (tom + dados) | 20.190 | 5.048 | todo conteúdo NTICS |
| Memory files projeto (2-3 por sessão) | 20.000 | 5.000 | sessões de projeto |
| **Estimativa conversa típica de marketing** | — | **~28.000** | workflows + brand + skill |
| **Estimativa conversa típica de projeto** | — | **~24.000** | workflows + memory + skill |

---

## Top 5 Culpados pelo Consumo Excessivo

### #1 — `skill-creator` (58.034 tokens por invocação)
Skill de meta-desenvolvimento com 15 arquivos (scripts Python, HTML de viewer, agents comparadores). **Nunca usada na produção diária do Lucas.** Se invocada por engano — ou como dependência de outra skill — injeta 58K tokens de uma vez.

### #2 — `MEMORY.md` injetado a cada turno (2.394 tokens × infinitas conversas)
O índice de memória é carregado via system-reminder em **todo turno de toda conversa**, independente de relevância. Com 46 entradas cobrindo desde Samarco até feedback de CSS, a maioria das entradas é irrelevante para a tarefa em curso. Acumula custo sem retorno proporcional.

### #3 — `tools/INDEX.md` (5.085 tokens, carregado frequentemente)
O maior índice de referência do repositório. Com 224 scripts descritos em detalhe, é lido toda vez que o modelo navega por ferramentas disponíveis. Frequência estimada: 40% das conversas técnicas.

### #4 — `remotion-best-practices` (30.019 tokens por invocação)
Cinco arquivos de regras carregados simultaneamente para uma skill de nicho (vídeo com React/Remotion). Uso real: raramente. Quando invocada, rivaliza em peso com 8 workflows médios simultâneos.

### #5 — Trilogia `projeto_estacao_samarco*.md` (7.228 tokens em 3 arquivos)
Três arquivos de memória sobre o mesmo projeto, carregados juntos quando há contexto de Samarco. A fragmentação em 3 arquivos foi feita para organização mas resulta em leitura triplicada. Projeto provavelmente encerrado ou em manutenção — candidato a arquivamento.

---

## 5 Recomendações Priorizadas

### Rec. 1 — Arquivar ou mover `skill-creator` para fora do `.claude/skills/`
**Impacto:** Elimina risco de 58.034 tokens por invocação acidental.  
**Como:** Mover `.claude/skills/skill-creator/` para `tools/skill-creator/` ou `docs/skill-creator/`. Não é uma skill de produção — é infra de desenvolvimento de skills. Pode ser chamada via script direto, sem precisar estar no diretório de skills carregável pelo harness.  
**Economia estimada:** 58.034 tokens eliminados do risco por conversa. Em conversas que a invocam: 100% de redução nesse componente.

### Rec. 2 — Reduzir MEMORY.md: consolidar 3 arquivos Samarco + podar entradas obsoletas
**Impacto:** Reduz tokens fixos injetados a cada turno.  
**Como:**  
  - Consolidar `projeto_estacao_samarco.md` + `projeto_estacao_samarco_plataforma.md` + `projeto_estacao_samarco_app_gamificado.md` em um único `projeto_estacao_samarco.md` com 3 seções. Economia: ~4.000 tokens quando o projeto é referenciado.  
  - Remover entradas triviais do MEMORY.md: `feedback_claudio_termo_claude.md`, `feedback_browser_automation.md` (regras óbvias já internalizadas).  
  - Migrar `feedback_ler_antes_de_atualizar.md` para o próprio CLAUDE.md como instrução direta.  
**Economia estimada:** ~800 tokens no índice MEMORY.md + ~4.000 tokens quando Samarco é contexto ativo.

### Rec. 3 — Dividir `tools/INDEX.md` em mini-índices por área
**Impacto:** Reduz de 5.085 tokens para ~500 tokens por consulta direcionada.  
**Como:** Criar `tools/index-content-gen.md`, `tools/index-reports.md`, `tools/index-sync.md` etc. O `tools/INDEX.md` principal vira apenas um sumário de 1 linha por área (= 20 linhas, ~200 tokens) apontando para os sub-índices. O CLAUDE.md já instrui leitura cirúrgica — o índice plano é que força a leitura integral.  
**Economia estimada:** 4.500 tokens por consulta a tools (redução de 90%).

### Rec. 4 — Comprimir `workflows/INDEX.md` para formato tabular mínimo
**Impacto:** Reduz de 3.845 tokens para ~800 tokens.  
**Como:** O INDEX.md atual tem descrições longas por workflow. Converter para tabela com 3 colunas: `workflow | área | trigger-keywords`. Sem parágrafos explicativos — o modelo navega para o arquivo de SOP para detalhes. Economia: ~3.000 tokens por consulta de roteamento.  
**Economia estimada:** ~3.000 tokens em 60% das conversas = ~1.800 tokens médios por conversa.

### Rec. 5 — Criar `brand-book/QUICK.md` com os 5 fatos essenciais NTICS
**Impacto:** Evita carregar `tom-de-voz.md` (3.592 tokens) e `brand-data.yaml` (1.456 tokens) toda vez.  
**Como:** Arquivo de 400-600 tokens com: boilerplate institucional validado, 6 números-chave (1.060 projetos / 11mi pessoas / etc.), 5 regras de tom ("não usar travessão", "expandir siglas", "CTA = acesse o link abaixo"), e ponteiros para os arquivos completos quando precisar de mais detalhe. O CLAUDE.md aponta para `brand-book/QUICK.md` como primeira consulta.  
**Economia estimada:** ~4.600 tokens em toda conversa de conteúdo NTICS (redução de 91% no custo de branding).

---

## Estimativa Consolidada de Economia

| Recomendação | Tokens economizados | Frequência de impacto |
|---|---|---|
| Rec. 1 — Arquivar skill-creator | 58.034 | por invocação (risco eliminado) |
| Rec. 2 — Consolidar Samarco + podar memória | ~4.800 | sessões com contexto Samarco |
| Rec. 3 — Mini-índices para tools | ~4.500 | 40% das conversas técnicas |
| Rec. 4 — Compactar workflows/INDEX.md | ~3.000 | 60% das conversas |
| Rec. 5 — brand-book/QUICK.md | ~4.600 | todo conteúdo NTICS |
| **Total potencial (sessão típica marketing)** | **~12.100** | conversas frequentes |

> Estimativa conservadora: implementar as 5 recomendações pode reduzir o custo de uma conversa típica de marketing de ~28.000 tokens para ~15.900 tokens — redução de **43%** no custo de contexto por sessão.

---

## Notas Metodológicas

- **Taxa de estimativa:** 1 token = 4 bytes (GPT-style; Claude pode ser ligeiramente diferente para português)
- **Frequências:** estimadas com base na leitura do CLAUDE.md, padrões de workflows e MEMORY.md
- **Ferramentas MCP e system-reminders** são overhead do harness, não do repositório — listados para completude mas não controláveis pelo projeto
- `tools/` Python não entra no custo de tokens do contexto — apenas seus outputs retornados ao modelo

---

*Gerado por Claude Sonnet 4.6 em 2026-05-27*
