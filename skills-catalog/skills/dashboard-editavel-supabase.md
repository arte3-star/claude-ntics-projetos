---
name: dashboard-editavel-supabase
description: >-
  Adiciona uma camada de edicao autenticada a um dashboard HTML estatico
  (GitHub Pages, arquivo local, etc.): pessoas com login (email+senha) editam os
  textos direto na pagina e salvam de forma persistente no Supabase; quem nao
  esta logado ve a versao salva, sem editar. Use SEMPRE que o usuario pedir para
  "deixar o dashboard editavel", "editar e salvar no dashboard", "colocar login
  pra editar", "cada pessoa editar o texto e salvar", "acesso com usuario e
  senha pra editar", "camada de edicao", "editor inline", ou quiser reaproveitar
  esse esquema (Supabase) em outro dashboard/projeto (128, 129, 132, novos). Cobre
  criar a tabela + RLS, injetar a camada no HTML, criar os usuarios editores
  (por lista ou puxando membros do ClickUp), publicar e testar o login.
---

# Dashboard editavel com Supabase

Transforma um dashboard HTML estatico num dashboard onde pessoas autenticadas
editam os textos inline e salvam. Backend = **Supabase** (Auth + uma tabela
`dashboard_content` com Row Level Security). A pagina continua estatica: um
`<script type="module">` injetado carrega o conteudo salvo, faz login e grava.

**Como funciona:** cada bloco de texto ganha um `data-edit-id`. Ao abrir, a
pagina busca no Supabase o conteudo salvo daquele bloco e substitui. Uma barra
flutuante oferece "Entrar para editar" -> login -> "Editar" (torna o texto
editavel) -> "Salvar" (upsert). Leitura e publica (RLS `using(true)`); escrita
so autenticada. O conteudo e separado por dashboard pela coluna `projeto`.

**Fundamentos do Supabase** (estrutura da conta, achar URL/chaves, SQL Editor,
RLS, gotchas): use a skill **`supabase-guia`** — esta skill e um fluxo especifico
em cima daquela base.

## Regra de seguranca (nao pule)

O assistente **NAO cria contas nem digita senhas para autenticar**, mesmo que
peçam. Na pratica isso significa:
- **Criar os usuarios** (SQL do `02_criar_usuarios`): o assistente prepara e cola
  o SQL no editor, mas o clique final em **Run** e do usuario.
- **Testar o login**: o assistente pode preencher o **e-mail** (dado comum) e
  toda a parte de editar/salvar, mas **digitar a senha e clicar "Entrar" e do
  usuario**. Depois de logado, o assistente assume o teste de edicao/salvar.
- Verificacoes que NAO sao "autenticar" (checar hash com `crypt`, testar leitura
  anon, probe com senha errada) o assistente pode fazer — ver a skill `supabase-guia` (references/gotchas.md).

## Passo a passo

### 0. Pre-requisitos
- Um projeto **Supabase** onde o usuario tenha acesso de dono (Settings -> API).
  Pode reusar um existente (ex.: um "CNH Project") ou criar novo. Reusar um
  projeto que guarda PII de outra coisa e aceitavel: a tabela `dashboard_content`
  fica isolada e o RLS protege; mas se preferir isolamento total, use projeto
  proprio.
- O(s) arquivo(s) HTML do dashboard.

### 1. Pegar URL + chave publica do projeto
No painel: **Settings -> API Keys**. Precisa da **URL** (`https://<ref>.supabase.co`,
o `<ref>` esta na barra de endereco) e da **chave publica** (`sb_publishable_...`
ou a `anon` JWT — as duas servem). **Nunca** a `service_role`/`secret`.
Detalhes (onde achar, por que a leitura da chave via navegador e bloqueada):
skill `supabase-guia`, references/estrutura-e-onde-achar.md e references/gotchas.md.

### 2. Criar a tabela + RLS (uma vez por PROJETO Supabase)
Rode `scripts/sql/01_tabela_dashboard_content.sql` no **SQL Editor**. Vai pedir
confirmacao ("Potential issue detected") por causa do DDL — confirme.

### 3. Injetar a camada no HTML
Para cada dashboard:
```bash
python scripts/add_edit_layer.py \
  --file caminho/dashboard.html \
  --proj 129 \
  --url https://<ref>.supabase.co \
  --key <CHAVE_SUPABASE_PUBLIC>
```
O `--proj` separa o conteudo por dashboard na tabela (use um id estavel: "128",
"129", "132"...). O script e **idempotente** (reinjeta sem duplicar) e marca os
blocos `.acc-body` e `.doc-summary`. Se o dashboard usar outras classes de bloco,
ajuste os `re.sub` no script.

### 4. Criar os usuarios editores
Copie `scripts/sql/02_criar_usuarios_TEMPLATE.sql`, edite a lista `VALUES` com
`('email','Senha')` (padrao sugerido: `PrimeiroNome2026`), cole no SQL Editor.
**O usuario clica Run** (criacao de conta). As senhas ficam so como hash — anote
antes. Para desambiguar nomes repetidos, varie a senha (ex.: `JessicaLora2026`).

**Puxar a lista do ClickUp** (opcional): use
`mcp__5cef576d-...__clickup_get_workspace_members`, monte `email` + `PrimeiroNome2026`,
pule contas genericas (PMO, Trainee) e duplicatas.

### 5. Publicar
Se o dashboard esta no GitHub Pages deste workspace, siga o procedimento padrao
de publicacao do repo (worktree temporario, commitar so os arquivos alterados,
push para `master`). Ver a memoria `feedback_git_desktop_ini_gdrive` e o fluxo
de publicacao ja usado nos dashboards. Dica para o checkout nao estourar timeout
com muitos arquivos no Drive: `git worktree add --no-checkout` e copiar so os
HTMLs alterados. Confirme no ar com uma requisicao + cache-buster.

### 6. Testar
Abra o dashboard, "Entrar para editar", **peca ao usuario** para digitar a senha
e entrar; depois clique "Editar", altere um bloco, "Salvar", recarregue e
confirme que persistiu. Se "travar sem erro", quase sempre e senha errada (a
pessoa digitou a senha pessoal em vez da `PrimeiroNome2026`).

## Arquivos da skill
- `scripts/add_edit_layer.py` — injeta a camada (login + editar + salvar +
  trocar senha; erros de login visiveis; timeout de 15s).
- `scripts/sql/01_tabela_dashboard_content.sql` — tabela + RLS.
- `scripts/sql/02_criar_usuarios_TEMPLATE.sql` — cria os logins (editar a lista).
- `scripts/sql/03_resetar_senha.sql` — reset de senha pelo admin.

Para fundamentos e armadilhas do Supabase (chaves, colar SQL no Monaco, verificar
sem logar, criar user por SQL/identities, instabilidade do painel), **leia antes**
a skill **`supabase-guia`**.
