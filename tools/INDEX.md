# Tools — Índice Resumido

Scripts Python determinísticos organizados por função. **Navegue pelo sub-índice da área** para ver scripts individuais, APIs e status.

> Para dúvidas sobre payload Leonardo AI: `workflows/marketing/referencia/leonardo_ai_core.md`

## Mapa de áreas

| Área | Sub-índice | O que tem |
|---|---|---|
| `content-gen/` + `media/` | [index-conteudo.md](index-conteudo.md) | Carrosseis, artigos, capas, imagens Leonardo, Pillow, Gamma |
| `integrations/` + `research/` | [index-integracoes.md](index-integracoes.md) | ClickUp, Drive, Gmail, Pipedrive, Sembly, Perplexity, Airtable, GWS |
| `adobe/` | [index-operacoes.md](index-operacoes.md) | Illustrator, After Effects, JSX scripts |
| `publishing/` + `publish/` + `migration/` | [index-operacoes.md](index-operacoes.md) | Newsletter, GitHub Pages, Lovable→NTICS pipeline, Negócio Cultural |
| `reports/` | [index-operacoes.md](index-operacoes.md) | PMO diário/semanal: ClickUp → HTML → Gmail |
| `sync/` | [index-operacoes.md](index-operacoes.md) | secondbrain_sync (21h), projeto_sync, state.yaml |
| `meetings/` + `video/` + `secondbrain/` | [index-operacoes.md](index-operacoes.md) | Reuniões, Remotion, análise de vídeo, SecondBrain |
| `_tests/` | [index-operacoes.md](index-operacoes.md) | Experimentos — NÃO usar em produção |

## Estrutura de diretórios

```
tools/
├── content-gen/    # Carrosseis, artigos, capas visuais
├── media/          # Imagens (Leonardo AI, Unsplash, PDF)
├── adobe/          # Illustrator, After Effects, JSX
├── integrations/   # ClickUp, Drive, Gmail, Pipedrive, Sembly, Airtable
├── research/       # Perplexity, CSR news, SALIC
├── publishing/     # Newsletter, WordPress, Negócio Cultural
├── publish/        # GitHub Pages
├── migration/      # Lovable → ntics.com.br pipeline
├── reports/        # PMO diário e semanal
├── sync/           # ClickUp/Drive ↔ SecondBrain/state.yaml
├── meetings/       # Classificação de reuniões
├── video/          # Remotion + análise de vídeo
├── secondbrain/    # Ingestão e relações do vault
└── _tests/         # Experimentos (não produção)
```
