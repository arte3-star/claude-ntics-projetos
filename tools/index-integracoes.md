# Tools — Integrações e Pesquisa
> Sub-índice de `tools/INDEX.md`. Conectores externos, APIs e pesquisa de dados.

## integrations/

| Script | Propósito | Status |
|---|---|---|
| create_clickup_tasks.py | Cria tasks ClickUp genéricas | Ativo |
| create_social_media_tasks.py | Cria tasks de conteúdo no ClickUp | Ativo |
| update_clickup_drive_links.py | Atualiza links Drive nas tasks ClickUp | Ativo |
| upload_to_drive.py / publicar_drive.py | Upload de arquivos para o Drive | Ativo |
| drive_2026_discover.py / scaffold.py | Descoberta e scaffolding de pasta Drive 2026 | Ativo |
| drive_2026_reorg.py | Reorganização Drive 2026 | One-shot (executado 2026-04-23) |
| drive_import_designer_assets.py | Baixa peças gráficas de projetos ativos | Ativo |
| read_google_doc.py | Lê conteúdo de Google Docs | Ativo |
| update_learning_registry.py | Atualiza registro de aprendizado (Sheets) | Ativo |
| create_pipedrive_note.py | Cria nota em deal Pipedrive | Ativo |
| pipedrive_match_deal.py | Match de deal por email | Ativo |
| sembly_pull_meetings.py / sembly_to_pipedrive.py | Polling Sembly → Pipedrive (4x/dia) | Ativo |
| clickup_pull_projetos_ntics.py / clickup_pull_sprint.py / clickup_pull_overdue_comments.py | Pull ClickUp para PMO | Ativo |
| clickup_remove_list_dependencies.py | Utilitário de limpeza de dependências | Utilitário |
| drive_find_cronograma.py / parse_cronograma.py | Busca e parseia cronograma XLSX | Ativo |
| update_lps_2026.py | Atualização em massa de LPs via Code Snippets | Ativo |
| webhook_server.py | Servidor webhook para n8n | Ativo |
| gws/forms_create.py | Cria Google Form de indicadores | Ativo |
| gws/gws_cli.py | CLI Gmail/Calendar/Drive | Ativo |
| gws/gws_auth.py | Autenticação Google Workspace | Ativo |
| gws/organize_meet_transcripts.py | Organiza transcrições de reuniões no Drive | Ativo |
| gws/slides_template_create.py | Cria template Google Slides | Stub |
| airtable/ | Sync projetos NTICS ↔ Airtable (setup_base, sync_projects, relatorio_diario) | Ativo |

## research/

| Script | Propósito | Status |
|---|---|---|
| search_perplexity.py | Busca notícias ESG via Perplexity | Ativo |
| research_csr_news.py | Pesquisa CSR news via Perplexity | Ativo |
| parse_salic_excel.py | Parseia Excel SALIC local | Ativo |
