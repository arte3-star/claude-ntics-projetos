---
name: sheets-app
description: "Cria uma camada visual interativa (estilo Artefato/app low-code) que roda ACOPLADA dentro de uma planilha do Google Sheets, eliminando a necessidade de ler linhas brutas. Combina back-end em Google Apps Script (Codigo.js) com front-end Tailwind (Interface.html) num projeto clasp pronto para deploy por CLI. Duas vias: carrega colunas de qualquer aba dinamicamente, filtra, seleciona linhas por checkbox e faz edições em massa (bulk update) que gravam de volta via setValues(). Use SEMPRE que o usuário quiser um app/painel/interface/dashboard editável dentro de uma planilha Google, um menu ⚡ na planilha, editar linhas em massa por uma tela em vez de célula a célula, ou mencionar Apps Script, clasp, HtmlService, sidebar/modal na planilha, low-code sobre Sheets — mesmo sem dizer 'app' explicitamente."
user-invocable: true
---

# Sheets App — app low-code acoplado ao Google Sheets

Gera um "app" que vive **dentro** de uma planilha Google: o usuário abre por um menu
personalizado (⚡ Painel) e ganha uma tela para filtrar, selecionar e editar dados em
massa — sem varrer linhas brutas. O código sai pronto para subir com **clasp**.

## Quando usar

- "Quero um painel/app/interface dentro da minha planilha para editar sem rolar mil linhas"
- "Um menu na planilha que abre uma tela para marcar linhas e mudar o status de várias de uma vez"
- "Dashboard editável / CRUD sobre a aba X", "sidebar na planilha", "modal com os dados"
- Qualquer menção a **Apps Script + HTML**, **clasp**, **HtmlService**, **onOpen**, **setValues** com fim de interface.

## Arquitetura (não fuja dela)

Sempre back-end Apps Script + front-end Tailwind encapsulado, sincronizados por `google.script.run`:

| Camada | Arquivo | Papel |
|---|---|---|
| Back-end | `Codigo.js` | `onOpen` (menu), `getSheetNames`, `getSheetData(aba)`, `bulkUpdate(aba, updates)` |
| Front-end | `Interface.html` | Tailwind (CDN) + tabela + checkboxes + filtro + paginação + modal de edição em massa |
| Manifesto | `appsscript.json` | timezone, runtime V8 |
| Deploy | `.clasp.json` | vincula ao scriptId da planilha |

**Duas vias obrigatórias:** a interface não é estática. Ela (1) lê as colunas de qualquer aba
ativa dinamicamente e (2) grava de volta. A gravação usa o padrão otimizado: agrupa as edições
por coluna e faz **1 leitura + 1 `setValues()` por coluna** — nunca `setValue` célula a célula
(estoura cota e trava a planilha). Cada linha carrega `_row` (nº real na planilha) para gravar no lugar certo.

**Padrão visual esperado:** cabeçalho com ações rápidas + seletor de aba, alerta visual de
feedback, tabela limpa com paginação/scroll, e o app abre por `onOpen` → **sidebar** (fixa) ou
**modal** (janela grande). É exatamente o que o template já entrega.

## Workflow

1. **Entenda o caso.** Pergunte (ou infira do contexto) só o essencial:
   - Título do app e do menu (ex.: "Painel de Inscrições" / "⚡ Painel").
   - Se é planilha **nova** ou **existente** (muda o passo de deploy — ver `assets/template/DEPLOY.md`).
   - Alguma regra de negócio além do CRUD genérico? (coluna travada, valores fixos num campo,
     confirmação antes de gravar). O template já cobre ler/filtrar/selecionar/editar em massa
     de **qualquer** aba sem hard-code de colunas — só personalize se pedirem.

2. **Copie o template.** Ele é a base testada. Copie `assets/template/` para a pasta de trabalho
   do usuário (ou `tmp/sheets-app-<slug>/` se não houver destino claro). Nunca reescreva do zero.

3. **Adapte o mínimo.** Em `Codigo.js` ajuste `APP_TITLE` e `MENU_TITLE`. Em `Interface.html`
   troque o texto do cabeçalho ("Painel de Dados") pelo título do caso. Se pediram regra específica,
   adicione — mas mantenha a leitura de colunas **dinâmica** (nunca fixe nomes de coluna no código).

4. **Valide no navegador antes de publicar.** `Interface.html` tem um bloco `MOCK` no rodapé que
   simula o back-end quando `google.script.run` não existe. Abra num preview local para conferir
   layout, filtro, seleção, edição inline (célula fica amarela) e o modal de edição em massa.
   Ajuste o que estiver torto antes de falar em deploy.

5. **Deploy por clasp.** Siga `assets/template/DEPLOY.md` (Opção A = planilha nova via
   `clasp create --type sheets`; Opção B = planilha existente colando o scriptId em `.clasp.json`,
   depois `clasp push`). Entregue ao usuário o caminho da pasta + os comandos exatos.

## O que o template já resolve (não reimplemente)

- Seletor de aba populado por `getSheetNames()` e leitura dinâmica via `getSheetData()`.
- Filtro de texto, paginação (25/pág), select-all da página, contadores de seleção/pendências.
- Edição inline por célula (`contenteditable`) acumulando "pendências" (destaque amarelo) + botão
  **Salvar alterações** que grava tudo de uma vez.
- **Editar selecionados**: modal para setar uma coluna com um valor em N linhas marcadas.
- Alertas de sucesso/erro/info, overlay de carregamento, escape de HTML, menu sidebar + modal.

## Regras

- **Mantenha as duas vias.** Se o pedido for só leitura, ok, mas confirme — o valor da skill está em gravar de volta com segurança.
- **Nada de hard-code de colunas** no fluxo genérico: o app deve servir qualquer aba.
- **Sempre valide no preview local** antes de instruir o deploy (o `MOCK` existe para isso).
- **Não feche o navegador** do usuário durante preview/automação.
- Ao entregar, dê o **caminho da pasta** e os comandos clasp prontos para copiar.

## Referência

- `assets/template/` — projeto clasp completo (copiar e adaptar): `Codigo.js`, `Interface.html`, `appsscript.json`, `.clasp.json.example`.
- `assets/template/DEPLOY.md` — passo a passo do clasp (planilha nova vs. existente) e preview local.
