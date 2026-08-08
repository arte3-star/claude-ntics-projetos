---
name: relatorio-semanal-estacao-samarco
description: |
  Atualiza semanalmente a aba "Relatórios" do painel do cliente Estação Samarco (projeto 132) com o que aconteceu na semana: trilhas que terminaram, presenças (Diário de Campo) e as melhores fotos do fotógrafo. Roda toda sexta-feira de manhã na nuvem (RemoteTrigger) em modo PRÉVIA — gera a atualização e envia por e-mail para <EMAIL> e <EMAIL> aprovarem antes de publicar.

  Acione quando o usuário disser: "atualiza os relatórios da Estação Samarco", "relatório semanal do painel Samarco", "rodar a rotina de sexta do painel 132", "prévia da semana da Estação Samarco", ou quando a rotina agendada de sexta disparar. Também quando o Lucas aprovar a prévia e pedir para publicar ("pode publicar o relatório da semana").
---

# Relatório Semanal — Painel Estação Samarco (projeto 132)

Rotina que mantém a aba **Relatórios** do painel do cliente (`ntics.com.br/estacao-samarco/painel/`) atualizada **toda semana**: quais trilhas aconteceram/terminaram, quantas pessoas participaram e as **melhores fotos do fotógrafo** (além das fotos do Diário de Campo).

Roda **sexta de manhã na nuvem** em modo **PRÉVIA** → e-mail para aprovação. Só publica depois que o Lucas aprova.

## Dois modos

- **PRÉVIA (sexta, nuvem):** levanta os dados da semana + lista as novas fotos do fotógrafo, monta um resumo e **envia por e-mail** para `<EMAIL>` e `<EMAIL>`. **Não publica.**
- **PUBLICAR (local, após aprovação):** baixa/converte/hospeda as fotos aprovadas, atualiza a aba Relatórios no template, faz build + publish.

---

## Fontes (constantes)

| Fonte | Como ler | O que traz |
|---|---|---|
| **Cronograma** | Google Sheets `<ID_PLANILHA_GOOGLE>`, aba `CRONOGRAMA GERAL` (cols: UF, Município, Comunidade, Local, Módulo, Início Divulgação, Abertura Inscrições, **Início das Aulas**, **Fim das atividades**) | quais trilhas ocorreram/terminaram na semana |
| **Diário de Campo** | POST `https://<REF_PROJETO_SUPABASE>.supabase.co/rest/v1/rpc/diario_campo` body `{"p_projeto":"estao_samarco_1781425848145"}` headers apikey+Authorization Bearer = anon key (ver abaixo) | presenças (`alunos`), data, `cidade`, `ativ`, fotos |
| **Inscritos** | GET `https://script.google.com/macros/s/<ID_SCRIPT>/exec?pwd=<SENHA>` → `registros[]` (cidade, presInicial, cert) e `total` | inscritas por localidade, certificados |
| **Melhores fotos (fotógrafo)** | Google Drive pasta `<ID_PASTA_DRIVE>` → **uma subpasta por localidade** (Santa Rita, BENEVENTE, Camargos, Catas Altas…), com JPG/HEIC (algumas têm subpasta "Melhores fotos") | curadoria do fotógrafo, além do Diário |

Supabase anon key (público, só leitura): `<CHAVE_JWT>`

Contexto de arquitetura, gotchas e nomenclatura: memória `reference_132_painel_dados_consolidados`.

---

## MODO PRÉVIA (sexta de manhã, nuvem)

1. **Janela da semana (BRT):** de sexta passada até hoje (últimos 7 dias). Guarde `DD/MM–DD/MM`.

2. **O que aconteceu na semana** — no cronograma, filtre as linhas cujo intervalo [Início das Aulas, Fim das atividades] intersecta a janela. Para cada trilha, marque se **terminou** nesta semana (Fim dentro da janela) ou está **em andamento**. Regra atual do calendário: **Empreendedorismo = 2 dias, Culinária e Beleza = 4 dias, aulas 17h–21h30**.

3. **Presenças** — do Diário de Campo, para cada localidade/trilha da semana, pegue o **pico de `alunos`** por sessão (não somar dias; não somar o mesmo evento em apelidos diferentes — casar pela cidade do próprio registro). Traga também nº de fotos no Diário.

4. **Inscritos/certificados** — do endpoint de inscritos, os números por localidade envolvida.

5. **Melhores fotos do fotógrafo** — liste o conteúdo da subpasta da(s) localidade(s) da semana em `<ID_PASTA_DRIVE>`. Conte quantas fotos novas há (JPG + HEIC) e monte os links: link da subpasta no Drive + até ~8 miniaturas `https://drive.google.com/thumbnail?id=<fileId>&sz=w600` (renderizam para quem tem acesso). **Não** processe/hospede fotos aqui.

