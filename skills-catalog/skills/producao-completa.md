---
name: producao-completa
user-invocable: true
description: |
  Pipeline completo em duas etapas: o Time de Design produz os assets visuais, depois o Time de Midias Sociais produz a copy e distribui.

  Acione quando o usuario disser: "producao completa", "do zero ao publicado", "faz tudo: arte e copy", "pipeline completo do projeto", "assets + distribuicao".
---

Este skill orquestra dois Agent Teams em sequencia:

## Etapa 1: Time de Design
Monte o Agent Team de design conforme a skill `time-design` (o workflow
`workflows/marketing/team_design_content.md` nao existe; a skill e a fonte).
Aguarde a entrega dos assets em `.tmp/entrega/`.

## Etapa 2: Time de Midias Sociais
Apos a entrega dos assets, monte o Agent Team de midias sociais conforme a skill
`time-social` (o workflow `workflows/marketing/team_social_media.md` nao existe).
Os assets do Time de Design em `.tmp/entrega/` sao o input do Time de Midias Sociais.

## Pipeline
```
/time-design (assets visuais)
  └──> .tmp/entrega/
        └──> /time-social (copy + distribuicao)
              ├──> Gmail draft (newsletter)
              ├──> ClickUp tasks (publicacoes)
              └──> .tmp/publicacao/ (pacotes por plataforma)
```

Pergunte ao usuario:
1. Qual projeto/tema?
2. Quais tipos de assets visuais precisa? (carrossel, apresentacao, motion)
3. Quais plataformas de distribuicao? (Instagram, LinkedIn, newsletter)
4. Quais inputs tem disponiveis? (relatorio, fotos, template .aep)
