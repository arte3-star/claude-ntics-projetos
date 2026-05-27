# Formalização de Fornecedores

> Gera emails de formalização de contratação no padrão NTICS e salva como draft no Gmail, a partir das linhas do Budget + dados do fornecedor.

---

## Quando usar

Sempre que um item do Budget passar para status **ORÇADO** e precisar ser enviado para Compras/Financeiro. Um email por fornecedor (uma linha do budget = um email).

Não usar para reembolsos internos (ver `diretriz_reembolso.md`).

---

## Fontes de referência (carregar antes de executar)

| Doc | URL ClickUp | Conteúdo |
|-----|-------------|----------|
| Diretriz Compras e Contratações | `https://app.clickup.com/9011929793/v/dc/8cje8p1-19631/8cje8p1-25931` | Regras de formalização, modelo de email, link de cadastro, fluxo de pagamento |
| Escopo - Principais Fornecedores NTICS | `https://app.clickup.com/9011929793/v/dc/8cje8p1-19631/8cje8p1-37451` | Responsabilidades e entregáveis por tipo de função (Produtor, Educador, Fotógrafo, Ator, etc.) |

> Esses dois documentos são a base. Carregue-os via MCP ClickUp (`clickup_get_document_pages`) no início de qualquer execução.

---

## Inputs

### Obrigatórios (uma linha do Budget por fornecedor)

| Campo | Origem | Descrição |
|-------|--------|-----------|
| `projeto` | Budget | Ex: `132. ESTAÇÃO SAMARCO` |
| `negociador` | Budget | Nome do responsável interno |
| `class1` / `class2` | Budget | Ex: `1.EQUIPE` / `1.B. Staff (em campo)` |
| `servico` | Budget | Ex: `Palestra`, `Produtor Executivo`, `Designer` |
| `fornecedor_razao` | Budget | Nome como aparece na planilha |
| `fornecedor_nome_completo` | Usuário | Nome completo real (se diferente do Budget) |
| `detalhamento` | Budget | Texto da coluna "Detalhamento do Serviço" |
| `valor_contratado` | Budget | Ex: `R$ 10.200,00` |
| `forma_pagamento` | Budget | Datas e parcelas (formato DD/MM - R$ X) |
| `email_fornecedor` | Usuário | Para CC no email |

### Opcionais

| Campo | Quando usar |
|-------|-------------|
| `bio_fornecedor` | Quando o usuário envia descrição de quem é a pessoa — ajuda a enriquecer o escopo |
| `metas_quantitativas` | Número de pessoas, ações, horas (preenche os `xxx` no escopo padrão) |
| `municipios` | Quando o escopo é geográfico (ex: produtora de campo por território) |

---

## Mapeamento Serviço → Seção do Escopo

| Serviço (Budget) | Seção do doc Escopo |
|------------------|---------------------|
| Produtor Executivo, Produção de Campo | Seção 2 (Produtor Executivo Local) + Seção 3 (Articulador) |
| Educador, Oficineiro, Palestrante | Seção 4 (Educador) |
| Fotógrafo | Seção 5 (Fotógrafo) |
| Ator, Equipe Teatral | Seção 6 (Atores / Equipe Teatral) |
| Monitor, Assistente | Seção 7 (Assistente / Monitor) |
| Designer, Design | Obrigações gerais (Seção 1) + cessão de direitos + entrega em alta resolução |
| Assessoria de Imprensa | Obrigações gerais (Seção 1) + releases + clipping + relatório |
| Editor de Vídeo | Obrigações gerais (Seção 1) + edição conforme briefing + cessão de direitos |

> Para funções fora da tabela, use as Obrigações Gerais (Seção 1.1 + 1.2) como base e adapte com o detalhamento do Budget e o contexto do usuário.

---

## Execução

### Fase 1: Coletar e validar inputs (gate humano)

1. Receba as linhas do Budget do usuário (pode ser uma ou várias por vez).
2. Para cada linha, confirme se tem **nome completo** e **email** do fornecedor.
3. Se faltar qualquer um dos dois, pergunte antes de continuar.
4. Verifique se há `metas_quantitativas` (nº de pessoas, horas, ações) — se não houver, pergunte se o usuário quer preencher ou deixar como `[a definir]`.

