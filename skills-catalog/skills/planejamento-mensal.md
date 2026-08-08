---
name: planejamento-mensal
description: Gera o dashboard HTML interativo de planejamento mensal do Escritório de Projetos da NTICS, com dados ao vivo do ClickUp. Produz um painel de abas (Gantt anual, visões do mês por coordenador / projeto / áreas transversais, calendário de execução em campo, e detalhado por semanas), mais um bloco de alertas e um checklist de pendências. Acione SEMPRE que o usuário disser "planejamento mensal", "planejamento do mês", "dashboard do mês", "monta o planejamento de [mês]", "atualiza o planejamento", "como está o mês", "visão do mês", "gera o painel mensal", ou qualquer variação de consolidação mensal do portfólio para tomada de decisão. Esta skill substitui a produção manual do dashboard, com objetivo de gerar em menos de 20 minutos o que antes levava horas. Use-a proativamente sempre que o contexto envolver o planejamento do mês inteiro ou a reunião mensal de portfólio. NÃO confundir com a skill norteador-semana (o infográfico semanal da reunião Hands On); esta é o planejamento do mês completo.
---

# Planejamento Mensal — NTICS Escritório de Projetos

Gera o dashboard mensal de planejamento a partir de dados ao vivo do ClickUp. O painel é a SAÍDA; a lógica e os dados moram aqui, nunca no HTML.

> ✅ **Template real, extraído do dashboard vivo (19/07/2026).** O `template.html` na raiz desta
> skill foi gerado a partir do `index.html` que o PMO roda de verdade (o de `arte3-star/claude-ntics-projetos/dashboards/pmo/`),
> separando dados da casca por contagem de chaves e **verificado byte-a-byte** (reinjetar os dados
> reproduz o original exato). Ele tem **8 marcadores** `/*__NTICS_INJECT:NOME__*/`, um por
> constante de dado. O exemplo real do mês está em `references/dados-julho-2026.js`.
> As constantes de dado são: `PROJECTS`, `PROJ_MES`, `SEMANAS_DATA`, `AREAS`, `CAL_CAMPO`,
> `ROTINAS_AREA`, `HANDSON_WEEKS`, `DEFAULT_WEEK_OVERRIDES`. Config estável (fica na casca, NÃO
> injetar): `IMGS`, `PHASE`, `COORD_NAMES`, `COORD_ORDER`, `TRANSVERSAL`, `PC`, `WK_DEFS`,
> `PHASE_DURATION`, `JUN`.
> O `references/exemplo-dados-junho.js` e a nomenclatura antiga (`CAL_EVENTS`/`AREAS_LIVE`/`PROJ_C`,
> marcador único `/*__NTICS_DATA_BLOCK__*/`) foram **descontinuados** — vieram de uma versão de
> nuvem que nunca rodou aqui. A lógica de extração do ClickUp em `references/extracao-clickup.md`
> segue válida (só reconcilie os nomes de constante com os reais acima).

## Princípio inegociável (lição cara)

O dashboard antigo era costurado à mão, com dados escritos dentro do código. Toda atualização exigia trabalho artesanal, e isso consumia horas. **Esta skill existe para inverter isso:** a skill contém a lógica de extração e o template; os dados entram por injeção a cada execução. Nunca escrever dado direto no template. Nunca dizer que algo é "ao vivo" se foi montado à mão.

## REGRA DE OURO DO VISUAL (não recriar, COPIAR)

O visual aprovado está CONGELADO no arquivo `template.html` (na raiz desta skill). É o design validado tela a tela com o Abilio (header verde, cards de coordenador com fotos, grade de 6 colunas do Detalhado por Semanas, calendário colorido por projeto com fotos, cards de área).

**NUNCA reconstruir o HTML/CSS do zero a partir de descrição.** Isso já foi tentado e o resultado fugiu do design aprovado (perdeu as fotos, a grade de 6 colunas virou grade simples, etc.). O jeito certo é:

