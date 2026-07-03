---
name: planejamento-redes-sociais
description: Gera o planejamento de redes sociais da NTICS a partir do ClickUp — levantamento do que foi entregue no período passado e do que está previsto para o próximo, análise por projeto e por pessoa, e proposta de pauta (≥1 vídeo por dia útil). Use quando o usuário pedir "planejamento de redes sociais", "planejamento semanal", "planejamento mensal", "relatório de redes sociais", "pauta de redes sociais" ou similar. Produz um resumo no chat e um dashboard HTML no padrão do repositório.
---

# Planejamento de Redes Sociais NTICS (ClickUp → relatório)

Modelo reutilizável. O usuário pede **`semanal`** ou **`mensal`** e esta skill faz todo o
levantamento no ClickUp, a análise e a proposta de pauta, entregando **(a)** um resumo em Markdown
no chat e **(b)** um dashboard HTML no padrão do repositório.

Pré-requisito: o **MCP do ClickUp** precisa estar conectado (ferramentas `clickup_*`). Se não
estiver, avise o usuário e pare.

Os detalhes de cada etapa estão nos arquivos de referência — leia o que precisar:
- `references/fontes-clickup.md` — onde os dados vivem no ClickUp e como descobri-los.
- `references/analise-e-proposta.md` — regras da análise e o algoritmo de proposta de pauta.
- `references/saida-html.md` — como clonar os templates e registrar no índice.

## Passo 0 — Modo e janelas de data

1. Descubra o modo: `semanal` ou `mensal`. Se o usuário não disser, **pergunte**; se estivermos na
   **1ª semana do mês**, sugira `mensal` como padrão.
2. Use a data de hoje (informada no contexto da sessão — nunca invente) para definir as janelas:
   - **semanal** → *período passado* = semana anterior (seg–dom); *próximo período* = próxima semana.
   - **mensal** → *período passado* = mês anterior; *próximo período* = próximo mês.
   Registre as datas exatas de início/fim de cada janela e use-as em todos os filtros.

## Passo 1 — Descobrir a fonte no ClickUp

Chame `clickup_get_workspace_hierarchy`. Localize (correspondência aproximada, case-insensitive) a
pasta **"Escritório de Projetos"** → subpasta/agrupamento **"Projetos Ativos"**, e as listas de
redes sociais (ex.: **"Kanban de redes sociais"**, **"Cronograma de redes sociais NTICS"**).
Anote os IDs encontrados e **liste ao usuário o que casou** (para ele corrigir se um nome divergir).
Detalhes e fallbacks em `references/fontes-clickup.md`.

## Passo 2 — Coletar as tarefas

Para cada lista de projeto ativo, ache a tarefa-pai **"Acompanhar redes sociais"** e puxe as
**subtarefas** (`clickup_get_task` com `subtasks=true`): *postar carrossel*, *postar vídeo*,
*criar/editar vídeo* (busque também "edição de vídeo"). Na lista de redes sociais, colete os
carrosséis com a tag **"institucional"** (ESG, projetos, notícia de projetos). Complemente com
`clickup_filter_tasks` / `clickup_search` por nome. Capture sempre **tags** (em especial
**"data fechada com cliente"** e **"institucional"**), **responsáveis**, **status** e **due date**.

## Passo 3 — Normalizar

Transforme cada item em `{tipo (carrossel|vídeo|edição), projeto, status
(concluído|planejado|backlog), data, responsável, tags[]}`. Resolva nomes de pessoas com
`clickup_resolve_assignees` / `clickup_find_member_by_name`. Papéis conhecidos: **Aline** = postagens
(e edita alguns vídeos), **Marcos** = edição de vídeo, designers **Marina**, **Alison** e outra
pessoa a descobrir dinamicamente. Não hard-code a terceira designer — derive dos responsáveis.

## Passo 4 — Separar por período

Divida os itens em **concluídos no período passado** × **previstos no próximo período**, conforme as
janelas do Passo 0. Itens em `backlog` sem data vão para uma bolsa "sem data confirmada".

## Passo 5 — Análise

Consolide (ver `references/analise-e-proposta.md`): nº de posts e nº de vídeos editados; **por
projeto** (quais postaram, quais ficaram silenciosos); **por pessoa** (quantos vídeos cada um editou,
quantos posts cada um fez); o que tem **data fechada com cliente** × o que **não tem**.

## Passo 6 — Proposta de pauta

Meta: **≥ 1 post de vídeo por dia útil** no próximo período. Mapeie os dias já cobertos, ache as
lacunas e, para **projetos em fase de finalização**, proponha **cortes / melhores momentos**
editados pela **Aline**, respeitando **no máximo 1 vídeo por dia para a Aline**. Monte um **rascunho
pronto da criação no ClickUp** (nome da subtarefa, lista, tarefa-pai, responsável = Aline, data)
**para aprovação** — **não crie tarefas automaticamente**. Algoritmo completo em
`references/analise-e-proposta.md`.

## Passo 7 — Saída (os dois formatos)

1. **Chat (Markdown):** resumo executivo com os KPIs do Passo 5, a proposta do Passo 6 e a tabela de
   rascunho para aprovação.
2. **HTML:** clone o template adequado numa pasta datada e preencha com os dados reais
   (ver `references/saida-html.md`):
   - **mensal** → `docs/projetos/redes-sociais-<mes>-<ano>/index.html`
     (modelo: `docs/projetos/redes-sociais-junho-2026/index.html`).
   - **semanal** → `reports/semana-<YYYY-MM-DD>/index.html`
     (modelo: `reports/semana-2026-05-23/index.html`) e adicione um card em `reports/index.html`.

## Aprovação e criação no ClickUp (opcional, após o relatório)

Só **depois** que o usuário aprovar a tabela de rascunho, use `clickup_create_task` para criar as
subtarefas de edição da Aline (uma por dia, respeitando o limite). Nunca crie antes da aprovação.
