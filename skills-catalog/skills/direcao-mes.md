---
name: direcao-mes
description: |
  Gera e publica a "Direção da Semana" da NTICS — o painel que dirige a semana que começa,
  em quatro blocos: o que está Atrasado, o que é da semana, e o que vem nas duas seguintes.
  Uma aba por projeto. A entrega é a tarefa-mãe, com as subtarefas aninhadas dentro dela,
  quem é responsável, a fase do projeto e o status. As já concluídas aparecem riscadas em
  verde; as atrasadas trazem o selo de há quantos dias venceram.

  Acione SEMPRE que o usuário disser: "direção da semana", "direção do mês", "direção do
  período", "atualiza a direção", "o que está atrasado por projeto", "o que cada projeto
  entrega por semana", "entregas por projeto", "o que vem pela frente por projeto".
  Também acione quando a rotina de domingo disparar.

  NÃO confundir com `painel-escritorio` (diário, a unidade é a PESSOA) nem com
  `norteador-semana` (infográfico da Hands On). Aqui a unidade é o PROJETO e a divisão é
  por semana.
---

# Direção da Semana

Painel que dirige a semana que começa. Fonte: ClickUp. Publicado no GitHub Pages.

**https://arte3-star.github.io/claude-ntics-projetos/dashboards/direcao-mes.html**

## Como rodar

```
python ~/.claude/skills/direcao-mes/scripts/rodar.py
```

- `4` (ou outro número) → muda quantas semanas para frente (padrão 3)
- `--local` → não publica
- `--so-build` → reaproveita o `dados.json` e só remonta o HTML

