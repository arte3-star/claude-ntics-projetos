# Rotina semanal de Noticias ESG — setup pendente

A rotina agendada de sabado (agente semanal de Noticias ESG) nao pode ser
executada porque a infraestrutura esperada nao existe neste repositorio.

## O que faltou (verificado em HEAD, origin/master e todo o historico git)

1. **`tools/content-gen/noticias_clickup_map.yaml`** — mapa que associa cada
   `semana_inicio` (segunda-feira) aos campos `numero`, `carrossel_task_id` e
   `artigo_task_id`. Sem ele, o agente nao sabe em quais tasks do ClickUp postar.
2. **`workflows/marketing/producao/carrosseis/carrossel_noticias.md`** — workflow
   completo referenciado pela skill `carrossel-noticias`.
3. **`workflows/marketing/producao/carrosseis/carrossel_noticias_canva.md`** —
   padrao completo do carrossel no Canva (Passo 7).

Nenhum arquivo `.yaml`/`.yml` esta rastreado no repositorio.

## Por que a execucao foi encerrada

O Passo 2 da rotina determina: "Se nao existir, registre erro e encerre."
Como o mapa nao existe, nao ha como obter `carrossel_task_id` e `artigo_task_id`
para a semana de 2026-10-05 (05/10 a 11/10/2026). O Passo 6 (postagem garantida
no ClickUp) e o unico entregavel obrigatorio e depende desses IDs; o Passo 7
(Canva) depende do Passo 6. Postar em uma task adivinhada violaria a regra
"nunca inventar" e poderia atingir a task errada, por isso nada foi postado.

## Como habilitar a rotina

Criar o arquivo `tools/content-gen/noticias_clickup_map.yaml` com entradas por semana, por exemplo:

```yaml
- semana_inicio: "2026-10-05"
  numero: 1
  carrossel_task_id: "<id da task de carrossel no ClickUp>"
  artigo_task_id: "<id da task de artigo no ClickUp>"
```

e adicionar os workflows citados acima. Depois disso, a execucao de sabado
seguira normalmente: pesquisa (ultimos 7 dias), curadoria de 9 noticias,
montagem do documento, postagem nas duas tasks e, best-effort, o carrossel no Canva.
