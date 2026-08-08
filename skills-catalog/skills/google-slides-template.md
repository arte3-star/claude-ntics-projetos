---
name: google-slides-template
user-invocable: true
description: |
  Cria template editavel em Google Slides com placeholders nomeados ({CIDADE}, {TRILHA}, {DATA}, {NOME}) a partir de brief estruturado, e exporta PNG de exemplo preenchido.

  Acione quando o usuario disser: "template de slides", "peca com campo variavel", "convite por cidade", "card de inscricao editavel", "certificado editavel", "a equipe vai reaproveitar essa peca", "deixa editavel pro time preencher", "modelo pra trocar so o nome/cidade".

  Ideal quando a peca vai ser reaproveitada pela equipe trocando campos. Para deck de apresentacao, use gerar-slide-chatgpt.
---

Leia e execute o workflow completo em `workflows/marketing/producao/google_slides_template.md`.

## Quando usar

- Convite por cidade (feed, WhatsApp, story)
- Card de inscrição com QR
- Certificado digital (A4, A5, carta)
- Qualquer peça que a equipe NTICS ou cliente vai preencher com dados diferentes dezenas de vezes

## Inputs

- **Tipo de peça** (`convite-cidade`, `card-qr`, `certificado-trilha`, `certificado-participacao`, `custom`)
- **Dimensões** do slide (padrão: feed 1080×1350 px, story 1080×1920 px, certificado A5 154×216 mm)
- **Paleta + tipografia** do KV do projeto (pode vir do folder KV no Drive)
- **Placeholders** — lista de campos editáveis com limite de caracteres
- **Exemplo preenchido** (opcional, para gerar PNG de preview)
- **Pasta Drive destino** (onde o Google Slides + PNG vão ser salvos)

## Output

- 1 Google Slides editável com placeholders nomeados no formato `{CAMPO}`
- 1 PNG exportado (exemplo preenchido) — 300 dpi
- Link direto do Slides na pasta Drive do projeto
- Comentário na task ClickUp (se integrado) com os 2 links

## Ferramentas

| Ferramenta | Arquivo | Função |
|---|---|---|
| Criador Slides | `tools/gws/slides_template_create.py` | Cria Slides via API com placeholders + export PNG |
| Auth Workspace | `tools/gws/auth.py` (existente) | OAuth Google Slides API scope |
