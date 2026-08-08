---
name: supabase-guia
description: >-
  Guia de fundamentos do Supabase para QUALQUER uso (nao so dashboards): entender
  como a conta esta estruturada (organizacao -> projetos/bases), o que fazer ao
  criar uma base nova, onde achar a URL, as chaves (publishable/anon/secret) e o
  SQL Editor, e como conectar/operar de um cliente (supabase-js: CRUD, Auth, RLS).
  Use SEMPRE que o usuario mencionar Supabase, criar uma base/projeto novo, achar
  a chave/URL/connection string, escrever ou rodar SQL no Supabase, configurar
  login/Auth, tabelas ou Row Level Security, guardar dados de um site/app estatico
  num backend, ou quiser "estudar/entender como usar o Supabase". É a skill-base;
  fluxos especificos (ex.: dashboard editavel) referenciam esta.
---

# Guia do Supabase (fundamentos, para qualquer projeto)

Supabase = Postgres gerenciado + Auth + Storage + APIs automaticas (REST e
realtime) em cima do banco. Para um site/app estatico (HTML no GitHub Pages, por
exemplo), ele funciona como backend sem servidor: o cliente fala direto com o
banco via `supabase-js`, e a seguranca vem do **Row Level Security (RLS)** no
Postgres + de uma **chave publica** que pode ficar embutida na pagina.

Esta skill e a base. Comece por ela sempre que o assunto for Supabase; depois vá
para o fluxo especifico (ex.: a skill `dashboard-editavel-supabase`).

## Como a conta do Lucas está estruturada

- **Conta Supabase do Lucas** -> 1 organizacao **"NTICS Projetos"** (Free Plan).
- Dentro dela, os **projetos** (o Supabase chama de projeto; é a "base" nova que
  você cria). Hoje: **"CNH Project"** (ref `<REF_PROJETO_SUPABASE>`), usado pela
  camada de edicao dos dashboards 128/129.
- Hierarquia mental: **Conta -> Organizacao -> Projeto (base) -> Tabelas / Auth /
  Storage**. Cada projeto tem seu proprio Postgres, suas chaves e sua URL.
- O plano Free cobre bem casos pequenos (500 MB de banco, 50k usuarios ativos/mes).
  Um mesmo projeto pode hospedar varias tabelas/apps; nao precisa um projeto por
  dashboard — separe por tabela/coluna quando fizer sentido.

## Ao criar uma base nova

No painel (supabase.com/dashboard): **New project** -> escolher a organizacao,
dar nome, definir a **senha do banco** (guarde-a; é o Postgres, nao é login de
usuario final) e a regiao. Espera uns minutos provisionar. Depois, tudo que você
vai precisar está em **Settings** e no menu lateral. Onde achar cada coisa:
`references/estrutura-e-onde-achar.md`.

## O que esta skill cobre (leia o reference certo)

- **Onde achar URL, chaves e o SQL Editor; para que serve cada chave** ->
  `references/estrutura-e-onde-achar.md`
- **Conectar de um cliente e operar** (supabase-js via esm.sh, select/insert/
  upsert, Auth com email+senha, RLS, criar usuario por SQL) ->
  `references/conectar-e-operar.md`
- **Gotchas / armadilhas** (chave anon é bloqueada de leitura pelo navegador,
  colar SQL grande no editor Monaco, aviso "Potential issue detected", verificar
  credencial sem logar, instabilidade do painel) -> `references/gotchas.md`

## Regra de seguranca (vale para qualquer uso)

- A **chave `service_role`/`secret`** ignora o RLS = acesso total. **Nunca** vai
  para o navegador/HTML/repo publico. Só a `publishable`/`anon` fica exposta, e o
  RLS é quem protege de fato.
- O assistente **NAO cria contas de usuario nem digita senhas para autenticar**,
  mesmo a pedido: prepara e cola o SQL/os passos, mas o Run de criacao de conta e
  o login de teste sao do usuario. Verificar sem logar (crypt no SQL, probe com
  senha errada, leitura anon) o assistente pode — ver `references/gotchas.md`.
- Habilite RLS em toda tabela exposta e escreva policies explicitas. Sem RLS +
  chave publica = qualquer um lê/escreve tudo.
