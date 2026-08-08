---
name: painel-escritorio
description: |
  Gera e publica o "Painel do Escritório de Projetos" da NTICS — o dashboard diário
  que mostra, por pessoa e por projeto, o que foi concluído nas duas semanas anteriores,
  o que está atrasado (separando o que realmente parou do que está aguardando terceiro),
  a carga da semana em curso e em que fase do projeto cada tarefa está. Aba Geral visual
  + uma aba detalhada por pessoa, com a lista de tarefas clicável para o ClickUp.

  Acione SEMPRE que o usuário disser: "atualiza o painel do escritório", "painel do
  escritório", "raio-x da semana", "como está a equipe", "quem está atrasado", "quanto
  cada um tem pra fazer", "carga da semana", "painel por pessoa", "dashboard do escritório".
  Também acione quando a rotina diária disparar.

  NÃO confundir com `norteador-semana` (infográfico da reunião Hands On, semanal) nem com
  `planejamento-mensal` (consolidação do mês). Este é o painel de pessoas, diário.
---

# Painel do Escritório de Projetos

Dashboard diário do Escritório de Projetos. Fonte: ClickUp. Saída: HTML publicado no
GitHub Pages.

**https://arte3-star.github.io/claude-ntics-projetos/dashboards/painel-escritorio.html**

## Como rodar

```
python ~/.claude/skills/painel-escritorio/scripts/rodar.py
```

- `--local` → coleta e monta, não publica (para conferir antes)
- `--so-build` → reaproveita o `dados.json` e só remonta o HTML (iteração de layout)

Saída em `G:\My Drive\Claude-NTICS-Projetos\tmp\painel-escritorio\`.

O script é **determinístico**: resumos por pessoa, cards de risco e rótulos de período
são todos derivados dos números. Não há texto de semana escrito à mão — o painel se
reescreve sozinho a cada rodada. Não é preciso editar nada para a rotina diária funcionar.

## O que o painel mostra

**Aba Geral** (visual, sem tabela): 4 cards de risco com número grande · colunas
proporcionais dos 7 dias da semana em curso **e da próxima** · colunas das 4 semanas ·
duas barras de fase (passivo e semana) · seção **tarefas crônicas** · seção **o que
mudou de data** · 3 donuts (taxa de entrega de cada semana anterior e quanto do passivo
está parado) · leaderboard da equipe com foto e 4 barras · bloco **fora do painel** ·
**dia planejado na sprint** · grid de cards de projeto (atrasadas grande + semana atual
e próxima nas mini-barras) · metodologia recolhida.

**Tarefas crônicas**: as que já foram empurradas **3 vezes ou mais** ou que
**escorregaram 14 dias ou mais** desde a primeira data que o painel viu. As duas medidas
existem porque o contador de vezes só cresce com o tempo, enquanto o deslocamento em
dias já é legível na primeira rodada. É o sintoma de escopo mal dimensionado ou tarefa
que ninguém quer — diferente de atraso pontual.

**Uma aba por pessoa**: foto, resumo automático, 7 indicadores, barras das 4 semanas,
situação das pendências, passivo mais antigo em dias, projetos que toca, fase do
trabalho, distribuição da semana nos 7 dias, **dia planejado na sprint**, alta/urgente
parada, e a **central de tarefas**.

**Central de tarefas** (o bloco "As tarefas, uma a uma"): cinco botões grandes no topo —
Tudo · Atrasadas · Em aberto · Em revisão · Concluídas — que **filtram a lista inteira**
ao clique, mais uma barra empilhada com a mesma leitura e seis blocos que **abrem e
fecham** (atrasadas · esta semana · próxima · empurradas · concluiu em cada semana
anterior). Abrem por padrão só *atrasadas* e *esta semana*; o resto começa recolhido,
porque tudo aberto de uma vez vira parede de texto. Cada tarefa tem borda colorida pelo
estado e link para o ClickUp.

As quatro cores são fixas e o painel é lido por elas — **não trocar sem trocar a legenda**:

| Estado | Cor | |
|---|---|---|
| Atrasada | vermelho `#c0202a` | venceu antes da segunda desta semana |
| Em aberto | azul `#2a6fb0` | com prazo à frente, não é revisão |
| Em revisão | teal `#0e6e82` | revisão ou aguardando externo, atrasada ou não |
| Concluída | verde `#1a7a46` | |

