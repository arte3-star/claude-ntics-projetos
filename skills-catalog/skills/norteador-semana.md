---
name: norteador-semana
description: |
  Gera o infográfico semanal "Clareza da Semana" da NTICS Projetos — o norteador visual que orienta a reunião Hands On toda semana. Substitui completamente o GPT e o Canva: puxa os dados do ClickUp, classifica os projetos nos blocos certos, monta o quadro de execuções em campo via etiqueta 📍execução, e entrega um HTML pronto para abrir no navegador e exportar.

  Acione SEMPRE que o usuário disser: "gera o norteador", "norteador da semana de X a Y", "clareza da semana", "monta o infográfico da semana", "prepara o hands on", ou qualquer variação de geração do relatório semanal de projetos. Também acione se o usuário mencionar "atualiza o norteador", "ajusta o norteador", "refaz o norteador".

  Este é o artefato mais importante da semana operacional do Abilio — use esta skill proativamente sempre que o contexto envolver a reunião semanal de alinhamento ou o resumo do portfólio para a equipe.
---

# Norteador da Semana — NTICS Projetos

Você gera o infográfico "Clareza da Semana" — um HTML visual que orienta a reunião Hands On semanal. A fonte de dados é o ClickUp. O output é um arquivo HTML idêntico ao modelo aprovado pelo Abilio.

## Princípios

1. **Nunca inventar informação.** Se não está no ClickUp ou foi dito pelo Abilio, não entra.
2. **Clareza sobre completude.** Se não conseguiu ler algum projeto, diz qual e por quê — nunca finge que cobriu tudo.
3. **Julgamento editorial é do Abilio.** A classificação automática por Fase já resolve 80%. Os 20% restantes (o que é crítico essa semana, contexto de reunião, decisões informais) precisam vir do Abilio. Sempre perguntar antes de gerar.
4. **Estrutura imutável.** O layout HTML, as seções e a ordem dos blocos são fixos — definidos nesta skill. Só o conteúdo muda.

> **Ordem das seções de projeto (definida pelo Lucas em 02/08/2026 — não alterar):**
> **1) Projetos em Execução → 2) Projetos em Planejamento → 3) Projetos com Ações Iniciais → 4) Projetos em Finalização.**
> A lógica é do mais quente para o mais frio: o que está em campo agora, depois o que está sendo preparado, depois o que está nascendo, e por último o que está encerrando.

---

## Tabela de Coordenadores (referência fixa — atualizar quando Abilio sinalizar mudança)

| Projeto | Coordenador |
|---------|-------------|
| #74 Global Goals (Áster Máquinas) | Jéssica Lora |
| #115 Cultura Robótica 2ED | Raíza Araújo |
| #116 Cultura Robótica (Áster) | Raíza Araújo / Mayara |
| #117 Teatro Whirlpool | Raíza Araújo |
| #119 PEC Sylvamo | Raíza Araújo |
| #120 Negócio Cultural 2ED (Statkraft + Itapoá) | Bruna Seibel |
| #121 Negócio Cultural 3ED (TAG) | Abilio / Jeferson |
| #122 Cultura Itinerante ODS (Repsol) | Bellmond Viga |
| #124 Gastronomia COMPAGAS | Mayara Ferreira |
| #125 Gastronomia GRU | Jéssica Lora |
| #126 Ecoarte Container GRU | Jéssica Lora |
| #127 PIE GRU + Sotreq | Jéssica Lora |
| #128 Festival Agricultura CNH | Raíza Araújo |
| #129 Agrofuturo CNH | Raíza Araújo |
| #132 Estação Samarco | Lucas Rotta |
| #133 Ecoarte Vibra | Bellmond Viga |

> Se Abilio sinalizar coordenador diferente do desta tabela durante a conversa, usar o que ele sinalizou e atualizar a tabela na skill.
>
> **Correção aplicada em 19/07/2026** (fonte: `reference_norteador-skill.md` do CLAUDE BRAIN, nota de 13/07/2026, não estava refletida na cópia da skill em uso): #74 e #126 corrigidos para Jéssica Lora, #115 corrigido para Raíza Araújo. Nota do Abilio sobre o #115: a responsabilidade ainda precisa ser ajustada no próprio ClickUp — o card deve sinalizar essa pendência até lá.

---

## Passo 0 — Coletar inputs do Abilio (OBRIGATÓRIO antes de qualquer chamada ao ClickUp)

Perguntar numa única mensagem, de forma curta:

```
Para gerar o norteador de [datas], preciso de 3 informações rápidas:
1. Foco comportamental da semana (3 bullets)
2. Algo novo esta semana que não está no ClickUp?
3. Algo que entra "na próxima semana" e deve aparecer no bloco de avisos?
```

