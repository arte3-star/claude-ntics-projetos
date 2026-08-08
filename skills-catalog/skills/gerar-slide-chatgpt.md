---
name: gerar-slide-chatgpt
description: "Gera e refaz imagens de slide dentro de uma conversa do ChatGPT (janela real do usuário, via Playwright + Chrome CDP). Use quando o pedido for criar/ajustar slides como imagem no ChatGPT, verificando cada um por screenshot. Ex.: decks 128/129, slides de apresentação, infográficos por prompt."
user-invocable: true
---

Gera slides como **imagem** dentro de uma conversa do ChatGPT (normalmente um GPT de projeto, ex.: "Criação PPT Projeto 128/129"), dirigindo a janela real do usuário via **Playwright + Chrome CDP**. Cada slide é um prompt; o modelo devolve uma imagem; a skill **espera, recarrega, tira screenshot e você verifica** antes de seguir.

Complementa a [editar-site-web] (mesmo Chrome CDP) e segue as memórias `[[feedback_gpt_reload_imagem]]` e `[[feedback_editar_site_web_helpers]]`.

## Quando usar

- "Gera os slides X no meu ChatGPT / nesse link do ChatGPT"
- "Refaz o slide Y corrigindo Z"
- Decks montados como imagens no ChatGPT (o usuário depois monta o PPT; os slides de foto real ele faz)

## Pré-requisitos

- Chrome aberto na **porta 9222** com o perfil `browser-session`, **já logado no ChatGPT**. Se não estiver, abra como na skill editar-site-web (Passo 1) e deixe o usuário logar. **Nunca feche o Chrome** (`[[feedback_browser_automation]]`).
- `gpt_slide.py` (bundled nesta skill) é o helper. Rode com o Python do sistema.
- Se a porta 9222 falhar por versão nova do Chrome, ver `[[feedback_playwright_cdp_workaround]]`.

## Fluxo

1. **Abrir a conversa certa** (se o usuário deu um link):
   ```bash
   python gpt_slide.py open "<URL_DA_CONVERSA>" shot_open.png
   ```
   Leia `shot_open.png` e confirme que é o projeto certo (título/pasta e último slide).

2. **Escrever o prompt em arquivo** (evita problema de escape/acentos). Um arquivo `.txt` por slide.

3. **Enviar e capturar** (a imagem leva ~90-150 s; o helper já espera, dá reload e captura):
   ```bash
   python gpt_slide.py send prompt_slide.txt shot_slide.png 140
   ```
   Rode em **background** (leva minutos) e leia `shot_slide.png` quando terminar.

4. **Verificar** lendo o PNG. Confira: texto correto e com acentos, dados certos, identidade certa, sem itens proibidos. Se errado, **refaça** (passo 5). Nunca declare pronto sem ver (`[[verificar]]`).

5. **Refazer/ajustar**: mande um prompt de correção mantendo o resto:
   > `Refaça o slide "TÍTULO" corrigindo X. Mantenha todo o resto igual.`

6. **Repetir** slide a slide. Serialize: **um envio por vez** na mesma conversa (não dispare dois `send` concorrentes).

## Regras de ouro (aprendidas na prática)

- **Reload obrigatório:** depois de enviar, a imagem termina mas o DOM não atualiza sozinho (fica em "Só mais um retoque…"). O `send` já dá `page.reload()`. Sem reload, poll dá timeout falso. (`[[feedback_gpt_reload_imagem]]`)
- **Foco no omnibox:** às vezes o `#prompt-textarea` "some" porque o foco está na barra de endereço. O helper faz `bring_to_front()` + `Escape` antes de digitar. Se `send` falhar com "waiting for locator #prompt-textarea", é isso; rode de novo.
- **Slides com muito texto garble:** E4/E5/E6 (grades, turmas, cidades) o ChatGPT às vezes troca letra/acento. Sempre verifique e refaça o texto específico.
- **Prompt sempre pede:** português correto **com acentos**; e, quando aplicável, **"sem régua de marcas na base"**, **"sem tratores nem máquinas"** (Lei Rouanet). Não misture "rodapé institucional com Lei/patrocínio" e "sem régua" no mesmo prompt — isso faz o modelo desenhar uma tarja de logos. Escolha um.
- **Trocar de conversa:** `open <URL>` navega a mesma aba para outro GPT/projeto (ex.: pular do 129 para o 128).

## Colisão com o usuário (importante)

O usuário pode estar digitando **na mesma janela do ChatGPT** ao mesmo tempo. Sinais: aparece uma mensagem `role=user` que você não enviou, ou variações "2/2 · Editar". Nesse caso:

- Não fique brigando com o scroll. Use os diagnósticos de DOM em vez de screenshots às cegas:
  ```bash
  python gpt_slide.py generating   # True se há geração em curso (não envie por cima)
  python gpt_slide.py state        # papel + tem_imagem das últimas 3 mensagens
  ```
- Se `state` mostrar sua última mensagem `role=user` **sem imagem** logo depois, a geração pode ter falhado ou está pendente: espere/gere de novo, não assuma que saiu.
- Se o usuário está ativo, **pause e alinhe** antes de enviar mais prompts.

## Comandos do helper

| Comando | O que faz |
|---|---|
| `open <url> <shot>` | navega a aba para a conversa e captura |
| `send <prompt.txt> <shot> [wait]` | envia o prompt, espera `wait`s (padrão 135), reload, captura |
| `shot <shot> [reload]` | só captura (reload opcional: 1/0) |
| `state` | papel + tem_imagem das últimas 3 mensagens (JSON-ish) |
| `generating` | True/False se há geração em curso |

## Boas práticas de entrega

- Um `.txt` de prompt por slide, nomeado pelo slide (ex.: `p128_capa.txt`).
- Ao final, liste o que ficou pronto e o que falta; sinalize slides que o usuário faz sozinho (foto real).
- Guarde os prompts finais no chat para o usuário reaproveitar.
