# Fontes no ClickUp — onde os dados vivem e como descobri-los

Nada de IDs fixos: **descubra em runtime**, porque os nomes podem mudar. Sempre reporte ao usuário o
que casou, para ele corrigir se necessário.

## Estrutura esperada

- **Space/Pasta:** "Escritório de Projetos".
- **Agrupamento:** "Projetos Ativos" (pasta ou conjunto de listas), uma **lista por projeto**.
- **Listas de redes sociais** (transversais):
  - "Kanban de redes sociais" — carrosséis institucionais (tag **institucional**): notícias ESG,
    projetos e notícia de projetos.
  - "Cronograma de redes sociais NTICS" — calendário geral de posts (usado nos relatórios anteriores).

## Descoberta

1. `clickup_get_workspace_hierarchy` → percorra spaces/folders/lists.
2. Case-insensitive + acento-insensível, ache:
   - pasta cujo nome contenha "escrit" + "projeto";
   - dentro dela, o grupo "projetos ativos" e as listas de projeto;
   - listas cujo nome contenha "redes sociais" (kanban e/ou cronograma).
3. Se algo não casar, **liste os candidatos** e pergunte ao usuário qual usar. Não adivinhe silenciosamente.

## Tarefas de interesse

Por lista de projeto ativo:
- Tarefa-pai: nome contém "acompanhar redes sociais".
- Subtarefas (via `clickup_get_task` com `subtasks=true`): nomes com "postar carrossel",
  "postar vídeo", "postar video", "criar vídeo", "editar vídeo", "edição de vídeo".

Transversais:
- Na lista de redes sociais, itens com a tag **institucional** (carrosséis ESG / projetos / notícia).

Ferramentas úteis: `clickup_filter_tasks` (por lista, status, datas, tags, assignees),
`clickup_search` (busca por texto no nome), `clickup_get_task` (detalhe + subtarefas),
`clickup_get_task_comments` (contexto/quando precisar entender status).

## Campos a capturar por tarefa

- **tipo:** carrossel | vídeo (post) | edição (produção de vídeo) — inferir do nome.
- **projeto:** a lista de origem.
- **status:** mapear os status do ClickUp em `concluído` | `planejado` | `backlog`.
- **data (due date):** para alocar no período e no calendário.
- **responsável(is):** resolver via `clickup_resolve_assignees` / `clickup_find_member_by_name`.
- **tags:** guardar todas; sinalizar em especial **"data fechada com cliente"** e **"institucional"**.

## Pessoas (papéis)

- **Aline** — postagens; também edita alguns vídeos (é quem fará os cortes propostos).
- **Marcos** — edição de vídeo (vídeo *case* final, maior).
- **Designers** — Marina, Alison e uma terceira pessoa (descobrir dinamicamente a partir dos
  responsáveis das tarefas de design/edição; não hard-code).

## Fase de finalização

Alguns projetos estão "em finalização": o evento já aconteceu e resta só o vídeo final. Detecte por
status/tag/nome que indiquem finalização/encerramento. Nesses projetos há material de sobra → é onde
cabem os **cortes / melhores momentos** adicionais editados pela Aline (ver `analise-e-proposta.md`).