Se o Abilio já tiver passado essas informações na mensagem de pedido, não perguntar de novo.

---

## Passo 1 — Puxar dados do ClickUp (4 buscas focadas, nesta ordem)

### REGRA CRÍTICA: conversão de timestamps
**NUNCA converter timestamp manualmente.** Sempre usar python:
```python
import datetime
datetime.datetime.fromtimestamp(timestamp_ms / 1000).strftime("%d/%m/%Y (%A)")
```
Erros de conversão manual contaminam o quadro de campo e a agenda do mês.

---

### Busca 1 — Tarefas em ATRASO (vencidas antes de hoje)

Rodar em DUAS chamadas separadas (uma para os projetos operacionais, outra para Inscrição) e manter a origem marcada — a origem decide o roteamento no Passo 2/3.

**1a — Projetos operacionais (folder Projetos Ativos):**
```
clickup_filter_tasks(
  folder_ids=["<ID_CLICKUP>"],
  due_date_to=<hoje>,
  include_closed=false,
  subtasks=true,
  order_by=due_date
)
```
**1b — Inscrição de Projetos (space Inscrição):**
```
clickup_filter_tasks(
  space_ids=["<ID_CLICKUP>"],
  due_date_to=<hoje>,
  include_closed=false,
  subtasks=true,
  order_by=due_date
)
```
Resultado 1a: tarefas vencidas por projeto → cards de projeto com badge ⚠️ em vermelho.
Resultado 1b: tarefas vencidas de Inscrição → alimentam SÓ o card "📝 Inscrição de Projetos" nas Áreas de Apoio (ver Passo 3). **Nunca misturar com os cards de projeto.**
**Não buscar lista por lista — uma busca por folder e uma por space capturam tudo.**

---

### Busca 2 — Tarefas DA SEMANA (seg a dom da semana corrente)

Também em DUAS chamadas separadas, mantendo a origem marcada.

**2a — Projetos operacionais (folder Projetos Ativos):**
```
clickup_filter_tasks(
  folder_ids=["<ID_CLICKUP>"],
  due_date_from=<segunda>,
  due_date_to=<domingo>,
  include_closed=false,
  subtasks=true,
  order_by=due_date
)
```
**2b — Inscrição de Projetos (space Inscrição):**
```
clickup_filter_tasks(
  space_ids=["<ID_CLICKUP>"],
  due_date_from=<segunda>,
  due_date_to=<domingo>,
  include_closed=false,
  subtasks=true,
  order_by=due_date
)
```
Resultado 2a: tarefas com prazo nesta semana → bullets normais dos cards de projeto.
Resultado 2b: atividades da semana de Inscrição → detalhadas por dia no card "📝 Inscrição de Projetos" (Passo 3). **Nunca entram no grid de projetos.**
**Não buscar sem filtro de data — gera ruído e consome tokens desnecessariamente.**

---

### Busca 3 — Execuções em campo (tag 📍execução, apenas esta semana)
```
clickup_filter_tasks(
  folder_ids=["<ID_CLICKUP>"],
  tags=["📍execução"],
  due_date_from=<segunda>,
  due_date_to=<domingo>,
  include_closed=false,
  subtasks=true,
  order_by=due_date
)
```
Converter cada `due_date` via python antes de alocar no dia da semana.
Badges adicionais: `nticsemcampo` → badge roxo; `captação em campo` → badge teal.
**Nunca alocar tarefa em dia sem converter o timestamp.**

---

### Busca 4 — Agenda do mês (tags de marcos, mês inteiro)
```
clickup_filter_tasks(
  folder_ids=["<ID_CLICKUP>"],
  tags=["ki - kick off interno", "kc - kick off cliente", "mockup / termo de abertura"],
  due_date_from=<primeiro do mês>,
  due_date_to=<último do mês>,
  include_closed=false,
  order_by=due_date
)
```
**Tags exatas — não usar variações.** Os nomes corretos no ClickUp são:
- `ki - kick off interno`
- `kc - kick off cliente`
- `mockup / termo de abertura`

Converter cada `due_date` via python. Exibir no bloco 4 do header "Agenda do Mês — [Mês]".

---

## Passo 2 — Classificar projetos nos blocos

**REGRA DE ROTEAMENTO POR ORIGEM (antes de classificar):**
Todo resultado da origem Inscrição (space `<ID_CLICKUP>` — Buscas 1b e 2b) NÃO entra na classificação de projetos abaixo e NÃO gera card no grid (Execução, Finalização, Planejamento etc.). Vai exclusivamente para o card "📝 Inscrição de Projetos" nas Áreas de Apoio (montado no Passo 3b). Só os resultados do folder `<ID_CLICKUP>` (Buscas 1a e 2a) passam pela tabela abaixo.

