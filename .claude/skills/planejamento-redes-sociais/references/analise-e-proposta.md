# Análise e proposta de pauta

## Parte A — Análise do período

A partir dos itens normalizados (Passo 3) e separados por período (Passo 4), produza:

### KPIs do período passado
- **Nº de posts publicados** (carrossel + vídeo), total e por tipo.
- **Nº de vídeos editados** (tarefas de edição concluídas).
- **Por projeto:** quais **postaram** e quantos posts cada um; quais ficaram **silenciosos** (nenhum
  post no período) — sinalizar, é a base para a proposta.
- **Por pessoa:**
  - vídeos editados por cada um (Marcos, Aline, etc.);
  - posts feitos por cada um (Aline e quem mais publicar);
  - carrosséis por designer (Marina, Alison, +1).
- **Institucional:** quantos carrosséis institucionais (ESG / projetos / notícia) saíram.

### Panorama do próximo período
- Itens **previstos** por dia/semana.
- **Com data fechada com cliente** × **sem data fechada** (usar a tag). O que não tem data fechada é
  material flexível para preencher lacunas.
- **Backlog sem data** — bolsa de itens candidatos a agendar.

## Parte B — Proposta de pauta (≥ 1 vídeo por dia útil)

Objetivo: garantir **pelo menos 1 post de vídeo em cada dia útil** do próximo período.

1. **Grade de dias úteis** do próximo período (seg–sex; ajuste se o cliente publicar em fins de semana).
2. **Alocar o que já existe:** posicione os vídeos já planejados (com data) nos seus dias. Prioridade
   para itens com **data fechada com cliente** — esses são fixos e não se movem.
3. **Identificar lacunas:** dias úteis sem nenhum vídeo.
4. **Preencher com cortes/melhores momentos** dos **projetos em finalização**:
   - cada corte vira uma subtarefa de edição **atribuída à Aline**;
   - alocar 1 corte por dia-lacuna, escolhendo projetos em finalização com material disponível;
   - equilibrar entre projetos (não concentrar tudo em um só) quando possível.
5. **Restrição da Aline — no máximo 1 vídeo para editar por dia:**
   - montar a carga diária da Aline = (edições já atribuídas a ela naquele dia) + (cortes propostos);
   - **nunca** exceder 1 por dia. Se um dia já tem edição da Aline, não proponha corte para ele —
     empurre para o próximo dia livre dela.
   - se não houver dias suficientes para cobrir todas as lacunas dentro do limite, **priorize** os
     dias úteis mais próximos e **liste as lacunas remanescentes** como pendência (não estoure o limite).

## Parte C — Rascunho de criação no ClickUp (para aprovação)

Entregue uma tabela pronta — **não crie nada ainda**:

| Dia | Projeto | Subtarefa (nome sugerido) | Lista | Tarefa-pai | Responsável | Tipo |
|-----|---------|---------------------------|-------|------------|-------------|------|
| seg 07/07 | <projeto> | Editar corte — melhores momentos <projeto> | <lista redes> | Acompanhar redes sociais | Aline | edição |

- Nome sugerido consistente (ex.: `Editar corte — melhores momentos <projeto>`).
- **Tarefa-pai** = "Acompanhar redes sociais" do projeto de origem.
- Confirme o limite de 1/dia para a Aline **na própria tabela** (uma linha por dia no máximo p/ ela).
- Só após o "ok" do usuário, criar via `clickup_create_task` (subtarefa do pai, assignee = Aline,
  due date = o dia alocado).

## Regras de bom senso
- Itens com **data fechada com cliente** são intocáveis: nunca sobrescrever nem realocar.
- Se faltar informação (status ambíguo, projeto sem material), **sinalize como pendência** em vez de
  assumir. O relatório sempre tem um bloco de "pendências / a confirmar".