1. Ler `template.html` como está (a casca: CSS, funções `build*`, config estável, e os 8 marcadores).
2. Gerar APENAS as 8 constantes de dado a partir do ClickUp (mesma forma de `references/dados-julho-2026.js`).
3. Para cada constante, substituir o marcador `/*__NTICS_INJECT:NOME__*/` pela declaração real `const NOME = <valor>;`.
4. Salvar como HTML final e entregar. NÃO sobra nenhum `__NTICS_INJECT__` no arquivo.

**As 8 constantes de dado (o que cada uma alimenta):**

| Constante | Alimenta | Origem no ClickUp |
|---|---|---|
| `PROJECTS` | Gantt anual (projeto × 12 meses × fase) | Fase por projeto ao longo do ano |
| `PROJ_MES` | Visões Por Projeto / Por Coordenador (fase do mês) | Projetos do mês-alvo + fase |
| `SEMANAS_DATA` | Detalhado por Semanas (gestão, coord × semana) | Tarefas-mãe de gestão, distribuídas por semana |
| `AREAS` | Cards de Áreas transversais | Campo ÁREAS/SETORES + Financeiro/Compras |
| `CAL_CAMPO` | Calendário de execução em campo | Tarefas com etiqueta `📍execução` |
| `ROTINAS_AREA` | Rotinas recorrentes por semana | Rotinas fixas (dia 05, 20 etc.) |
| `HANDSON_WEEKS` | Estrutura das semanas do mês | Semanas seg→dom do mês |
| `DEFAULT_WEEK_OVERRIDES` | Seed/baseline por `projeto\|mês\|bloco` | Ajustes manuais congelados na reunião |

Gerar com a MESMA forma de `references/dados-julho-2026.js`, só trocando o conteúdo pelos dados do mês pedido. NÃO mexer no CSS, nas funções `build*`, na config estável, nem na estrutura HTML do template.

## O que esta skill produz

Um arquivo HTML único com abas:
1. **Gantt anual** — visão dos 12 meses (estrutura relativamente estável, validada com o usuário antes de mudar).
2. **Visões do mês** (sub-abas):
   - Por Coordenador
   - Por Projeto
   - Por Áreas transversais (cards)
   - Detalhado por Semanas (trabalho de gestão, semana a semana)
3. **Calendário de execução em campo** (colorido por projeto, com etiquetas).
4. **Bloco de alertas** (topo) + **checklist de pendências** (rodapé).

Detalhes de cada aba e do template visual: ver `references/template-visual.md`.
Lógica de extração detalhada (queries, filtros, classificação): ver `references/extracao-clickup.md`.

## REGRAS DE PROCESSO NTICS (não violar — não são erro, é como a empresa opera)

Estas regras vêm de aprendizado direto com o Abilio. Tratá-las como problema gera ruído e desconfiança no painel.

### R1 — Projeto pré-abertura: tarefas sem data e sem responsável são INTENCIONAIS
Enquanto o projeto não é ABERTO (conclusão da 1a etapa: Mockup + Planejamento + Termo de Abertura), tarefas-mãe e subtarefas ficam propositalmente sem data e sem responsável. É na abertura que se define cronograma, equipe e tarefas. Antes disso, só o COORDENADOR do projeto é conhecido.
- NUNCA sinalizar essas tarefas como "órfãs", "atrasadas" ou "problema de saneamento".
- Distinguir projeto pré-abertura de projeto aberto. Em projeto pré-abertura, a ausência de alocação é o estado esperado.

### R2 — Etiquetas de campo são camadas independentes; ausência é informação
- `📍execução` = projeto sendo realizado naquele local.
- `captação em campo` = há captação fotográfica/vídeo naquela ação (nem toda ação tem).
- `nticsemcampo` = há pessoa da NTICS acompanhando presencialmente (nem toda ação tem).
A ausência de `captação em campo` ou `nticsemcampo` NÃO é falta de preenchimento: é o fato real. O Calendário mostra o que existe, nunca cobra o que não existe.

