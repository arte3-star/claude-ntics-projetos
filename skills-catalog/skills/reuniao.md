---
name: reuniao
description: |
  Processa uma reunião a partir da transcrição: classifica (INTERNAL/SALES/STRATEGIC),
  extrai as tasks com responsável e prazo, separa o que ficou em aberto, e cria as
  tarefas no ClickUp com os campos obrigatórios.

  Acione SEMPRE que o usuário disser: "processa a reunião", "gera as tasks da reunião",
  "lê a ata", "vira task o que ficou da reunião", "classifica essa reunião",
  "extrai as tarefas dessa transcrição", "o que saiu da sprint de X", "processa a sprint",
  "analisa essa transcrição", "cria as tasks dessa call", "resumo da reunião com o cliente",
  "passa a ata pro ClickUp", ou colar/apontar uma transcrição ou link de ata.

  Também acione quando o usuário mencionar reunião de sprint, kickoff, alinhamento,
  call com cliente/patrocinador, ata do Meet, ou anexar arquivo de transcrição.

  NÃO confundir com resumo-sprints (que consolida a semana inteira de várias sprints
  em subpágina do documento "Sprints"); esta skill processa UMA reunião.
---

# Processar reunião

Reunião é o trabalho de maior volume aqui. O gargalo histórico foi ler a transcrição
pela metade e virar sugestão em tarefa. Esta skill existe para evitar as duas coisas.

## Regras que não se negociam

1. **Ler a transcrição INTEIRA.** Nunca só o bloco "Observações" ou "Resumo" do Meet.
   O script não trunca mais; não recrie o truncamento passando trecho.
2. **Sugestão não é tarefa.** Pedido levantado e não resolvido vai para
   `open_questions`, nunca para o ClickUp como task. Só é task o que foi pactuado.
3. **Ler antes de escrever.** Antes de criar ou atualizar qualquer coisa no ClickUp,
   conferir o estado atual — o Lucas edita direto e não pode perder mudança.
4. **Revisar com o Lucas antes de criar as tasks.** Mostrar a lista extraída primeiro.

## Passo 1 — obter a transcrição completa

Fontes possíveis, em ordem de preferência:

- arquivo local passado pelo usuário → use `--file <caminho>`
- documento/página do ClickUp → puxe pelo MCP e grave em `tools/.tmp/transcript.txt`
- Google Drive → `download_file_content` (não `read_file_content`, que trunca em silêncio)
- texto colado na conversa → `--text`

Confirme o tamanho antes de seguir. Se vier suspeito de curto (< 5.000 chars para uma
reunião de uma hora), você provavelmente pegou só o resumo. Volte e busque a transcrição.

## Passo 2 — classificar e extrair

```bash
cd "G:/My Drive/Claude-NTICS-Projetos"
PYTHONUTF8=1 python tools/meetings/classify_meeting.py --name "<titulo da reuniao>" [--file <caminho>]
```

O script lê a chave do `.env` da raiz sozinho. Se der `APIConnectionError`, é o proxy
TLS local: repita com `NTICS_INSECURE_TLS=1` na frente do comando.

Saída: `tools/.tmp/meeting_result.json` com `meeting_type`, `confidence`, `project_number`,
`tasks[]` (cada uma com `context`, o trecho da transcrição que a originou), `open_questions[]`,
`pipedrive_summary` e `learning`.

Transcrição acima de 400 mil chars é processada em blocos com sobreposição e os
resultados são unidos; nada é descartado.

## Passo 3 — revisar antes de escrever

Apresente ao Lucas:

- tipo e confiança (`confidence < 80` já vem marcado com `triage: true`)
- projeto identificado
- a lista de tasks com responsável e prazo
- as pendências em aberto, separadas, explicitamente **não** viram task

Só siga depois do OK dele. Se a confiança vier baixa, diga isso em vez de seguir calado.

## Passo 4 — criar as tasks no ClickUp

Para cada task aprovada, ao criar na lista `Projetos Ativos`:

- **campos obrigatórios:** Fase, Fase PMBOK, Área/Setor
- **assignee:** o `assignee_id` do JSON (já resolvido pela prioridade nome → título da
  reunião → palavra-chave). Se vier `null`, pergunte, não chute.
- **etiqueta `claude`** sempre
- **datas:** `due_date` no formato `"YYYY-MM-DD HH:MM"`. Se estiver reduzindo um `due`
  existente, passe `start_date` junto — `due` menor que `start_date` é ignorado em silêncio.
- tarefa de captação em campo usa o prefixo `Captação em Campo ·`
- o `context` de cada task vai no corpo, como rastro de origem

Sem tabela Markdown no corpo: o ClickUp mostra os pipes como texto literal. Use blocos.

## Kick off com cliente tem passo extra

Se a reunião for kick off com cliente, o trabalho não termina nas tasks. Leia
`references/kickoff-cliente.md` e siga: as tarefas vão para a **lista do projeto** na fase
Kick-off, as pendências do cliente entram com status `aguardando (externo)`, e o **e-mail
pós kick off já vai escrito** dentro da tarefa de envio do e-mail. Escrever é seu; enviar
é do Lucas.

## Passo 5 — fechar o ciclo

- `open_questions` → registre onde o projeto guarda pendência (`itens-em-aberto.md`),
  não como task
- `learning` preenchido → vale uma memória nova ou `/projeto-salvar`
- `meeting_type == "SALES"` → `pipedrive_summary` é o resumo para o CRM

## Ruído de transcrição

O script já normaliza, mas você também deve reconhecer ao ler:
"Enitix", "Anityx", "NTX", "NTIX" = NTICS · "Cláudio" = Claude (nunca uma pessoa) ·
"Tapuã" = Porto Itapoá (projeto 120).
