# Tools — Operações, Publicação e Adobe
> Sub-índice de `tools/INDEX.md`. Publishing, migration, reports, sync, meetings, vídeo, Adobe e testes.

## adobe/

| Script | Propósito | Status |
|---|---|---|
| adapt_artwork_illustrator.py | Adapta arte para novo cliente | Ativo |
| adapt_motion_aftereffects.py | Adapta motion template After Effects | Ativo |
| apply_text_edits_illustrator.py | Aplica edições de texto PDF em .ai | Ativo |
| arte_impressao.py | Gera arte CMYK para gráfica | Stub |
| extract_kv_assets.py | Extrai paleta + SVG/PNG de .ai do KV | Ativo |
| kv_derivar.py | Deriva KV do projeto (Illustrator + Leonardo) | Stub |
| estampa_textil.py | Gera arte têxtil (avental, camiseta, dolma) | Stub |
| revisao_arte_pdf.py | Checks técnicos: CMYK, DPI, sangria, fontes | Stub |
| jsx/*.jsx | Scripts JSX invocados pelos .py acima | Vários |

## publishing/ e publish/

| Script | Propósito | Status |
|---|---|---|
| build_newsletter.py / send_newsletter.py / publish_to_brevo.py | Pipeline newsletter | Ativo |
| generate_project_site.py | Gera site de projeto via Jinja2 | Ativo |
| reformat_empreendedorismo.py | Reformata conteúdo para WordPress | Ativo |
| heygen_create_video.py | Cria vídeo no HeyGen via API | Ativo |
| publish/publish_html.py | Publica HTML em GitHub Pages | Ativo |
| _nc_*.py | Suite WordPress/TutorLMS Negócio Cultural | Ativo |

## migration/

Pipeline Lovable → ntics.com.br. Workflow: `criar_landing_ntics.md`.

| Script | Propósito | Status |
|---|---|---|
| lovable_to_ntics.py | Orquestrador principal | Ativo |
| build_site_model.py / build_all_models.py | Modelo da página a partir do scrape | Ativo |
| build_photo_assignment.py / inject_photos.py | Atribuição e injeção de fotos | Ativo |
| editorial_rewrite.py | Reescreve copy em tom NTICS | Ativo |
| refine_sites.py / adjust_sites.py | Ajustes pós-build | Ativo |
| upload_ntics.py / upload_new_sites.py | Upload via Code Snippets API | Ativo |
| generate_all_final.py | Pipeline end-to-end | Ativo |

## reports/

| Script | Propósito | Status |
|---|---|---|
| run_pmo_daily.py | Entrypoint diário (cron 8h) | Ativo |
| run_pmo_weekly.py | Entrypoint semanal (sexta 16h) | Ativo |
| aggregate_pmo_metrics.py / aggregate_pmo_weekly.py | Agregação de métricas ClickUp | Ativo |
| generate_pmo_summary.py / generate_weekly_summary.py | Resumo via Claude Haiku | Ativo |
| render_pmo_html.py / render_pmo_weekly.py | Render Jinja2 → HTML | Ativo |
| send_pmo_email.py | Envio Gmail (Lucas/Bruna/Abílio) | Ativo |

## sync/

| Script | Propósito | Status |
|---|---|---|
| **secondbrain_sync.py** | **Sync ClickUp → SecondBrain diário 21h** | **Ativo** |
| projeto_sync.py | Sync state.yaml ↔ ClickUp + Gmail | Ativo |
| read_drive_xlsx.py | Lê XLSX do Drive sem download | Utilitário |
| _form_extract.py / _form_fill_132.py / _form_read_api.py | Formulários Samarco (132) | Por-projeto |

**`secondbrain_sync.py --slug <slug> --dry-run`** para testar; output em `SecondBrain/projetos/{slug}/tasks-summary.md`.

## meetings/ e video/

| Script | Propósito | Status |
|---|---|---|
| meetings/classify_meeting.py | Classifica reunião via Claude API | Ativo |
| video/remotion-video/ | Vídeos React/Remotion (Node.js) | Ativo |
| video/video_analysis/ | Análise e edição de vídeos Python | Ativo |

## secondbrain/

| Script | Propósito | Status |
|---|---|---|
| update_profiles_from_drive.py | Atualiza perfis de projeto a partir do Drive | Ativo |
| build_relations.py | Constrói relações entre notas SecondBrain | Ativo |
| ingest_projetos_anteriores.py | Ingesta projetos históricos no vault | Ativo |

## _tests/

Scripts experimentais — NÃO invocar em produção: `teste_estilo_mindset.py`, `teste_og_image.py`, `teste_perplexity_imagens.py`, `teste_unsplash_noticias.py`.
