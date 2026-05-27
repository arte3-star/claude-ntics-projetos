# Workflow — /projeto-sync-ta

> Atualiza o TAP (ClickUp Doc) de um projeto com as informações mais recentes do Drive, ClickUp e SecondBrain. Pode ser executado manualmente ou após processamento de reunião.

## Quando usar

- Após reunião com cliente (informações novas confirmadas)
- Após atualização de planilhas Google Sheets
- Após novo arquivo subido no Drive do projeto
- Periodicamente (revisão semanal de estado)
- Quando o usuário pedir "atualiza o TAP do projeto X"

## Inputs

- `codigo` — código do projeto (ex: 128)
- `slug` — slug do projeto (ex: `cnh-festival-agricultura`)
- `secao` — (opcional) seção específica a atualizar: `cronograma`, `engajamento`, `comunicacao`, `financeiro`, `stakeholders`. Se omitido, atualiza todas as seções vivas.

## Localização dos IDs

Os IDs do documento e das páginas ficam em:
```
SecondBrain/projetos/{codigo}-{slug}/state.yaml → tap_clickup_doc
```

## Seções e suas fontes

| Seção | Página | Fontes de dados |
|-------|--------|----------------|
| Identificação + Links | `identificacao_links` | Fixo — atualizar só se mudar PRONAC ou links |
| Escopo + Indicadores | `escopo_indicadores` | Fixo — atualizar só se mudar escopo contratual |
| Cronograma | `cronograma` | state.yaml (blockers, proxima_acao, historico_fases) + ClickUp (due dates das tasks) |
| Engajamento | `engajamento` | state.yaml (cidades, oficinas) + reuniões + Sheets de engajamento |
| Comunicação | `comunicacao` | state.yaml (deliverables_design, deliverables_conteudo) + ClickUp (status das tasks de comunicação) |
| Financeiro | `financeiro` | stakeholders.yaml (fornecedores) + ClickUp (tasks de contratos) + Sheets financeiro |
| Stakeholders | `stakeholders` | stakeholders.yaml + reuniões (novos contatos confirmados) |
| Encerramento | `encerramento` | Só preencher ao fechar o projeto |

## Passo a Passo

### Passo 1 — Carregar contexto do projeto

1. Ler `SecondBrain/projetos/{codigo}-{slug}/state.yaml`
2. Extrair `tap_clickup_doc.doc_id` e o mapa de `paginas`
3. Ler `SecondBrain/projetos/{codigo}-{slug}/stakeholders.yaml`
4. Ler `SecondBrain/projetos/{codigo}-{slug}/CLAUDE.md` (para contexto rápido)

### Passo 2 — Varrer fontes de dados

**Drive (arquivos novos desde a última atualização):**
- Usar `mcp__claude_ai_Google_Drive__list_recent_files` na pasta raiz do projeto
- Identificar: atas de reunião, contratos assinados, planilhas de engajamento atualizadas
- Para cada arquivo relevante: `mcp__claude_ai_Google_Drive__read_file_content`

**ClickUp (tasks e comentários recentes):**
- Usar `clickup_filter_tasks` na lista do projeto
- Filtrar tasks com status `done` ou `in progress` recentemente atualizadas
- Usar `clickup_get_task_comments` para tasks de decisão
- Identificar: contratos assinados, escolas confirmadas, datas firmes, novos stakeholders

**state.yaml e SecondBrain:**
- Verificar `blockers` (algum foi resolvido?)
- Verificar `proxima_acao` (mudou?)
- Verificar `historico_fases` (mudou de fase?)

### Passo 3 — Identificar o que mudou

Para cada seção viva, montar um diff do que precisa ser atualizado:

```
CRONOGRAMA:
  - Blocker TAP-FORMAL: ainda ativo / resolvido?
  - Data kickoff: confirmada? (estava pendente)
  - Novo marco identificado?

ENGAJAMENTO:
  - Nova escola confirmada?
  - Data de cidade confirmada?
  - Articulador local contratado?

FINANCEIRO:
  - Valor total confirmado?
  - Novo contrato assinado?
  - Pagamento realizado?

STAKEHOLDERS:
  - Interlocutor CNH confirmado?
  - Novo contato de fornecedor?
  - E-mails pendentes preenchidos?
```

### Passo 4 — Atualizar as páginas do TAP

Para cada seção com mudança:

1. Ler a página atual com `clickup_list_document_pages` + `clickup_get_document_pages`
2. Montar o conteúdo atualizado preservando a estrutura (tabelas, headers)
3. Atualizar com `clickup_update_document_page`
4. Sempre manter a linha `🔄 **Última atualização:**` ao final da página

**Regra crítica:** nunca sobrescrever informação existente que não foi confirmada como mudada. Se a fonte não confirma a mudança, manter o valor anterior.

### Passo 5 — Atualizar o state.yaml

Se houve mudança de fase ou blocker resolvido:
- Atualizar `fase` no state.yaml
- Mover blocker resolvido de `status: ativo` para `status: resolvido`
- Adicionar entrada em `historico_fases`

### Passo 6 — Registrar no execucao.md

Adicionar entrada em `SecondBrain/projetos/{codigo}-{slug}/execucao.md`:
```
## YYYY-MM-DD — Sync TAP
Seções atualizadas: [lista]
Fontes consultadas: [Drive / ClickUp / reunião]
Mudanças: [resumo em 2-3 linhas]
```

## Edge Cases

| Situação | Ação |
|----------|------|
| Nenhuma mudança identificada | Registrar "sem mudanças" no execucao.md. Não chamar update. |
| Conflito de informação (Drive diz X, ClickUp diz Y) | Perguntar ao usuário qual é a versão correta antes de atualizar |
| Seção fixa com mudança de escopo | Alertar usuário: "O escopo mudou — isso requer aprovação formal antes de atualizar o TAP" |
| Blocker resolvido parcialmente | Manter como ativo, atualizar a descrição para refletir o progresso |

## Integração com processamento de reuniões

Quando chamado após `/process-meeting-transcript` ou processamento de ata:
- O processador de reuniões passa um objeto `{informacoes_tap: {...}, tasks: [...]}` 
- `/projeto-sync-ta` usa `informacoes_tap` para atualizar as páginas relevantes
- Tasks são criadas separadamente via ClickUp MCP

## Exemplo de uso

```
/projeto-sync-ta 128 cnh-festival-agricultura
/projeto-sync-ta 128 cnh-festival-agricultura cronograma
/projeto-sync-ta 129 cnh-agrofuturo-escolas stakeholders
```
