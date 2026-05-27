# Workflows Index

Template e convenções em [_TEMPLATE.md](_TEMPLATE.md) e [CONVENTIONS.md](CONVENTIONS.md).

## Escritório de Projetos (`escritorio-projetos/`)

| Workflow | Arquivo | Comando |
|---|---|---|
| Briefing Videomaker | `briefing_videomaker.md` | — |
| Termo de Abertura | `termo_abertura.md` | — |
| Perfil Estratégico | `perfil_estrategico.md` | — |
| Plano de Divulgação | `plano_divulgacao.md` | — |
| Roteiro Vídeo Completo | `roteiro_video_completo.md` | — |
| Briefing Website | `briefing_website.md` | — |
| Engenhoca Prestação Contas | `engenhoca_prestacao_contas.md` | — |
| Processamento de Reuniões | `process_meeting_transcript.md` | — |
| Sembly → Pipedrive | `sembly_to_pipedrive.md` | — |
| Criar Site do Projeto | `criar_site_projeto.md` | `/criar-site` |
| Form de Indicadores | `form_indicadores_projeto.md` | — |
| Email Calendário Social | `email_calendario_social.md` | — |
| Relatório Diário PMO | `relatorio_diario_pmo.md` | `/relatorio-pmo` |
| Relatório Semanal PMO | `relatorio_semanal_pmo.md` | `/relatorio-pmo-semanal` |
| KV Derivar Projeto | `kv_derivar_projeto.md` | `/kv-derivar` |
| Arte Impressão CMYK | `arte_impressao_cmyk.md` | `/arte-impressao-cmyk` |
| Estampa Têxtil | `estampa_textil.md` | `/estampa-textil` |
| Projeto Abrir | `projeto-abrir.md` | `/projeto-abrir` |
| Projeto Retrospectiva | `projeto-retrospectiva.md` | `/projeto-retrospectiva` |
| Projeto Tasks Sync | `projeto-tasks-sync.md` | `/projeto-tasks-sync` |
| Formalização de Fornecedores | `formalizacao_fornecedores.md` | — |

**Cadeia típica:** Perfil Patrocinador → Termo de Abertura → Plano Divulgação → `/briefing-video` (Roteiro + Carrossel) → Briefing Website → Criar Site

## Inscrição de Projetos (`inscricao-projetos/`)

| Workflow | Arquivo |
|---|---|
| Estruturador Lei Rouanet | `estruturador_rouanet.md` |
| Conselheiro SALIC | `conselheiro_salic.md` |
| Conselheiro Lei Reciclagem | `conselheiro_reciclagem.md` |

## Marketing — Produção (`marketing/producao/`)

| Workflow | Arquivo | Comando |
|---|---|---|
| Plano Mensal | `plano_mensal.md` | `/plano-mensal` |
| Roteiro Vídeo | `roteiro_video.md` | `/roteiro-video` |
| Artigo Mensal | `artigo_mensal.md` | `/artigo-mensal` |
| Newsletter | `newsletter.md` | `/newsletter` |
| Artigo Site | `artigo_site.md` | `/artigo-site` |
| Artigo Notícias Site | `artigo_noticias_site.md` | — |
| Vetorizar | `vetorizar_imagem.md` | `/vetorizar` |
| Post Instagram | `posts/post-instagram.md` | `/post-instagram` |
| Google Slides Template | `google_slides_template.md` | `/google-slides-template` |
| Revisão Arte Impressão | `../revisao/revisao_arte_impressao.md` | `/revisao-arte-impressao` |
| Landing Pré-Projeto | `landing_preprojeto_ntics.md` | `/criar-landing-preprojeto` |
| Landing v2 | `landing_v2_ntics.md` | `/criar-landing-v2` |
| Publicar Drive | `../publicar_drive.md` | `/publicar-drive` |
| Publicar GitHub Pages | `../../publicar_github_pages.md` | — |

## Marketing — Carrosseis (`marketing/producao/carrosseis/`)

| Tipo | Arquivo | Comando |
|---|---|---|
| Notícias ESG | `carrossel_noticias.md` | `/carrossel-noticias` |
| Educativo ESG | `carrossel_educativo.md` | `/carrossel-educativo` |
| Case Projeto | `carrossel_case_projeto.md` | `/carrossel-case` |
| Projeto Ativo Cliente | `carrossel_projeto_ativo_cliente.md` | `/carrossel-cliente` |
| Briefing Carrossel+Vídeo | `briefing_carrossel_video.md` | `/briefing-video` |
| Capa de Vídeo | `../videos/capa_video.md` | `/capa-video` |

**Cadeia editorial:**
```
/plano-mensal → agente criador semanal (domingo 20h)
  ├→ /carrossel-educativo (segunda)
  ├→ artigo_noticias_site → /carrossel-noticias (terça)
  ├→ /roteiro-video (quarta)
  └→ /carrossel-case (quinta)
/artigo-mensal (fim do mês) → /artigo-site → /newsletter
/carrossel-cliente (por projeto ativo — pré/durante/pós)
```