Uma atrasada **em revisão entra nos dois filtros** — clicar em "atrasadas" tem de mostrar
tudo que venceu, e clicar em "em revisão" tem de mostrar tudo que saiu das mãos da pessoa.
Por isso a soma dos botões passa do total, e o painel diz isso na tela. Já a barra
empilhada usa buckets **disjuntos** (atrasada em revisão conta como revisão, igual ao
critério de atraso real), senão a soma não fecha.

**Reagendamento**: o painel guarda o `due` de cada tarefa a cada rodada em
`historico-datas.json` e destaca o que **mudou de data em vez de ser concluído** —
na aba da pessoa, num card de risco e numa seção da Geral. Mostra também quantas vezes
a mesma tarefa já foi adiada (`3×`) e se ela já estava atrasada quando foi movida.
Sem isso o passivo cai no painel sem nada ter sido entregue e parece produtividade.

As abas têm âncora na URL (`#bellmond-viga`), então dá para mandar o link individual.
Na impressão, a barra de abas some e cada aba vira uma página.

## Janelas (móveis, calculadas a partir de hoje)

| | Período |
|---|---|
| A | duas semanas atrás (seg a dom) |
| B | semana anterior (seg a dom) |
| C | semana em curso (seg a dom) |
| D | **próxima semana** (seg a dom) |
| Atrasadas | venceram antes da segunda desta semana e continuam abertas |

**Por que D existe:** sem a próxima semana o painel tem um ponto cego. Numa sexta ou
num domingo a semana em curso já acabou, e tarefa empurrada para a semana seguinte
some da vista em vez de aparecer como trabalho que vem. Em 02/08/2026 isso ficou
explícito: 203 tarefas na semana em curso contra **466 já marcadas para a seguinte**.

Recorte: space **Escritório de Projetos `<ID_CLICKUP>`** — Projetos Ativos, Sprint do
Escritório, Diário de Campo e listas de gestão.

## Definições que o painel usa

- **Concluída**: status atual do tipo concluído E data de conclusão dentro da janela.
- **Atraso real**: atrasada que NÃO está em `revisão` nem `aguardando (externo)`. Sem
  essa separação, quem entregou e está esperando terceiro aparece como devedor.
- **Pendência**: é o conjunto das **atrasadas**, nada mais. Não somar com o que venceu na
  semana passada e segue aberto — isso é a mesma tarefa contada duas vezes, porque o que
  venceu na semana passada já venceu antes desta segunda.
- **Fase**: campo oficial `Fases do Projeto` (`e766d376-5231-4c34-9bab-9fb7d1e74c6a`),
  8 valores de Venda a Fechamento. Quando a tarefa não tem fase, o painel **sobe a cadeia
  de tarefas-mãe** até achar uma — essas aparecem com `↑`. O que sobra vira "rotina"
  (listas de gestão/sprint, que legitimamente não têm fase) ou "sem fase" (falha de
  preenchimento no ClickUp).
- **Dia planejado na sprint**: campo `🗓️ Semana` (`61eab10f-d0b2-4fde-8013-736f3d161253`),
  Segunda a Sexta + Rotina + Anual. É **o dia em que a pessoa planeja executar, não a data
  de entrega** — tarefa pode vencer sexta e estar marcada para terça. Por isso ele nunca
  substitui a distribuição por prazo: aparece ao lado dela, e o painel sempre imprime em
  quantas tarefas o campo está preenchido (hoje ~15% delas), para a leitura parcial ficar
  explícita. Some da tela quando ninguém preencheu.

## Armadilhas da API do ClickUp — já resolvidas, não "simplificar"