Aplicar a tabela abaixo. Em caso de dúvida, sinalizar para o Abilio — nunca chutar.

| Fase no ClickUp | Bloco no norteador |
|---|---|
| Execução + ação de campo na semana com urgência | **Crítico** |
| Execução + campo ativo sem urgência especial | **Em Execução** |
| Fechamento + ainda tem campo ativo | **Em Execução** |
| Kick-off / Planejamento | **Planejamento** |
| Fechamento sem campo ativo | **Finalização** |
| Próxima etapa ainda não iniciada | **Planejamento Próximas Etapas** |
| Visão de mês seguinte | **Planejamento Próximo Mês** |

**Regra de crítico:** projeto com tarefa vencida urgente (⚠️), problema sinalizado pelo Abilio, ou execução que trava outra coisa → Crítico, independente da Fase.

---

## Passo 3 — Montar bullets de cada projeto

Apenas resultados operacionais (Buscas 1a e 2a — folder `<ID_CLICKUP>`). Inscrição é tratada no Passo 3b.
Para cada projeto, sintetizar em 3-5 bullets:
- **Tarefas em atraso (Busca 1a):** aparecem primeiro, em vermelho com prefixo ⚠️
- **Tarefas da semana (Busca 2a):** bullets normais
- Não listar tarefas palavra por palavra — sintetizar o que precisa acontecer
- Datas de execução NÃO entram nos cards — já aparecem no quadro de campo
- **Coordenador:** usar a tabela de coordenadores fixos acima. Se Abilio sinalizou diferente na conversa, prevalecer o que ele disse.

---

## Passo 3b — Montar o card "📝 Inscrição de Projetos" (Áreas de Apoio)

Alimentado SÓ pelas Buscas 1b e 2b (space `<ID_CLICKUP>`). Fica no bloco Áreas de Apoio — nunca no grid de projetos.

O space de Inscrição empilha muitos vencidos (20+ por semana). Sem compressão o card estoura. Aplicar esta regra:

**1. Vencidos ANTIGOS (mais de 7 dias — `due_date` < hoje − 7):**
Agrupar TODOS num único bullet `late`, com contagem e responsáveis. Nunca listar um a um.
Formato: `<li class="late">N itens vencidos (DD/MM a DD/MM): resumo curto do que são · Resp1 / Resp2</li>`
- `N` = quantidade agrupada
- datas = menor e maior `due_date` do grupo (converter via python — nunca manual)
- resumo = 1 frase do tipo de pendência (ex: "rendimentos captados, propostas e auditorias")
- responsáveis = assignees distintos do grupo, separados por " / "

**2. Vencidos da SEMANA ATUAL (0 a 7 dias — `due_date` >= hoje − 7 e < hoje):**
Detalhar individualmente, um bullet `late` por item, com data e responsável.

**3. Atividades da SEMANA (Busca 2b — prazo seg a dom):**
Detalhar individualmente por dia, um bullet normal por item.
Formato: `<li>DD/MM: descrição da atividade · Responsável</li>`

Ordenar: bullet de vencidos antigos agrupado primeiro, depois vencidos da semana, depois as atividades por data crescente.
Referência de layout deste card: ver o exemplo aprovado no `index.html` do GitHub (bloco `sup-card` "📝 Inscrição de Projetos").

---

## Passo 4 — Montar o quadro de execuções em campo

Organizar as tarefas da Busca 3 por dia (Segunda a Domingo — o norteador cobre 7 dias).
**Sempre Segunda a Domingo — não Segunda a Sábado.**

Para cada tarefa:
- Projeto (número + nome curto)
- Nome da tarefa (escola, local, ação)
- Responsável (assignee)
- Badges conforme tags

Se um dia não tiver execução tagueada → "Sem execução tagueada" em cinza.

**Regra crítica:** nunca limpar um dia inteiro durante edições. Sempre editar tarefa a tarefa.
Se aparecer execução de praça já encerrada → sinalizar para Abilio remover a etiqueta da tarefa.

---

## Passo 5 — Bloco 4 do Header: "Agenda do Mês — [Mês]"

Usar os resultados da Busca 4. Exibir apenas:
- `ki - kick off interno` → KI — Kickoff Interno
- `kc - kick off cliente` → KC — Kickoff Cliente
- `mockup / termo de abertura` → Mockup / Termo Abertura

Formato de cada linha: `DD/MM — #NNN Nome curto | Tipo | Responsável`
Ordenar por data crescente.
**Não incluir nenhum item que não tenha uma dessas 3 tags — tarefas de fase "📌 FASE:" não entram aqui.**

---

## Passo 6 — Gerar o HTML

