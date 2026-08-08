---
name: video-postprod
description: |
  Pos-producao de video com FFmpeg: remove silencio, masteriza audio para padrao
  broadcast, queima legendas e aplica zoom dinamico em talking-head. Receitas
  validadas, prontas para rodar em depoimento de campo, reels e video de projeto.

  Acione quando o usuario disser: "limpa esse video", "tira as pausas do video",
  "remove o silencio", "melhora o audio do video", "masteriza o audio",
  "queima a legenda", "coloca legenda no video", "legenda pro reels",
  "poe zoom no depoimento", "trata o video antes de publicar",
  "o audio ta baixo/inconsistente", "video de celular com audio ruim".

  Tambem acione quando o material for depoimento gravado em campo, talking-head
  longo, ou qualquer video que vai para Instagram/TikTok (onde a maioria assiste
  sem som e a legenda queimada e obrigatoria).

  NAO confundir com briefing-video (que gera o roteiro para o editor humano) nem
  com capa-video (que faz a capa estatica).
---

# Pos-producao de video (FFmpeg)

Cada etapa tem sua receita em arquivo proprio. Leia o arquivo da etapa antes de
rodar o comando: os parametros foram ajustados para o material de campo da NTICS
e mudar valor no chute degrada o resultado.

## Ordem recomendada do pipeline

A ordem importa. Rodar fora de sequencia retrabalha ou degrada o material.

1. **`silence-removal.md`** — remove pausas excessivas, mantendo 0,3s para
   naturalidade. Primeiro, porque encurtar depois invalida os timestamps da legenda.
2. **`smart-zoom.md`** — zoom suave em momentos de enfase, para dar dinamismo a
   talking-head e depoimento longo.
3. **`audio-mastering.md`** — highpass, EQ de presenca, compressao e normalizacao
   de loudness. Sempre antes de adicionar trilha.
4. **`burn-subtitles.md`** — queima a legenda por ultimo, a partir do SRT do
   Whisper ou do TTS, com o corte e o audio ja definitivos.

Nem todo video precisa das 4 etapas. Depoimento de celular normalmente precisa de
todas; captacao de camera boa costuma dispensar o passo 3.

## Antes de entregar

- Confira o resultado assistindo, nao so pelo log do FFmpeg.
- Video que vai para rede social nao leva a regua institucional do projeto.
- Guarde o original: todo comando aqui gera arquivo novo, nunca sobrescreva a captacao bruta.
