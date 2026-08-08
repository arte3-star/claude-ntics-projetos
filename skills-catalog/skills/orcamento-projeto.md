---
name: orcamento-projeto
description: >
  Monta o orçamento de produção de um projeto NTICS no formato oficial da planilha
  "2026 ORÇAMENTO NTICS PRODUÇÃO GERAL" (colunas Class1/Class2/Serviço/Fornecedor/Qtd/Unit/
  Estimado). Lê a lista de material e a metodologia do projeto no SecondBrain, consulta o
  catálogo de fornecedores já cadastrados da NTICS (Supabase Portal NTICS + fallback local)
  para usar preços reais, e completa o que falta com pesquisa de preço online (local por
  cidade quando é serviço tipo mesa/cadeira/tenda). Acione SEMPRE que o usuário disser
  "monta o orçamento do projeto X", "preciso orçar", "orçamento de produção", "cotar os
  itens/materiais do projeto", "quanto vai custar o projeto/evento", "faz o orçamento em
  cima do que vendi", ou ao abrir um projeto novo que precisa de orçamento — mesmo que ele
  não diga a palavra "orçamento" explicitamente (ex.: "preciso saber quanto sai a estrutura
  do evento", "levanta os custos das oficinas"). Também acione para atualizar/refinar um
  orçamento já começado ou trocar preços por fornecedor cadastrado.
---

# Orçamento de Projeto NTICS

Esta skill transforma a metodologia de um projeto em um orçamento de produção real, no
formato da planilha oficial, usando os fornecedores que a NTICS já contratou como fonte de
preço e pesquisa online só para o que falta. Ela **cresce com o uso**: a cada projeto,
novas regras e preços validados voltam para `references/regras-aprendidas.md` e para o
catálogo Supabase.

**Leia primeiro** `references/regras-aprendidas.md` (as lições de projetos anteriores — evita
repetir erros) e `references/formato-ntics.md` (as 17 colunas, a taxonomia Class1/Class2 e o
mapeamento catálogo→orçamento). Elas são o cérebro da skill; o texto abaixo é o passo a passo.

## O processo (6 passos)

### 1. Ler a fonte real (não chutar os itens)
Os itens do orçamento vêm de `SecondBrain/projetos/<slug>/`:
- `lista-de-material-<proj>.md` — o levantamento "sem preços" de tudo que precisa ser
  produzido/comprado/alugado, por categoria e por oficina. É a espinha do orçamento.
- `metodologia-detalhada-<proj>.md` — o bloco "5. Materiais" de cada atividade, com o
  briefing de cada peça, e o dimensionamento (cidades, grupos, salas).
- Se existir a **imagem/arte do que foi vendido** (evento, praça, feira), itemize a
  estrutura a partir dela — o que foi vendido manda (regra 13).

Se não achar a lista de material, leia a metodologia e monte a lista você. Não invente itens.

### 2. Dimensionar e classificar cada item
Anote os parâmetros do projeto: nº de cidades, grupos/equipes, salas, turnos. Para cada
item decida como ele escala (define a coluna Reco — ver formato-ntics.md):
- **Itinerante** (produz 1× e viaja) · **Aluguel local** (×cidade) · **Consumível** (×cidade/×grupo).
Confirme com o usuário o que é itinerante e o que é alugado localmente — parte do material
viaja, parte se contrata em cada praça.

### 3. Preço em cascata: catálogo primeiro, web depois
Para **cada Serviço**, rode o catálogo antes de pesquisar na web:
```
python .claude/skills/orcamento-projeto/scripts/consulta_catalogo.py "<serviço>"
```
(ex.: `"Banner"`, `"Backdrop"`, `"Camiseta"`, `"Hospedagem"`, `"Gerador"`). Use `--json` para
saída estruturada, `--listar-servicos` para ver todos os nomes, `--live` para tentar o
Supabase ao vivo antes do fallback local.

- **Achou fornecedor cadastrado (✓):** use `valor_unitario` + `razao_social` + `cnpj`. Escolha o
  de maior `n_contratacoes` (o "★ mais contratado"), salvo motivo pra outro. **Cuidado com a
  regra 1** (o valor pode ser de um lote, não unitário — cheque a faixa/especificação).
- **Não achou, ou é serviço local (mesa/cadeira/tenda/som/palco/gerador):** pesquise o preço
  **online, por cidade** (regra 2). Guarde o link/fonte.
- **Consolide** no fornecedor que faz mais coisas (regra 4).

### 4. Aplicar as regras aprendidas
Antes de fechar valores, passe a lista por `references/regras-aprendidas.md`. As que mais
pegam: lote≠avulso, produto≠nome-parecido, Rouanet não paga máquina (contrapartida R$0),
evento em turnos = metade do mobiliário, deck personalizado custa mais que carta avulsa.

### 5. Montar no formato oficial
Produza as linhas nas 17 colunas (ver formato-ntics.md). `VALOR Estimado = Qtd×Ciclos×Reco×Unit`.
Deixe `VALOR cotado` **vazio** (só entra com orçamento real fechado). Marque em destaque os
itens "A COTAR / A CALCULAR / CONTRAPARTIDA / OPCIONAL". Sinalize as premissas de quantidade
que ainda dependem de confirmação da produção.

Separe por blocos/abas quando fizer sentido: Comunicação visual, Material, Viagens, Evento —
cada um no mesmo cabeçalho. Viagem itemizada (cada voo/carro/hospedagem, por cidade).

### 6. Entregar + crescer a memória
Entregue como o usuário pedir: tabela pra colar (TSV), CSV no formato do artifact de
Orçamento de Projeto, ou .xlsx/Google Sheets (uma aba por bloco). **Ao final, atualize
`references/regras-aprendidas.md`** com o que aprendeu neste projeto e, se houver preço novo
validado, proponha devolvê-lo ao catálogo Supabase (o cadastro cresce).

## Saída em CSV (para importar na planilha real)
O artifact "Orçamento de Projeto" exporta com este cabeçalho exato — use-o ao gerar CSV:
```
Projeto,Negociadores,Class1,Class2,Serviço,Fornecedor (Razão),Detalhamento,Qtd,× Ciclos,× Recorrências,R$ Unit,VALOR cotado R$,VALOR Contratado R$,Forma de Pagamento,TIPO,Orçamento,Sinal errado
```
(No .xlsx-mestre interno usamos "× Reco" e "VALOR Estimado R$"; para importar na planilha
oficial, use o cabeçalho acima.)

## Catálogo de fornecedores (fonte de preço nº 1)
- Supabase **Portal NTICS** (`<REF_PROJETO_SUPABASE>`): tabelas `fornecedores` e
  `itens_fornecedor` (leitura pública por RLS). Colunas em formato-ntics.md.
- Dashboard ao vivo: `output/cotador-fornecedores/Catalogo_Fornecedores_AoVivo.html`.
- **Fallback local** (usado por padrão pelo script): `data/cotador_data.json` (611
  fornecedores / 98 produtos / 2.336 registros). Se a leitura ao vivo estiver vazia (RLS/
  chave), o fallback garante a consulta.

## Subir para Google Sheets (se pedirem)
Base64 inline no MCP não é confiável para binário — use a API do Drive via `tools/gws`
(`files().update` mantém o mesmo link; `verify=False` por causa do Norton). Ver a memória
[[reference_upload_binario_drive_api]].
