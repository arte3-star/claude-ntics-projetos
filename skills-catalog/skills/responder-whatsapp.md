---
name: responder-whatsapp
description: Ler e responder mensagens no WhatsApp Web via Chrome (CDP). Use quando o usuário pedir para ver mensagens recebidas, responder contatos, checar não lidas, ou disparar mensagens/avisos pelo WhatsApp. Cobre leitura de conversas, detecção de mensagens recebidas e envio confiável de respostas (texto). Não fecha o Chrome.
---

# Responder WhatsApp (CDP)

Skill para **ler e responder** mensagens no WhatsApp Web automatizando o Chrome via Chrome DevTools Protocol (CDP). Toda a lógica testada está em `wa_cdp.py` (mesma pasta).

## Quando usar
- "Veja o que fulano respondeu / o que chegou no WhatsApp"
- "Responda essas pessoas", "manda esse aviso", "checa as não lidas"
- Atendimento/cobrança/engajamento por WhatsApp em qualquer projeto.

Para projetos específicos, combine com o workflow do projeto (ex.: `workflows/inscricao-projetos/132-estacao-samarco-responder-whatsapp.md`), que traz contexto e respostas-padrão.

## Pré-requisitos (verificar SEMPRE antes)
1. Chrome aberto com porta de debug num **perfil DEDICADO** (não o perfil padrão):
   ```powershell
   & "C:\Program Files\Google\Chrome\Application\chrome.exe" `
     --remote-debugging-port=9222 --remote-allow-origins=* `
     --user-data-dir="C:\Users\lucas\wa-chrome-auto" `
     --no-first-run --no-default-browser-check "https://web.whatsapp.com"
   ```
   ⚠️ Use um `--user-data-dir` LOCAL (fora do Google Drive). Perfil dentro do G:\ (Drive) é sincronizado e **corrompe a sessão / derruba a porta 9222** repetidamente. `C:\Users\lucas\wa-chrome-auto` é estável.
   Checar vivo: `curl -s --max-time 5 http://127.0.0.1:9222/json/version` (se cair, relançar).
   - ⚠️ **Chrome 136+ IGNORA `--remote-debugging-port` quando o `--user-data-dir` é o perfil PADRÃO** ("...\Chrome\User Data"). Por isso o comando antigo (Profile 29 no dir padrão) parou de subir a porta 9222 após update do Chrome (v150). Use SEMPRE o dir dedicado acima — desacopla do Chrome normal do usuário e não quebra em updates.
   - Primeira vez nesse perfil: aparece o **QR** — capturar screenshot (via CDP `Page.captureScreenshot`) e pedir para o usuário parear (WhatsApp > Aparelhos conectados). Depois a sessão persiste (`Manter sessão iniciada`).
2. **NUNCA feche o Chrome** durante a automação a menos que o usuário peça (`feedback_browser_automation`). Se a porta caiu e o perfil está preso, peça autorização antes de fechar/reabrir.
3. Rodar o Python pela pasta de scripts do projeto quando precisar gravar saída (`G:\My Drive\Claude-NTICS-Projetos\tmp\`), por causa do Norton (`feedback_scripts_tmp_dir`).
4. `print` de acentos/emojis no Windows quebra (cp1252); o `wa_cdp.py` já faz `sys.stdout.reconfigure(utf-8)`.

## Uso (CLI)
```bash
# Listar conversas do painel (ver não lidas)
python ".claude/skills/responder-whatsapp/wa_cdp.py" inbox --last 25

# Ler as últimas mensagens de um número (<< recebida, >> enviada)
python ".claude/skills/responder-whatsapp/wa_cdp.py" read 5531999999999 --last 12

# Enviar uma resposta (texto de arquivo; {first} é substituído por --first)
python ".claude/skills/responder-whatsapp/wa_cdp.py" send 5531999999999 tmp/resposta.txt --first Maria --anchor "trecho-âncora"
```
Como módulo:
```python
from importlib.util import spec_from_file_location, module_from_spec
# importe wa_cdp e use: connect(wa_ws_url()) -> CDP(ws); setup(c); send_text(c, tel, texto)
```

## Como funciona (lições embutidas — não regredir)
- **Telefone:** prefixe `55` antes do deeplink `send?phone=`. Números só com DDD (ex.: `31...`) falham com `CHAT_NAO_ABRIU`.
- **Clipboard exige foco:** `navigator.clipboard.writeText` dá *NotAllowedError* se a página não está focada. `setup()` chama `Emulation.setFocusEmulationEnabled(true)`, que destrava o clipboard mesmo com a aba em segundo plano.
- **Envio confiável:** limpar a caixa, colar (Ctrl+V) com fallback `Input.insertText`, e **clicar no botão Enviar** (o Enter falha quando o WhatsApp está montando o preview de um link). Confirmar o envio pela **caixa vazia** + até 3 tentativas. Status: `ENVIADO` / `NA_CAIXA` (preso, não saiu).
- **Mensagem recebida vs enviada:** uma `.copyable-text` é *recebida* quando o `data-pre-plain-text` contém os **últimos 8 dígitos do contato**. Não use a classe `message-in` nem exclua o nome do remetente.
- **CSV de planilha (se precisar cruzar):** abrir `https://docs.google.com/spreadsheets/d/{ID}/export?format=csv&gid={GID}` via `Target.createTarget` (cai em `C:\Users\lucas\Downloads`) e parsear com `csv.reader` (suporta célula multi-linha) — ver `feedback_google_sheets_csv_scraping`.

## Boas práticas de resposta
- Personalize com o **primeiro nome** e responda ao que a pessoa de fato escreveu (leia com `read` antes).
- **Sem travessão (—)** em nenhuma mensagem (`feedback_sem_travessao_textos`).
- Faça um **canário** (1 envio) + conferir por screenshot antes de disparar em lote.
- Em lote, deixe ~2s entre envios e registre o resultado por contato.
