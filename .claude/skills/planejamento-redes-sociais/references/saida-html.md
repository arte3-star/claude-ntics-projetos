# Saída HTML — clonar os templates existentes

Não recrie o layout do zero. **Clone** o template do padrão certo e substitua os dados. Mantenha o
estilo (inline CSS/JS, sem build), pois o repositório é HTML puro publicado via GitHub Pages.

## Mensal

- **Modelo:** `docs/projetos/redes-sociais-junho-2026/index.html`.
- **Destino:** `docs/projetos/redes-sociais-<mes>-<ano>/index.html` (ex.: `redes-sociais-julho-2026/`).
- Elementos do template (reutilize as mesmas classes):
  - **KPI cards**: `.card-grid` > `.kpi-card {blue|orange|red|green|amber|purple}` com
    `.kpi-n` (número), `.kpi-l` (rótulo), `.kpi-sub` (detalhe). Use para os KPIs da Parte A.
  - **Calendário**: `.cal-wrapper > .cal` com `.cal-header`, `.cal-week-label`, `.cal-day`
    (`.cal-day-num`) e eventos `.cal-event` nas variantes `ev-carrossel`, `ev-video`, `ev-artigo`,
    `ev-post-proj`, `ev-campo`. Posicione os posts/vídeos do próximo período aqui.
  - **Legenda** de tipos (`.section-nav` / bloco de legenda) e **seções** com `.section-title`.
  - **Pipeline** de vídeos com badges de status; **bloco de "Em planejamento — sem data confirmada"**;
    **bloco de pendências/perguntas** — use para os itens sem data fechada e para as pendências.
  - **Rodapé**: "Relatório gerado em <hoje> · Dados extraídos do ClickUp". Atualize a data (use a data
    real da sessão, não invente) e a descrição da lista de origem.
- Inclua a **proposta de pauta** (cortes da Aline) como uma seção destacada, e a **tabela de rascunho
  para aprovação** — deixe claro que ainda não foi criada no ClickUp.

## Semanal

- **Modelo:** `reports/semana-2026-05-23/index.html`.
- **Destino:** `reports/semana-<YYYY-MM-DD>/index.html` (data da segunda-feira da semana do relatório).
- Depois de gerar, **registre no índice** `reports/index.html`: adicione um `<a class="card"
  href="semana-<YYYY-MM-DD>/">` com um `.title` no mesmo formato dos cards existentes
  (ex.: "Relatório Semanal · N projetos em campo · X atividades").

## Regras
- Preencher **somente com dados reais** vindos do ClickUp; nunca inventar números, datas ou nomes.
- Onde faltar dado, mostrar explicitamente (ex.: "sem data confirmada", "a confirmar com cliente").
- Não alterar os templates-modelo originais; sempre trabalhar na nova pasta datada.
- Ao final, informe ao usuário os caminhos dos arquivos gerados/alterados.
