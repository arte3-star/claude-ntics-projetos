---
name: design-briefing
user-invocable: true
description: |
  Gate de aprovacao antes de qualquer geracao de imagem: confirma modelo, tamanho, tom e estrutura com o usuario, e traz 1-2 ideias proprias como seed para co-criar.

  Acione ANTES de gerar qualquer imagem, capa, card ou arte quando o pedido vier vago ("faz uma arte", "cria uma imagem", "monta um card") sem definir formato, tom ou estrutura.

  Se o pedido ja vier completo e explicito, siga direto sem o gate.
---

## Quando usar

Invoque `/design-briefing` **antes** de qualquer chamada à Leonardo AI ou geração em lote de imagens. Skills como `/carrossel-educativo`, `/carrossel-noticias`, `/carrossel-cliente` e `/carrossel-caso` devem passar por este gate obrigatoriamente.

**Regra:** Nenhuma imagem gerada sem aprovação explícita dos parâmetros de design.

---

## Protocolo

### Passo 1 — Coletar contexto disponível
Antes de perguntar, leia o que já existe:
- Briefing ou task do ClickUp (tema, cliente, objetivo)
- `brand-book/data/brand-data.yaml` (cores, logo, tom)
- Histórico de carrosseis anteriores similares (se existir em `output/marketing/`)

### Passo 2 — Apresentar proposta de parâmetros
Mostre ao usuário uma proposta curta e objetiva:

```
PROPOSTA DE DESIGN — [Nome do carrossel]

Modelo Leonardo:  [modelo proposto]
Estilo visual:    [ex: realista, flat, corporativo]
Paleta:           [cores principais]
Formato cards:    [ex: 1080x1080, 1080x1350]
Tom do texto:     [ex: educativo, inspiracional, técnico]
Estrutura copy:   [ex: título + 3 bullets + CTA]
Referência:       [ex: similar ao carrossel ODS semana 12]

Aprova ou ajusta?
```

### Passo 3 — Aguardar aprovação
**Não execute geração até receber confirmação explícita.**
Aceitar respostas como:
- "Aprova" / "Ok" / "Pode ir"
- Ajustes pontuais ("muda o modelo para X")

### Passo 4 — Documentar parâmetros aprovados
Antes de executar, registre os parâmetros aprovados em um comentário ou log local:
```
# Design aprovado em [data]
# Modelo: X | Estilo: Y | Paleta: Z | Formato: WxH
```

### Passo 5 — Executar com parâmetros confirmados
Execute o pipeline de geração usando exatamente os parâmetros aprovados. Não altere modelo ou estilo durante a execução.

---

## Casos que NÃO precisam deste gate

- Revisão ou correção de carrossel já gerado (`/revisao-carrossel`)
- Geração de texto/copy sem imagens
- Re-run de pipeline com parâmetros idênticos ao último aprovado (documente que está reutilizando)

---

## Após geração

Execute `/verificar` ou `/revisao-carrossel` antes de reportar conclusão.
