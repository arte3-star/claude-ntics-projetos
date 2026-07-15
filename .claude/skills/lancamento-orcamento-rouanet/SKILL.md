---
name: lancamento-orcamento-rouanet
description: Guia o novo lançamento da aba de orçamento de um PRONAC na planilha de prestação de contas Rouanet (Google Sheets), a partir do PDF do orçamento aprovado (SALIC). A pessoa cuida da estrutura (3 passos manuais) e o Claude na barra lateral do Chrome preenche os dados. Use quando o usuário pedir "novo lançamento de orçamento", "lançar orçamento Rouanet", "preencher aba de orçamento", "orçamento SALIC/PRONAC" ou similar.
---

# Novo Lançamento de Orçamento (Planilha Rouanet)

Fluxo para criar e preencher a aba de orçamento de um novo PRONAC a partir do PDF do
orçamento aprovado (SALIC).

**Regra de ouro:** a **pessoa cuida da estrutura** (3 passos rápidos e seguros) e o **Claude
preenche os dados**. Assim ninguém erra a formatação e o preenchimento sai em segundos.

> ⚠️ Onde este fluxo roda: o preenchimento em si acontece com o **Claude na barra lateral do
> Google Chrome**, com a planilha do Google Sheets e o PDF do SALIC abertos. Fora desse ambiente
> (ex.: dentro do repositório, sem acesso à planilha), esta skill serve para **preparar e entregar
> o prompt canônico e conduzir a conferência** — não para editar a planilha diretamente.

## Passo 0 — Pré-requisitos (deixe aberto)

1. A **planilha** de prestação de contas aberta no Chrome, logada na conta certa.
2. O **PDF do orçamento aprovado** (SALIC) — em outra aba do Chrome (o Claude consegue ler) ou à
   mão para anexar na barra lateral.
3. A **barra lateral do Claude** aberta no Chrome.

Onde achar os dados no PDF:
- **PRONAC e nome do projeto:** topo da 1ª página — ex.: `PRONAC: 2512916 - PROGRAMA NEGÓCIO
  CULTURAL - 3ª EDIÇÃO`.
- **Total para conferência:** última página, linha **"Total do Projeto"**, coluna **VL. APROVADO**.

## Passo 1 — Parte manual (a pessoa faz — 3 passos, ~1 minuto)

Oriente o usuário a fazer, nesta ordem:

1. **Duplicar o MODELO** — no rodapé, botão direito na aba **"MODELO" → Duplicar**. Surge
   "Cópia de MODELO".
2. **Renomear a aba** — botão direito na aba nova → **Renomear** → padrão `PRONAC_NOME DO PROJETO`
   → Enter. Ex.: `2512916_PROGRAMA NEGÓCIO CULTURAL - 3ª EDIÇÃO`.
   > ⚠️ Use **botão direito → Renomear**. Evite o duplo-clique (pode pular para a aba errada).
3. **Ajustar o título (célula A1)** — clique em **A1** → padrão `Orçamento_NOME DO PROJETO_PRONAC`
   → Enter. Ex.: `Orçamento_PROGRAMA NEGÓCIO CULTURAL - 3ª EDIÇÃO_2512916`.

> O padrão do **nome da aba** e do **título A1** são diferentes: a aba **começa** com o PRONAC; o A1
> **termina** com o PRONAC. Copie os dois exatamente como nos exemplos.

## Passo 2 — Entregar o prompt de preenchimento

Com a **aba nova em foco** e o **PDF disponível**, o usuário cola na barra lateral do Claude o
prompt canônico. Entregue-o **verbatim** (bloco pronto para copiar) — ele está em
`references/prompt-preenchimento.md`. Se o usuário quiser, personalize apenas o nome/PRONAC do
projeto; o corpo das regras não muda.

As regras de leitura do PDF e a estrutura da aba (blocos de 5 linhas, colunas a preencher, fórmulas)
estão em `references/estrutura-e-colunas.md` — consulte se precisar explicar ou ajustar algo.

## Passo 3 — Conduzir para sair sem erro

- **Valide por blocos, não tudo de uma vez.** Quando o Claude mostrar a primeira etapa/cidade,
  confira 1 ou 2 itens contra o PDF antes de mandar continuar.
- **Olhe o SALDO do primeiro item:** sem pagamentos lançados, ele deve nascer **igual ao total**
  daquele item. Se nascer diferente, pare.
- **No fim, confira o TOTAL GERAL** contra o "Total do Projeto" (VL. APROVADO) do PDF — tem que ser
  **idêntico**.
- **Se algo sair torto,** a aba é descartável: botão direito → Excluir e recomece do Passo 1. Não
  afeta as outras abas.

## Passo 4 — Checklist de conferência final

Rode o checklist completo de `references/conferencia-e-erros.md`. Os pontos críticos:

- [ ] Nome da aba no padrão `PRONAC_NOME` e título A1 no padrão `Orçamento_NOME_PRONAC`.
- [ ] Todos os itens com **VL. APROVADO > 0** lançados (glosados a R$0 ficam de fora).
- [ ] Coluna I das linhas laranja é **fórmula** `=F*G*H`.
- [ ] Linhas verdes e SALDO **sem valores digitados** (só as fórmulas do modelo).
- [ ] Linha **TOTAL GERAL** criada, com R$ e realce.
- [ ] **TOTAL GERAL = "Total do Projeto" (VL. APROVADO) do PDF** — idênticos.

A tabela de **erros comuns e solução** também está em `references/conferencia-e-erros.md`.