| Armadilha | O que acontece | Como o script trata |
|---|---|---|
| `last_page` | Volta `true` no MEIO da paginação e trunca (909 tarefas viraram 686) | Só para quando a página vem **vazia** |
| `date_closed_gt/lt` | Devolve 2.000+ tarefas, 535 delas ainda em "backlog" | Não usar. Puxar `date_updated_gt` e filtrar localmente por tipo de status + timestamp |
| `subtasks` | Sem `subtasks=true` o painel vê menos de um terço do trabalho | Sempre `true`; subtarefa de 3º nível é a maior parte do volume |
| Lista template | "Modelo de Projeto - Claude" não é trabalho real | Descartada de todas as contas |
| Publicação | `git` no Drive contamina o `.git` com `desktop.ini` | Publicar só via `gh api` |
| Histórico de datas | A API **não** devolve o `due_date` anterior de uma tarefa | `historico-datas.json` guarda o que foi visto na rodada anterior |
| Placeholder repetido | Chave repetida num `dict` é descartada em silêncio — foi assim que `__LB__` (rótulo da semana) engoliu o leaderboard por várias rodadas | A tabela de substituição é **lista de pares** com checagem de duplicata que aborta o build |
| Verificação da publicação | Comparar o arquivo baixado com ele mesmo dá "OK" mesmo servindo a versão anterior | `publicar.py` compara o **sha256 do arquivo local** com o que voltou do repo, e tenta de novo até propagar |
| Painel acima de 1 MB | A Contents API devolve `content` vazio nesse tamanho | Cai para a Git Blobs API pelo sha (o painel passou de 1 MB em 02/08/2026) |
| Pendência contada duas vezes | `atrasadas + B["abertas"]` parece "atrasadas + o que venceu semana passada", mas o que venceu na semana passada **já venceu antes desta segunda** — é o mesmo conjunto. A caixa mostrava 62 onde o ClickUp tinha 32 (03/08/2026) | Pendência é `atrasadas`, e só. `nb` serve apenas para a taxa de entrega |
| Aba velha aberta | O painel é uma foto; o ClickUp anda o dia todo. Sem carimbo visível, divergência normal parece erro | Carimbo `📸 Foto do ClickUp em <hora>` no topo, com o aviso de recarregar |

**Ressalva a manter no rodapé:** tarefa com mais de um responsável conta para cada um,
então a soma por pessoa é maior que o total do escritório.

## Estrutura

```
scripts/pull.py       ClickUp -> dados.json (janelas móveis + herança de fase + reagendamento + dia da sprint)
scripts/build.py      dados.json + template -> HTML (resumos, riscos e central de tarefas automáticos)
scripts/visual.py     componentes SVG: donut, colunas, leaderboard, cards
scripts/publicar.py   gh api PUT + verificação do que ficou no repo
scripts/rodar.py      orquestra os três
references/template.html    esqueleto com placeholders __XXX__
references/fotos-equipe.md  fotos da equipe em data URI
```

Em `tmp/painel-escritorio/` ficam também `historico-datas.json` (memória de `due_date`,
**não apagar**) e `dados-ontem.json` (snapshot da rodada anterior, usado no aviso diário).

As abas ficam em **ordem alfabética**, com "(sem responsável)" sempre por último.

## Quem entra no painel — regra fixa

**Só entra quem tem tarefa com prazo na semana em curso ou na próxima.** Aba com
contador zero não existe e não pode voltar a existir. Quem não tem nada marcado para
as duas semanas fica de fora **mesmo que carregue passivo antigo** — pessoa que saiu
da equipe, ou que só tem tarefa velha esquecida, não ocupa espaço no painel da semana.

Pedido do Lucas em 03/08/2026, depois de ver três abas marcando `0`. Não afrouxar a
regra para "tem alguma atrasada": era exatamente isso que colocava Bruna, Bruno e Yvie
no painel com uma tarefa parada desde 2025.

A exclusão **nunca é silenciosa**, em dois lugares:
- o build imprime `fora do painel (sem tarefa nesta semana nem na proxima): ... |
  atrasadas que carregam: N`;
- a Geral traz o bloco **"Fora do painel"**, com nome, foto e o que cada um ainda deve.

O passivo dessas pessoas continua contando nos totais do topo, nos cards de projeto,
nas crônicas e nas barras de fase. O que muda é só a aba.

## Dependências

ClickUp API key no `.env` do projeto · `gh` logado como `arte3-star` · `requests` e
`Pillow` no Python. O Norton derruba TLS, por isso `verify=False` nas chamadas.

## Limites

- Não escreve no ClickUp, só lê.
- O resumo por pessoa é factual e montado por regra. Julgamento editorial (o que é
  crítico, contexto de reunião) continua sendo do Lucas — o painel dá os números.
- Pessoa com mais de um e-mail/conta no ClickUp aparece duas vezes.