Saída em `G:\My Drive\Claude-NTICS-Projetos\tmp\direcao-mes\`.

## O recorte — este painel é prospectivo

Roda no domingo e dirige a semana que começa. **Não é retrospectiva**: o passado só entra
como atraso. Quatro blocos, sempre nesta ordem:

| Bloco | O que é |
|---|---|
| **Atrasado** | vencido e ainda aberto, olhando até 90 dias para trás |
| **A semana** | a semana que contém amanhã (seg a dom) — a que está sendo dirigida |
| **+1 semana** | a seguinte |
| **+2 semanas** | a terceira |

Atrasado + 3 semanas é o que dá a visão do mês. Rodando toda semana, a janela anda junto.

Tarefa **concluída no passado não entra** — ela não dirige nada e só faria volume. Já as
concluídas dentro das 3 semanas entram, riscadas em verde, porque a semana precisa mostrar
o que já saiu.

## O que o painel mostra

**Aba Geral** (mesmo vocabulário visual do `painel-escritorio`, que divide o `base.css`):

1. **Resumo em texto** — parágrafo derivado dos números, nada escrito à mão.
2. **4 cards de risco** — atrasado · alta/urgente vencida · a semana · projeto mais atrasado.
3. **Colunas de volume** por bloco + **3 donuts** (atraso na mão da equipe, quanto da
   semana já saiu, entregas com responsável).
4. **Grid de cards de projeto** — atraso como número grande, mini-barras de esta semana e
   próxima, faixa de situação do que está vencido, avatares de quem carrega, última reunião.
5. **Matriz projeto × bloco**.
6. **Matriz pessoa × projeto** — a carga real de cada um, com selo vermelho de quanto
   daquela célula já venceu. O fundo escurece pela **proporção de atraso**, não pelo
   volume: 8 tarefas em dia são menos urgentes que 3 vencidas.
7. **Carga por pessoa** — 4 barras (atrasadas · esta semana · próxima · +2), ordenada por
   quanto cada um tem vencido.
8. **As últimas reuniões** e a metodologia, recolhidas.

**Uma aba por projeto**: cabeçalho com número, nome, fase dominante, equipe e mini-barras
dos blocos · **resumo em texto do projeto** · **o que as reuniões decidiram** · os 4 blocos
com os cards. No botão da aba, o número vermelho é quanto está atrasado e o cinza é quanto
vence na semana.

**Ordem das abas e das linhas da matriz é alfabética** — projeto numerado ordena pelo
número (#74 antes de #115, não a ordem de texto), os nomeados vêm depois pelo nome. É
ordem fixa de propósito: o Lucas procura o projeto pelo número, e ordem que muda toda
semana obriga a procurar de novo.

**Card de entrega**: data e dia · selo `há N d` quando está atrasada · fase · nome clicável
para o ClickUp · fotos de todos os responsáveis (da entrega e das subtarefas) · status ·
selo de alta/urgente · `▸ N subtarefas` recolhido.

A borda esquerda do card é a situação: vermelha não começou, laranja em andamento, azul
fora das mãos (revisão/aguardando externo), verde concluída — e a concluída fica riscada.

## A tarefa-mãe tem que estar visível

O maior problema do painel era esse: a maior parte dos cards é subtarefa, e sozinha ela
não diz de que frente é — quatro cards "Receber termo de adesão assinado" lado a lado, sem
assunto. O `de: <mãe>` em itálico no rodapé não resolvia.

Agora, dentro de cada bloco:

- **2 ou mais irmãs no mesmo bloco** → viram um **grupo com a mãe no cabeçalho**: nome
  clicável para o ClickUp, quantas entregas, quantas atrasadas e a fase. Os cards ficam
  dentro do grupo.
- **Irmã sozinha** → mantém o chip **`↑ nome da mãe`**, agora azul e clicável, acima do
  nome da entrega em vez de escondido no rodapé.

Não trocar isso por "promover a mãe a entrega": a mãe está fora da janela justamente
porque não vence no período, e promovê-la faria o painel mostrar prazo que não existe.

## As decisões vêm das reuniões

Cada aba de projeto traz **o que as reuniões decidiram**, lido de
`C:\Users\lucas\Nextcloud\NTICS-OS\ntics-nucleo\Reuniões\AAAA-MM.md` — as fichas que a
rotina `colher-reunioes-ntics` escreve. Janela de 45 dias.

O painel **transcreve Decisão e Encaminhamento como estão**. Não interpreta transcrição e
não inventa decisão: se não está na ficha, não entra. O casamento ficha × projeto é feito
pelo número do projeto **só no cabeçalho da ficha** — o corpo tem valor em reais e
quantidade de aluno, que viram falso positivo na hora.

Rodando na nuvem o Nextcloud não existe; o painel sai sem o bloco e diz isso na
metodologia, em vez de falhar.

## Definições

- **Entrega = tarefa-mãe**: tarefa da janela que não tem outra tarefa-mãe dentro da janela.
  Se a mãe existe mas está fora, o card mostra `de: <nome da mãe>` — sem isso a subtarefa
  aparece solta e perde o contexto.
- **A semana** é a que contém *amanhã*. Rodando no domingo, começa amanhã; rodando no meio
  da semana, é a própria semana em curso. Não hardcodar data.
- **Fase**: campo oficial `Fases do Projeto` (`e766d376-5231-4c34-9bab-9fb7d1e74c6a`);
  quando a tarefa não tem, herda da tarefa-mãe subindo a cadeia.

## Armadilhas da API do ClickUp — já resolvidas, não "simplificar"

| Armadilha | Como o script trata |
|---|---|
| `last_page` volta `true` no meio da paginação e trunca | Só para quando a página vem **vazia** |
| Sem `subtasks=true` some a maior parte do volume | Sempre `true` |
| Lista "Modelo de Projeto - Claude" é template | Descartada de todas as contas |
| `git` no Drive contamina o `.git` com `desktop.ini` | Publicar só via `gh api` |

**Ressalva do rodapé:** tarefa com mais de um responsável conta para cada um na carga
por pessoa.

## Estrutura

```
scripts/pull.py       ClickUp -> dados.json (atrasado + N semanas, herança de fase)
scripts/build.py      dados.json + reuniões -> HTML (Geral visual + aba por projeto)
scripts/visual.py     componentes: donut, colunas, cards de risco, card de projeto, matriz, leaderboard
scripts/reunioes.py   fichas do NTICS OS -> decisões por projeto
scripts/publicar.py   gh api PUT + verificação do que ficou no repo
scripts/rodar.py      orquestra pull -> build -> publicar
references/base.css   CSS compartilhado com o painel-escritorio
references/fotos-equipe.md
```

**Placeholders são lista de pares com checagem de duplicata**, não `dict` nem tupla de
`%s`: chave repetida num dict é descartada em silêncio e engole o bloco inteiro sem erro
nenhum — foi assim que o leaderboard sumiu do painel-escritorio por várias rodadas. O build
aborta se sobrar `__XXX__` sem substituir.

## Limites

- Só leitura no ClickUp.
- **Não filtra "principais" por critério de prioridade.** Toda tarefa-mãe entra como
  entrega; a hierarquia é que separa entrega de detalhe. Se for para cortar (só high/urgent,
  só com etiqueta de campo), o critério precisa ser dito — não inventar.
- Projeto sem tarefa na janela não gera aba.
