# PMO NTICS — painel mensal de planejamento

Dashboard do Escritório de Projetos, servido por GitHub Pages.

**No ar:** https://arte3-star.github.io/claude-ntics-projetos/dashboards/pmo/

## Arquivos

- `index.html` — a casca do painel (estrutura, CSS, lógica; Gantt anual + visões do mês + calendário de campo + detalhado por semanas). Dados injetados inline nas constantes JS (`PROJECTS`, `SEMANAS_DATA`, `CAL_CAMPO`, `TRANSVERSAL`, `PROJ_MES`, `PHASE`, `IMGS`, `ROTINAS_AREA`, `COORD_NAMES`, `COORD_ORDER`).
- `julho-2026-clickup.html` — snapshot do mês de julho/2026 puxado do ClickUp.
- `assets/` — as 14 fotos dos coordenadores + logo (referenciadas por caminho relativo `assets/*.jpg`).

## Como atualizar o mês

O painel é gerado pela skill **`planejamento-mensal`** (nível de usuário), a partir de dados ao vivo do ClickUp. A skill contém a lógica de extração; o HTML é a saída. Ver a skill para o fluxo completo.

## Origem

Migrado em 19/07/2026 do setup do Abílio (`jrabilio/pmo`) para o repositório da NTICS (`arte3-star/claude-ntics-projetos`), sem dependência de GitHub externo.
