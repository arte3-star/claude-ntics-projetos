---
name: revisao-carrossel
user-invocable: true
description: |
  Revisa visualmente os cards de qualquer carrossel NTICS: texto, cores, logo e layout, sinalizando problema com sugestao de correcao.

  Acione quando o usuario disser: "revisa o carrossel", "confere os cards", "ta bom esse carrossel?", "olha se ficou certo", "valida antes de postar", "tem erro nesses cards?", "revisa antes de mandar pro cliente".
---

Leia e execute o workflow completo em `workflows/marketing/producao/carrosseis/revisao-carrossel.md`.

## Inputs

**Obrigatórios:**
- `pasta` — caminho dos cards a revisar (ex: `output/marketing/carrosseis/educacional/5-sinais/`)
- `tipo` — tipo de carrossel: `educativo`, `case` ou `noticias`

**Opcionais:**
- `regenerar` — se `true`, dispara o script de correção para achados bloqueantes (🔴)

## Ferramentas

| Tool | Uso |
|------|-----|
| `Read` (imagem) | Inspecionar visualmente cada card |
| `brand-book/data/brand-data.yaml` | Conferir dados numéricos da NTICS |
| `brand-book/02-identidade-verbal/tom-de-voz.md` | Calibrar tom editorial |
| `tools/content-gen/regen_educativo_bg_test.py` | Corrigir cards educativos (logo CTA, fundo foto) |

## Fluxo

1. Carregar referências de marca e feedback memories de revisão
2. Ler todos os cards da pasta via Read (imagem)
3. Aplicar checklist universal + específico do tipo
4. Reportar achados com gravidade 🔴🟡🟢
5. Se `regenerar=true` e achados 🔴: disparar correção
6. Salvar relatório em `output/.../revisao-{data}.md`