**Layout = o aprovado que está no GitHub.** Sempre buscar a estrutura mais recente do repositório `arte3-star/claude-ntics-projetos` (pasta `dashboards/norteador/`), nunca de memória nem de um template local que pode estar desatualizado:
```
https://raw.githubusercontent.com/arte3-star/claude-ntics-projetos/master/dashboards/norteador/index.html
```
Baixar esse `index.html`, usá-lo como esqueleto (CSS + ordem de blocos + estrutura dos `sup-card`, incluindo o card "📝 Inscrição de Projetos") e só trocar o conteúdo pelos dados da semana. Se o download falhar (sem rede), usar `references/template.md` como fallback offline e avisar o Abilio que usou a cópia local.

Preencher:
- Datas da semana no header e título
- Bloco 1: Foco comportamental (vem do Abilio — Passo 0)
- Bloco 2: Principais Atenções (projetos críticos e urgências da semana)
- Bloco 3: (semana/datas)
- Bloco 4: Agenda do Mês (Busca 4)
- Cards de cada projeto nos blocos corretos, com ⚠️ para atrasados, nesta ordem de seções: **Execução → Planejamento → Ações Iniciais → Finalização**
- Quadro de campo Segunda–Domingo (Busca 3)
- Áreas de Apoio e Gestão (conteúdo fixo — ver `references/areas-fixas.md`), EXCETO o card "📝 Inscrição de Projetos", que é dinâmico e vem do Passo 3b
- Novidades (vem do Abilio — Passo 0)
- Bloco "Próxima Semana" (vem do Abilio — Passo 0)
- Principais Ações (4 colunas): sintetizar a partir dos projetos

Salvar em `/mnt/user-data/outputs/norteador-[dd-dd]-[mes].html`

---

## Passo 7 — Apresentar e iterar

Entregar o arquivo via `present_files`. Informar ao Abilio:
- Quais projetos foram classificados automaticamente
- Quais precisam de confirmação (casos ambíguos, Fase não preenchida)
- Projetos com tarefas em atraso identificadas (⚠️)
- Se houve leitura parcial

Aguardar ajustes. Aplicar com `str_replace` cirúrgico — **nunca reescrever o arquivo inteiro a cada ajuste pequeno.**
**Nunca limpar um bloco ou dia inteiro para corrigir um item — editar só o item afetado.**

---

## Erros conhecidos a evitar (aprendidos em produção)

| Erro | Como evitar |
|------|-------------|
| Converter timestamp manualmente e errar o dia | Sempre usar python datetime |
| Assumir coordenador pelo contexto | Usar tabela fixa acima; prevalece o que Abilio disse na conversa |
| Classificar fase errada por inferência | Usar Busca 1+2 filtradas; dúvida → perguntar ao Abilio |
| Buscar todas as tarefas sem filtro de data | Sempre filtrar: atraso = `due_date_to=hoje`; semana = `due_date_from/to` da semana |
| Limpar dia inteiro no quadro de campo | Editar tarefa a tarefa, nunca o dia todo |
| Usar tags com nomes aproximados | Usar nomes exatos: `ki - kick off interno`, `kc - kick off cliente`, `mockup / termo de abertura` |
| Ler template de memória | Sempre ler `references/template.md` integralmente antes de gerar |
| Omitir tarefa que existia na busca inicial | Antes de remover qualquer item, verificar se havia outras tarefas no mesmo dia/bloco |
| Jogar tarefa de Inscrição no grid de projetos | Origem space `<ID_CLICKUP>` (Buscas 1b/2b) → só o card "📝 Inscrição de Projetos", nunca card de projeto |
| Listar 20+ vencidos de Inscrição um a um | Comprimir vencidos > 7 dias num único item com contagem + responsáveis (Passo 3b) |
| Gerar o HTML de um template de memória/local desatualizado | Baixar o layout aprovado do GitHub (`arte3-star/claude-ntics-projetos/dashboards/norteador/index.html`) a cada geração |

---

## Limites desta skill

- Não gera o infográfico como imagem — só HTML (exportar via Ctrl+P no navegador)
- Não atualiza o ClickUp — só lê
- Não inventa bullets sem base em tarefa ou input do Abilio
- Não decide sozinha o que é "crítico" quando a Fase não é conclusiva — pergunta

## Referências

- **Layout aprovado (fonte da verdade):** `https://raw.githubusercontent.com/arte3-star/claude-ntics-projetos/master/dashboards/norteador/index.html` — baixar a cada geração (Passo 6)
- `references/template.md` — espelho offline do layout do GitHub (fallback apenas se o download falhar)
- `references/areas-fixas.md` — Conteúdo fixo das Áreas de Apoio e Gestão (o card "📝 Inscrição de Projetos" é dinâmico — Passo 3b)
- `references/field-ids.md` — IDs dos campos personalizados do ClickUp