### Fase 2: Montar o escopo (auto)

Para cada fornecedor:

1. Identifique a seção do doc **Escopo - Principais Fornecedores NTICS** que corresponde ao serviço.
2. Use o `detalhamento` do Budget como linha mestra do escopo.
3. Complemente com as responsabilidades da seção correspondente (pré-execução, execução, acessibilidade, entregáveis).
4. Se houver `bio_fornecedor`, extraia informações contextuais que reforcem o escopo (ex: território de atuação, especialidade).
5. Sempre inclua ao final:
   - Cessão de direitos autorais e/ou uso de imagem (quando aplicável ao tipo de função)
   - Nota fiscal dentro do prazo acordado

### Fase 3: Compor o email (auto)

Seguir exatamente o modelo da Diretriz Compras e Contratações (Seção 8):

```
Para: producao@ntics.com.br; abilio@ntics.com.br; compras@ntics.com.br
Cc: [email do fornecedor]
Assunto: ORÇAMENTO FORNECEDOR_[SERVIÇO]_[Nº PROJETO]_[NOME DO PROJETO]_[VALOR]

Olá Ariadne, tudo bem?

Gostaria de formalizar a contratação de [NOME DO FORNECEDOR].
Por favor, seguir com o processo de cadastro/contrato e programação de pagamento.

[NOME DO FORNECEDOR], seguem as informações:

- Projeto: [Nº] – [NOME DO PROJETO] – [CIDADE/UF, se aplicável]
- Serviço contratado: [SERVIÇO]
- Escopo (entregáveis):
  [bullets gerados na Fase 2]
- Valor total: R$ [VALOR]
- Condição/programação de pagamento:
  [parcelas do Budget]
- Observação NTICS: Se houver ajuste por atraso/mudança de execução,
  o pagamento será prorrogado de acordo com o novo cronograma do projeto.

Cadastro do fornecedor (quando necessário):
https://docs.google.com/forms/d/e/1FAIpQLSchYAY0nRmsyd1y-S_t67lOC23UbyFEMFyH99rW8p37DCNfDA/viewform
Caso já tenha cadastro, não precisa realizar novamente o preenchimento.

Atenciosamente,
[NEGOCIADOR]
NTICS Projetos
```

### Fase 4: Salvar drafts no Gmail (auto)

Para cada email composto:
1. Chamar `mcp__claude_ai_Gmail__create_draft` com:
   - `to`: `["producao@ntics.com.br", "abilio@ntics.com.br", "compras@ntics.com.br"]`
   - `cc`: `[email do fornecedor]` (quando disponível)
   - `subject`: assunto no padrão acima
   - `htmlBody`: email formatado em HTML com listas aninhadas
2. Confirmar o `id` do draft retornado.

### Fase 5: Verificar e reportar (auto)

Após salvar todos os drafts, reportar:

| Fornecedor | Assunto | Status |
|------------|---------|--------|
| Nome | Assunto completo | Draft salvo / Erro |

Lembrar o usuário de:
- Confirmar se o Budget foi atualizado para **ENVIADO COMPRAS**
- Adicionar CC do fornecedor nos drafts onde o email estava faltando (se houver)

---

## Output esperado

- N drafts salvos no Gmail (um por fornecedor)
- Tabela de confirmação com nome, assunto e status de cada draft

---

## Checklist de qualidade

- [ ] Nome completo do fornecedor está correto no assunto e no corpo
- [ ] Assunto segue o padrão: `ORÇAMENTO FORNECEDOR_[SERVIÇO]_[Nº]_[PROJETO]_[VALOR]`
- [ ] Escopo tem pelo menos 4 bullets específicos (não genéricos)
- [ ] Parcelas batem com a coluna "Forma de Pagamento" do Budget
- [ ] Link de cadastro presente em todos os emails
- [ ] Observação NTICS de prorrogação presente
- [ ] Draft confirmado com `id` retornado pelo Gmail

---

## Dependências

**Upstream (precisa estar pronto antes):**
- Linha do Budget com status **ORÇADO** e dados completos

**Downstream (após envio):**
- Budget atualizado para **ENVIADO COMPRAS**
- Compras/Financeiro processa cadastro e programação de pagamento