### R3 — Marcos KI e KC são TAGS, não nomes de tarefa
- Tag `ki - kick off interno` = alinhamento interno NTICS.
- Tag `kc - kick off cliente` = abertura oficial com cliente.
Rastrear marcos SEMPRE por essas tags (nomes exatos, minúsculas), nunca por texto no nome da tarefa.
- Quando a tag não existe no projeto: o kickoff ainda não foi agendado. Vira item de CHECK ("a agendar") com observação, NÃO erro.
- A fase de Kick-off engloba a fase Mockup/Termo de Abertura.

### R4 — Coordenadores conhecidos (confirmado jun/2026; reconfirmar a cada ciclo)
- #122 (Cultura Itinerante ODS / Repsol) = Bellmond
- #128 (Festival Agricultura Sustentável / CNH) = Lucas
- #129 (Agrofuturo Cultural nas Escolas / CNH) = Lucas
Antes da abertura, o coordenador é a única alocação definida.

## FLUXO DE EXECUÇÃO (passo a passo)

Execute em ordem. Pare e reporte se estourar o teto de chamadas (ver Limites).

1. **Parâmetros.** Receber mês e ano alvo (default: mês corrente). Calcular a janela: atrasadas (mês anterior em aberto) + mês alvo + primeira semana do mês seguinte (vira a coluna "O que vem aí", prévia, não execução).

2. **Varredura ampla das tarefas-mãe.** Uma chamada `filter_tasks` com `folder_ids:["<ID_CLICKUP>"]` (folder Projetos Ativos), janela calculada, `subtasks:false`, `include_closed:false`. Paginar com `page` se passar de 100 resultados. ATENÇÃO: usar `folder_ids`, NÃO `space_ids`. Buscar pelo space traz lixo que não é projeto (Sprints, Cronograma de redes sociais, listas Modelo de Projeto). Confirmado em teste: o space inclui essas listas; o folder não. Se ainda assim aparecer alguma lista de modelo/template/sprint/redes, descartá-la no processamento.

3. **Calendário (tags de campo).** Chamadas `filter_tasks` por tag de campo (`📍execução`) no mesmo space e janela, `subtasks:true`, `include_closed:true`. Ler as 3 etiquetas de cada tarefa como camadas (R2). Tratar eventos multi-dia: se a tarefa tem `start_date` e `due_date` diferentes, o evento aparece em todos os dias do intervalo.

4. **Marcos KI/KC.** Uma chamada `filter_tasks` com `tags:["ki - kick off interno","kc - kick off cliente"]` no space, sem filtro de data (marcos podem estar fora da janela). Cruzar com a agenda se o Google Calendar estiver disponível (ver passo 7). Projeto sem a tag = kickoff a agendar (R3).

5. **Detalhado por Semanas (gestão).** Das tarefas-mãe da varredura ampla, excluir: marcadores `📌 FASE:`, rotinas `👤`, redes sociais, e toda tarefa-mãe com `📍execução` na mãe ou em qualquer subtarefa (campo vive no Calendário). O que sobra é gestão. Para essas, `get_task` seletivo (teto ~15) para ler subtarefas não-concluídas (máx 4 + "+N"). Distribuir por semana pelo due_date; tarefa-mãe repete nas semanas onde há subtarefa caindo.

6. **Áreas transversais.** Ler as áreas pelo campo ÁREAS/SETORES (ver `references/extracao-clickup.md` para o critério e a pendência de saneamento). Financeiro (lista `<ID_CLICKUP>`) e Compras (lista `<ID_CLICKUP>`) são leituras separadas. Auditoria e Criação de Projetos (Mayara) saem do space de projetos.

7. **Cruzamento com agenda (se Google Calendar disponível).** Para cada KI/KC, verificar se há evento correspondente na agenda do período. Com evento = "agendado" (verde). Sem evento = "a agendar" (amarelo). Se o conector não estiver ativo, marcar como "verificar agenda" e seguir.