6. **Monte a prévia (HTML)** — assunto `Estação Samarco · Relatório da semana DD/MM–DD/MM (prévia p/ aprovação)`. Corpo:
   - Cabeçalho com a janela da semana.
   - **O que rolou:** por localidade, quais trilhas terminaram/andaram, com as datas.
   - **Presenças:** tabela localidade × trilha × nº de presentes (fonte: Diário de Campo).
   - **Inscritos/certificados** atualizados por localidade.
   - **Fotos do fotógrafo:** por localidade, nº de fotos novas + link da pasta + miniaturas.
   - Rodapé: "Responda **aprovado** para publicar no painel (ou aponte ajustes). Publicação: skill `relatorio-semanal-estacao-samarco` modo PUBLICAR."

7. **Enviar por e-mail** para `<EMAIL>` **e** `<EMAIL>`:
   - **Local:** use o padrão `tmp/send_pmo_gmail_noverify.py` (OAuth gws, `verify=False`), assunto/HTML acima, os 2 destinatários.
   - **Nuvem:** se o conector Gmail permitir envio, envie aos 2. Se só permitir rascunho, crie **draft** endereçado aos 2 (o Lucas revisa e envia). Se o Gmail não estiver disponível, ponha a prévia INTEIRA na notificação final do trigger (que já vai por e-mail ao Lucas) e registre "Fabiula não recebeu — Gmail indisponível nesta execução".

8. **Regras:** nunca inventar número (só o que veio das fontes); se uma fonte não abriu na execução, diga qual e siga; sem travessão em texto que vá ao cliente; presença sempre rotulada "(campo)". **Não publica nada no painel neste modo.**

---

## MODO PUBLICAR (local, após "aprovado")

Feito numa sessão normal (tem o ambiente local, credenciais WP e pillow-heif). Diretório de trabalho: `G:\My Drive\Claude-NTICS-Projetos\tmp`.

1. **Fotos:** baixe as fotos das subpastas aprovadas com `download_file_content` (MCP Drive) → decodifique/converta local (`decode_all.py`/pillow-heif: `ImageOps.exif_transpose`, resize ~w1200, q82). Suba para `ntics.com.br/estacao-samarco/painel/<loc>/NN.jpg` via nticsfiles API (base64), como já feito em `camargos/` (`CAM_FOTOS`).

2. **Template** `tmp/mockup_template.html`, aba Relatórios (`renderRelatorio`) — arquitetura **data-driven por localidade**:
   - As abas de localidade saem do array **`RELTABS`** (dentro de `renderRelatorio`): cada item `{key,label,date,dot,inicio:'DD/mmm',sec,growth}`. Só aparece a aba cuja `inicio` (formato DD/mmm, ex.: `'28/jul'`) já passou — `.filter(t=>_parseData(t.inicio)<=_hoje())`. **Nova localidade começou = adicionar 1 item ao `RELTABS`** (mais recente em cima). Cada localidade viva usa `secLocViva({key,cor,nome,sub,crono,insc,cert,fotos,nota})` que já monta: inscritas + Trilhas e presenças (via `statusTrilha`+`diarioTrilha`) + gráfico de crescimento (`growthCard`, canvas `growth-<key>`) + galeria. Localidades encerradas (Camargos/Catas Altas) reusam `secCAM`/`secMG` + `growthCard`.
   - Fotos: const `<LOC>_FOTOS=Array.from({length:N},...'painel/<loc>/NN.jpg')`. O gráfico da aba lê `GROWTH_LOC` pelo nome em `growth`; **rode `tmp/gerar_growth_por_loc.py`** para atualizar `GROWTH_LOC` (e `GROWTH` combinado) com os dados novos da planilha.
   - **Cronograma:** se as datas/durações mudarem, atualizar **os DOIS**: o mapa `CRONO` (linha ~418, formato `'DD/mmm'`, usado por `statusTrilha`) **e** `CRONO_MG`/`CRONO_ES` (ISO, usado por renderCrono) — senão as datas divergem entre abas.
   - **Resumo da Semana** = só dados sólidos da semana (cards `opCard` das localidades da semana) + **"Melhores fotos da semana"** (fotos do Drive da semana; na falta, melhores do Diário de Campo) + crescimento combinado + engajamento/decisões. NÃO repetir o grid de gráficos por localidade (cada um está na sua aba).

3. **Build + publish:** `python build_index.py` → `python swap_painel.py`. Verifique ao vivo (navegar com `?cb=`, `auth()`, ler o DOM). Cuidado com o fallback (R=95) — espere `R.length>150`.

4. Registre no fim: o que foi publicado e o link do painel.

---

## Notas de manutenção

- Se o **cronograma** mudar (datas/durações), atualizar também `CRONO_MG`/`CRONO_ES` e `EXEC_CFG` (horas/oficinas) no template — hoje: Emp 2 dias/9h, Cul 4 dias/18h, Bel 4 dias/18h, aulas 17h–21h30.
- Pasta do fotógrafo tem estrutura irregular (às vezes subpasta "Melhores fotos", às vezes fotos soltas, mais Vídeos/Drone) — pegar as imagens da localidade, ignorar vídeos/zip.
- A rotina é **semanal (sexta)**; o RemoteTrigger correspondente chama esta skill em modo PRÉVIA.