## Marketing — Agentes (`marketing/agentes/`)

| Agente | Arquivo | Trigger |
|---|---|---|
| Criador Semanal | `agente_criador_semanal.md` | Domingo 20h |
| Revisor Semanal | `agente_revisor_semanal.md` | Segunda 8h |
| Ajustes Tempo Real | `agente_ajustes_tempo_real.md` | Comentário ClickUp |
| Publicador | `agente_publicador.md` | Status "aprovado" ClickUp |

## Marketing — Referência (`marketing/referencia/`)

| Doc | Arquivo |
|---|---|
| **Leonardo AI Core** (porta de entrada) | `leonardo_ai_core.md` |
| Leonardo AI Cookbook (erros, exemplos) | `leonardo_ai_cookbook.md` |
| LinkedIn Strategy | `linkedin_strategy.md` |
| Uso de Squads | `uso_squads_marketing.md` |
| Time Mídias Sociais | `team_midias_sociais.md` |
| Time Design Conteúdo | `team_design_conteudo.md` |

## APIs de Conteúdo

| API | Uso | Variável |
|---|---|---|
| Leonardo AI | Imagens (nano-banana-2, 4:5) | `LEONARDO_API_KEY` |
| Perplexity | Notícias ESG (sonar-pro) | `PERPLEXITY_API_KEY` |
| Unsplash | Imagens stock (fallback) | `UNSPLASH_API_KEY` |
| Gmail | Drafts de newsletter (MCP) | Google OAuth |
| Brevo | Email marketing em massa | `BREVO_API_KEY` |
| Serper | Google Images para newsletter | `SERPER_API_KEY` |

## Skills → Workflows

| Comando | Workflow correspondente |
|---|---|
| `/plano-mensal` | `marketing/producao/plano_mensal.md` |
| `/carrossel-noticias` | `marketing/producao/carrosseis/carrossel_noticias.md` |
| `/carrossel-educativo` | `marketing/producao/carrosseis/carrossel_educativo.md` |
| `/carrossel-case` | `marketing/producao/carrosseis/carrossel_case_projeto.md` |
| `/carrossel-cliente` | `marketing/producao/carrosseis/carrossel_projeto_ativo_cliente.md` |
| `/briefing-video` | `marketing/producao/carrosseis/briefing_carrossel_video.md` |
| `/post-instagram` | `marketing/producao/posts/post-instagram.md` |
| `/capa-leonardo` | `marketing/referencia/leonardo_ai_core.md` |
| `/capa-video` | `marketing/producao/videos/capa_video.md` |
| `/criar-landing-ntics` | `marketing/referencia/criar_landing_ntics.md` |
| `/criar-landing-preprojeto` | `marketing/producao/landing_preprojeto_ntics.md` |
| `/criar-landing-v2` | `marketing/producao/landing_v2_ntics.md` |
| `/publicar-drive` | `marketing/publicar_drive.md` |
| `/relatorio-pmo` | `escritorio-projetos/relatorio_diario_pmo.md` |
| `/relatorio-pmo-semanal` | `escritorio-projetos/relatorio_semanal_pmo.md` |
| `/projeto-abrir` | `escritorio-projetos/projeto-abrir.md` |
| `/projeto-retrospectiva` | `escritorio-projetos/projeto-retrospectiva.md` |
| `/projeto-tasks-sync` | `escritorio-projetos/projeto-tasks-sync.md` |
| `/criar-site` | `escritorio-projetos/criar_site_projeto.md` |
| `/kv-derivar` | `escritorio-projetos/kv_derivar_projeto.md` |
| `/arte-impressao-cmyk` | `escritorio-projetos/arte_impressao_cmyk.md` |
| `/estampa-textil` | `escritorio-projetos/estampa_textil.md` |
| `/google-slides-template` | `marketing/producao/google_slides_template.md` |
| `/revisao-arte-impressao` | `marketing/revisao/revisao_arte_impressao.md` |
| `/adaptar-arte` | (skill inline) |
| `/motion-projeto` | (skill inline) |
| `/vetorizar` | `marketing/producao/vetorizar_imagem.md` |
| `/video-analysis` | `escritorio-projetos/analise_edicao_video.md` |
| `/editar-negocio-cultural` | (skill inline — WP/TutorLMS) |
| `/editar-linkedin` | (skill inline — Voyager API) |
| `/postar-linkedin` | (skill inline — Playwright) |
| `/editar-site-web` | (skill inline — Playwright+CDP) |
| `/salvar` | SecondBrain vault |
| `/verificar` | gate de sucesso |
| `/debug` | investigação 4-fases |
| `/design-briefing` | gate antes de gerar imagem |