8. **Montar o HTML (COPIAR o template, não recriar).** Ler `template.html`. Gerar as 8 constantes de dado no formato de `references/dados-julho-2026.js`. Para cada uma, substituir seu marcador `/*__NTICS_INJECT:NOME__*/` pela declaração `const NOME = <valor>;`. NÃO tocar em CSS, funções, config estável ou estrutura. Ver "REGRA DE OURO DO VISUAL".

9. **Validar o RENDER, não só a sintaxe.** Conferir que: (a) as 8 constantes foram injetadas (PROJECTS, PROJ_MES, SEMANAS_DATA, AREAS, CAL_CAMPO, ROTINAS_AREA, HANDSON_WEEKS, DEFAULT_WEEK_OVERRIDES); (b) NÃO sobrou nenhum `/*__NTICS_INJECT:` no arquivo final; (c) a sintaxe JS fecha (`node --check` com stub de document/window); (d) abrir o HTML e conferir que nenhuma aba está vazia. Ver `references/extracao-clickup.md` seção "Armadilhas de código".

10. **Entregar** o dashboard + bloco de alertas + checklist de pendências (kickoffs a agendar, decisões P0 conhecidas).

## LIMITES E RANGE DE ACESSO

- **Escopo de leitura:** folder Projetos Ativos (`<ID_CLICKUP>`) via `folder_ids` (NÃO `space_ids`, que traz lixo). Mais duas listas transversais: Tático Financeiro (`<ID_CLICKUP>`) e Gestão Compras (`<ID_CLICKUP>`). Nada além disso.
- **Listas a excluir sempre** (se aparecerem): qualquer "Sprint", "Cronograma de redes sociais NTICS" (`<ID_CLICKUP>`), e "Modelo de Projeto" / template (`<ID_CLICKUP>` e similares). Não são projetos reais.
- **Janela temporal estrita:** atrasadas + mês alvo + 1a semana do mês seguinte. PROIBIDO puxar lista inteira sem filtro de data (estoura contexto).
- **Varredura ampla sempre com `subtasks:false`.** `subtasks:true` apenas nas chamadas de Calendário e nos `get_task` seletivos de gestão.
- **Teto de chamadas ao ClickUp: ~25.** Estimativa por execução: 1 varredura ampla + 1-2 tags de campo + 1 KI/KC + ~15 get_task seletivos + 2 listas transversais + 1 agenda. Se ultrapassar, PARAR e sugerir estreitar a janela, em vez de continuar cego.
- **Meta de tempo:** abaixo de 20 minutos.

## RASTREIO DE TAGS (resumo)

| Tag | Função | Onde reflete |
|-----|--------|--------------|
| `📍execução` | ação em campo naquele local | Calendário (exclui de Semanas) |
| `captação em campo` | há captação foto/vídeo | badge no Calendário |
| `nticsemcampo` | pessoa NTICS presente | badge "NTICS em Campo" no Calendário |
| `ki - kick off interno` | marco kickoff interno | Calendário + Semanas + check agenda |
| `kc - kick off cliente` | marco kickoff cliente | Calendário + Semanas + check agenda |
| `claude` | tarefa criada por automação | rastreio interno |

Nota: NÃO existe mais a tag `❗crítico` no Calendário. Crítico é marcação de gestão; se aparecer, fica em Semanas, nunca no Calendário.

## PRIORIDADES

- `urgent` → badge vermelho URGENTE. `high` → badge laranja ALTA.
- Urgente + vencida (em projeto ABERTO) → entra no bloco de alertas do topo.
- Atenção: urgente/vencida em projeto pré-abertura pode cair na regra R1; não alarmar.

## IDs DE REFERÊNCIA

Mapa completo de listas-projeto, coordenadores, campo ÁREAS/SETORES e valores: ver `references/extracao-clickup.md`.

## DÍVIDA TÉCNICA CONHECIDA

O campo ÁREAS/SETORES não está saneado em todas as tarefas (ex: tarefa de pós-projeto da Mayara marcada como Produção&PMO em vez de Criação). Enquanto não saneado, usar o fallback de classificação descrito em `references/extracao-clickup.md`, e sempre incluir no checklist final um lembrete para sanear na raiz.
