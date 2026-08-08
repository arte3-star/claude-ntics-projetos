---
name: abertura-budget
description: >
  Abre o pré-orçamento (Fase 1, alocação macro) de um projeto novo: faz uma série de
  perguntas (nome/patrocinador, budget total, tipo de projeto, cidades/localidades, escolas
  já confirmadas, alunos esperados, fonte de recurso, duração), calcula a distribuição do
  budget total por Class1/Class2/Serviço usando o padrão histórico de % de gasto daquele
  tipo de projeto, e cria uma aba nova já com essas linhas na planilha oficial "2026
  ORÇAMENTO NTICS PRODUÇÃO GERAL". Acione SEMPRE que o usuário disser "abrir um budget/
  orçamento novo", "preciso montar o pré-orçamento do projeto X", "quanto vai pra cada
  categoria nesse projeto", "cria a aba de orçamento do projeto novo", ou ao começar a
  planejar financeiramente um projeto que ainda não tem cotação nenhuma. É o PASSO 0 antes
  da skill `orcamento-projeto` (que detalha item por item com fornecedor real depois que
  esta primeira alocação existe).
---

# Abertura de Budget NTICS

Gera a primeira versão (macro, por padrão histórico) do orçamento de um projeto novo —
antes de ter qualquer cotação real. Não substitui `orcamento-projeto` (que detalha linha a
linha com fornecedor de verdade); esta skill só dá o ponto de partida: "dado que temos
R$X e o projeto é do tipo Y, como isso provavelmente se divide?"

**Leia primeiro:** `references/tipos-e-perguntas.md` (os 7 tipos, como classificar, a lista
exata de perguntas) e `references/formato-abertura.md` (como o valor é calculado, o estilo
visual e o formato de saída). Os dados por trás (`data/padroes_tipo.json`,
`data/template_servicos_por_tipo.json` e `data/projetos_historicos.json` — este último com o
breakdown completo dos 40 projetos individuais, não só a média por tipo) vêm da análise em
[[project_padroes_orcamento_tipos]] — 40 projetos reais de 2023-2026.

## O processo (4 passos)

### 1. Fazer as perguntas
Siga a ordem de `references/tipos-e-perguntas.md`. Pode fazer em bloco (uma mensagem com
todas) ou uma a uma — o usuário escolhe. As únicas realmente obrigatórias pro cálculo são
**budget total** e **tipo de projeto**; as outras (cidades, escolas, alunos, fonte de
recurso, duração) alimentam o registro do projeto e a checagem de sanidade do passo 3.

Se o usuário não souber o tipo, ajude a classificar pela tabela de palavras-chave — não
adivinhe sem checar com a pessoa quando for ambíguo.

### 2. Calcular o pré-orçamento
```
python scripts/calcular_pre_orcamento.py --tipo "<um dos 7 tipos>" --budget <valor> \
    --projeto "<NNN. NOME (PATROCINADOR)>" --negociador "<nome>" --json > /tmp/pre_orc.json
```
Isso gera as linhas já normalizadas pra somar exatamente o budget informado. Use
`--sem-servicos` se o usuário preferir só os totais por Class1/Class2 sem sugestão de
serviço (pergunte se não tiver certeza — o padrão é COM sugestão de serviços, decisão do
Lucas 2026-08-07).

### 3. Checagem de sanidade (antes de escrever) — mostre os exemplos reais mais próximos
O comando acima já devolve `exemplos_proximos`: os 2-3 projetos REAIS daquele tipo com
orçamento total mais parecido com o budget informado (não só a média do tipo — casos de
verdade, com nome, valor, % real por Class1 e cidades/alunos quando existir). **Mostre isso
ao usuário antes de escrever a aba** — é a forma de verificar se o pré-orçamento gerado faz
sentido contra o que já aconteceu, não só contra uma média abstrata.

Também compare o budget informado com `custo_por_cidade_media`/`custo_por_aluno_media` do
tipo em `data/padroes_tipo.json`, usando o nº de cidades/alunos que o usuário informou. Se o
budget implícito por cidade/aluno estiver muito fora da faixa histórica (ex.: menos da
metade ou mais que o dobro) — ou se os exemplos próximos tiverem uma % por Class1 bem
diferente do que o pré-orçamento gerado —, avise antes de seguir.

### 4. Escrever a aba na planilha oficial
```
python scripts/escrever_aba_planilha.py --spreadsheet-id <ID_PLANILHA_GOOGLE> \
    --aba "<NNN. NOME (PATROCINADOR)>" --linhas-json /tmp/pre_orc.json
```
Roda com `--dry-run` primeiro se quiser confirmar o que vai ser escrito antes de fato criar
a aba. Sem `--dry-run`, cria a aba de verdade e devolve o link direto (`#gid=...`).

**Isso escreve numa planilha de produção que o Abílio usa todo dia** — confirme o nome
exato da aba com o usuário antes de rodar sem `--dry-run` se houver qualquer dúvida sobre o
número do projeto ou o nome do patrocinador (evita ter que renomear/apagar depois).

## Depois de criar a aba

Diga ao usuário que a Fase 1 está pronta e que o próximo passo natural é rodar
`orcamento-projeto` pra substituir cada linha "A DETALHAR" por fornecedor e preço real do
catálogo — mas isso só quando ele pedir, não encadeie automaticamente.

## Crescer a skill

Se um projeto novo não encaixar bem em nenhum dos 7 tipos, ou se um tipo precisar de um 8º
serviço típico que não está no template, registre isso e, quando tiver orçamento real
fechado desse projeto, ele deveria entrar na próxima atualização de
`data/padroes_tipo.json`/`data/template_servicos_por_tipo.json` (regerar a partir do
pipeline em [[project_padroes_orcamento_tipos]], não editar esses JSONs à mão).
