---
name: revisao-arte-impressao
user-invocable: true
description: |
  Auditoria tecnica de arte pronta para impressao: valida CMYK, 300 dpi minimo, sangria, fontes em outline, logos vetoriais, hierarquia de marca e as regras NTICS de regua e sub-marca.

  Acione quando o usuario disser: "confere essa arte antes de mandar", "revisa o PDF da grafica", "ta pronto pra imprimir?", "valida a arte", "checa se ta em CMYK", "a grafica reclamou", "audita essa peca", "revisa antes de aprovar com o fornecedor".

  Retorna checklist pass/fail com instrucao de correcao.
---

Leia e execute o workflow completo em `workflows/marketing/revisao/revisao_arte_impressao.md`.

## Quando usar

- Antes de enviar qualquer arte impressa para gráfica
- Após execução da skill `/arte-impressao-cmyk`
- Quando receber arte finalizada da designer e precisar validar antes de aprovar com cliente
- Ao questionar uma arte já mandada à gráfica que saiu errada (diagnóstico)

## Inputs

- **Arquivo** .PDF, .AI, .EPS ou .PNG preview
- **Tipo de peça** (rollup, pantojet, wind banner, camiseta, etc.) — define regras específicas
- **Dimensões esperadas** (cm)
- **Projeto** — para validar regras contextuais (ex: tem régua MinC? qual logo soberana?)

## Output

Checklist estruturado:

### 🟢 Pass / 🔴 Fail / 🟡 Warning

| Item | Resultado | Observação |
|---|---|---|
| Espaço de cor CMYK | 🟢 Pass | — |
| DPI das imagens ≥ 300 | 🔴 Fail | Imagem logo_samarco.png está em 150 dpi |
| Sangria ≥ 3 mm | 🟢 Pass | Sangria de 5 mm detectada |
| Fontes em outline | 🟡 Warning | Montserrat Bold não convertida — converter |
| Logo patrocinador soberana | 🟢 Pass | Logo Estação Samarco em hierarquia 1 |
| Régua MinC | 🟢 Pass | Ausente (projeto não é Lei de Incentivo) |

Lista de correções necessárias antes do envio à gráfica.

## Ferramentas

| Ferramenta | Arquivo | Função |
|---|---|---|
| Validador PDF | `tools/adobe/revisao_arte_pdf.py` | PyMuPDF + ReportLab: checa CMYK, DPI, sangria, fontes |
| Validador AI | `tools/adobe/revisao_arte_ai.py` | Illustrator COM: inspeciona camadas, cores, fontes |

## Regras NTICS padrão (aplicadas por default)

- **CMYK obrigatório** — se for RGB, 🔴 Fail
- **Sangria 3 mm mínima** · 5 mm para pantojet/backdrop
- **DPI ≥ 300** em imagens raster embedadas
- **Fontes em outline** no PDF final
- **Logos vetoriais** — se tiver PNG/JPG como logo, 🔴 Fail
- **Contexto do projeto** (via task-mãe ClickUp):
  - Lei de Incentivo → régua MinC obrigatória
  - Corporativo → sem régua MinC
  - Samarco → logo Estação Samarco soberana + logo Samarco corporativa como "apresenta"

## Fluxo

1. Receber arquivo
2. Rodar `tools/adobe/revisao_arte_pdf.py` ou `_ai.py`
3. Comparar com regras do projeto (cruzar com TAP no SecondBrain se disponível)
4. Gerar relatório pass/fail
5. Se 🔴 Fail em algum item crítico: bloquear envio, retornar lista de correções
6. Se 🟡 Warning: alertar mas permitir envio com aprovação do usuário
7. Se tudo 🟢 Pass: liberar envio à gráfica
