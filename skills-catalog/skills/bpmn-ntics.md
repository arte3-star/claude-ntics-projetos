---
name: bpmn-ntics
description: >
  Converte os processos mapeados da NTICS em diagramas BPMN 2.0 visuais.
  Lê um descritivo BPMN-ready (processos/descritivos/<área>/<slug>.md, no repo
  ntics-nucleo), monta um spec JSON e gera <slug>.bpmn (abre no Camunda Modeler,
  draw.io, VS Code) + <slug>.svg (preview). Use quando o usuário pedir para
  "gerar BPMN", "desenhar o processo", "modelar em BPMN", "transformar o
  descritivo em diagrama" ou visualizar/exportar um ou vários processos NTICS.
---

# BPMN NTICS — descritivo → diagrama

Transforma os **214 descritivos BPMN-ready** da NTICS em BPMN 2.0 padrão de mercado,
sem depender de nenhum MCP externo. O formato de saída (`.bpmn`) é **universal**:
abre no [Camunda Modeler](https://camunda.com/download/modeler/) (grátis), draw.io,
Signavio, Bizagi e na extensão BPMN do VS Code — e de lá você exporta **SVG / PNG / PDF**.

## Divisão de trabalho (por que funciona)

- **Você (Claude)** faz a parte que o LLM faz bem: ler o descritivo `.md` (tabelas,
  raias, tipos) e produzir um **spec JSON** limpo e fiel.
- **`bpmn_from_spec.py`** faz a parte que o LLM faz mal: o **layout** — posicionar
  caixas, empilhar raias e rotear as setas (incluindo loops de gateway). É determinístico,
  então 1 ou 214 processos saem com o mesmo padrão visual.

**Nunca escreva as coordenadas do BPMN à mão.** Só produza o spec e rode o script.

## Fonte de entrada

Descritivos canônicos em `ntics-nucleo/processos/descritivos/<área>/<slug>.md`
(template em `_template-descritivo-bpmn.md`). As 7 áreas:
`comercial-vendas`, `comunicacao-cs`, `financeiro-compras`, `gente-juridico`,
`gestao-lab`, `inscricao-criacao`, `producao-escritorio`.

Cada descritivo já traz: **Raias**, **Etapas (sequência BPMN)** com `Tipo`+`Raia`,
**Gateways (decisões)**, **Eventos de início/fim** e **Conexões**. É tudo que o spec precisa.

## Passo a passo

1. **Leia o descritivo** alvo por inteiro.
2. **Monte o spec JSON** (schema abaixo):
   - Uma entrada em `lanes` por raia da seção *Raias* — na ordem de cima para baixo em
     que fizer sentido no fluxo (agrupe quem interage). Inclua raias de **sistema**
     (ClickUp, Claude, Drive) quando aparecerem como executoras.
   - Um nó por linha da tabela *Etapas*, **na ordem**. Traduza a coluna `Tipo`:

     | `Tipo` no descritivo | `type` no spec        | BPMN                 |
     |----------------------|-----------------------|----------------------|
     | tarefa               | `task`                | Task                 |
     | tarefa-usuario       | `userTask`            | User Task            |
     | tarefa-sistema       | `serviceTask`         | Service Task         |
     | decisão              | `exclusiveGateway`    | Gateway exclusivo (×)|
     | espera               | `intermediateCatchEvent` | Evento intermediário |
     | subprocesso          | `callActivity`        | Call Activity        |

     Gateways paralelos/inclusivos (quando o texto indicar "e/ou simultâneo"):
     `parallelGateway` / `inclusiveGateway`.
   - Adicione **um `startEvent`** (a partir do *Evento de início*) e **um ou mais
     `endEvent`** (da seção *Eventos de fim*).
   - **Flows:** ligue os nós na ordem. Para cada linha da tabela *Gateways*, crie o nó
     `exclusiveGateway` e **dois flows** saindo dele, com `name` = a condição
     ("sim"/"não", ou o rótulo curto). O ramo "não" que reprocessa **volta** para o nó
     anterior (loop) — é permitido e o script roteia por baixo.
3. **Rode o gerador:**
   ```bash
   python .claude/skills/bpmn-ntics/bpmn_from_spec.py <spec.json> --out-dir bpmn-out
   ```
   Sai `bpmn-out/<id>.bpmn` + `bpmn-out/<id>.svg`.
4. **Mostre o resultado** ao usuário (o `.svg` como imagem) e diga que o `.bpmn` abre no
   Camunda Modeler para editar/exportar. Se ele validar, escale para mais processos.

Em lote (uma área inteira): gere vários specs numa pasta e rode
`python .../bpmn_from_spec.py pasta_de_specs/ --out-dir bpmn-out`.

## Schema do spec

```json
{
  "process": "Nome legível do processo",     // vira o nome do Pool
  "id": "slug-do-processo",                   // vira o nome dos arquivos
  "area": "producao-escritorio",
  "lanes": ["Raia 1", "Raia 2", "..."],       // ordem = de cima p/ baixo
  "nodes": [
    { "id": "start", "type": "startEvent", "name": "...", "lane": "Raia 1" },
    { "id": "t1",    "type": "userTask",   "name": "...", "lane": "Raia 2" },
    { "id": "g1",    "type": "exclusiveGateway", "name": "Aprovado?", "lane": "Raia 2" },
    { "id": "end",   "type": "endEvent",   "name": "...", "lane": "Raia 2" }
  ],
  "flows": [
    { "from": "start", "to": "t1" },
    { "from": "t1",    "to": "g1" },
    { "from": "g1",    "to": "end", "name": "sim" },
    { "from": "g1",    "to": "t1",  "name": "não" }
  ]
}
```

Regras: todo `id` é único; todo `lane` tem de existir em `lanes`; `flows` só referenciam
`id`s de `nodes`. Nós já vêm em ordem de sequência (o script usa isso para o layout).

## Convenções NTICS

- **1 arquivo por processo**, nome = o `slug` do descritivo (ex.: `abertura-de-projeto-tap.bpmn`).
- **Fidelidade > invenção.** Só modele o que está no descritivo. O que a fonte não
  confirma (seção *Pendências*) **não vira** caixa — no máximo um comentário para o usuário.
- **Raias de sistema** entram como lanes normais (ClickUp, Claude, Drive, GPT).
- Saída padrão em `bpmn-out/` na raiz do worktree (ou onde o usuário pedir).
- Preserve os nomes/papéis como no descritivo (inclusive "PMO (a estruturar)").

## Exemplo de referência

`examples/abertura-de-projeto-tap.json` → o processo real *Abertura de Projeto → TAP*
(5 raias, 2 gateways com loop de reprovação). Rode-o para ver o padrão de saída.

## Alternativa: edição visual ao vivo (opcional)

Para iterar arrastando caixas com IA dentro do editor, existe o MCP
[Camunda Desktop Modeler plugin](https://lobehub.com/mcp/jesseleresche-camunda-mcp)
(19 tools, exige o Modeler aberto). Esta skill **não** depende dele — ela é offline,
determinística e portátil. Use o MCP só se quiser co-edição visual depois de gerar a base.
