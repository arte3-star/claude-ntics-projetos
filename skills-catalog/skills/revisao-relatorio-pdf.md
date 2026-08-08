---
name: revisao-relatorio-pdf
user-invocable: true
description: |
  Revisa um relatorio de projeto em PDF (relatorio final, dossie de prestacao de
  contas, deck de resultados) pagina por pagina antes de ir para o patrocinador
  ou cliente: erro ortografico, inconsistencia de nomenclatura (nome do
  patrocinador/parceiro grafado diferente do oficial, nome de pessoa com letra
  faltando ou grafia trocada entre mencoes) e erro de contexto/numeros que nao
  batem entre paginas (total que nao fecha com a soma das partes, numeracao de
  modulo/fase duplicada, contagem de itens diferente da galeria mostrada).

  Acione quando o usuario mandar um PDF de relatorio e disser algo como "analisa
  esse relatorio", "revisa esse PDF", "confere se tem erro nesse relatorio",
  "faz uma analise completa desse PDF", "ve se tem erro ortografico e de
  contexto", "confere antes de mandar pro cliente/patrocinador", "cita [nome] ao
  inves de [nome oficial]?", ou pedir para conferir numeros/dados de um
  relatorio em PDF. Mesmo que o usuario nao peca explicitamente "roda a skill",
  acione sempre que o pedido for revisar/auditar um relatorio de projeto em PDF
  antes de ele ser publicado ou enviado a terceiros.
---

Leia e execute o workflow completo em `workflows/marketing/revisao/revisao_relatorio_pdf.md`.

## Quando usar

- Antes de qualquer relatorio final de projeto (prestacao de contas, dossie de
  resultados, deck pos-execucao) ser enviado ao patrocinador/cliente.
- Quando o usuario mandar um PDF e pedir para "conferir erro" nele.
- Ao suspeitar que um nome de patrocinador/parceiro esta sendo grafado errado ou
  de forma inconsistente ao longo do relatorio.

## Inputs

- **Arquivo** — caminho do PDF a revisar.
- **Foco opcional** — se o usuario ja apontar uma suspeita especifica (ex.: "ve
  se cita X em vez de Y"), confirme essa primeiro mas nao pare so nela: rode a
  checagem completa de qualquer forma, porque os erros de maior impacto ate
  agora (numero que nao fecha com a soma das partes) so aparecem numa leitura
  pagina a pagina.
- **Anotar no PDF?** — perguntar se o usuario quer so a resposta no chat ou
  tambem uma copia do PDF com os achados como comentario (sticky note) na
  posicao de cada trecho. Default: so responder no chat, a nao ser que o
  usuario ja tenha pedido antes.

## Ambiente

Esta maquina nao tem poppler/pdftoppm — o Read tool nativo do Claude Code falha
em paginas de PDF (`pdftoppm is not installed`). Nao insista nele: use direto o
script `tools/adobe/relatorio_pdf_review.py` (PyMuPDF), que nao depende de
binario externo. Detalhe completo no workflow.

## Ferramentas

| Ferramenta | Arquivo | Funcao |
|---|---|---|
| Extrator + renderizador | `tools/adobe/relatorio_pdf_review.py extract` | Confere contagem real de paginas, extrai texto (so como pista) e renderiza cada pagina em PNG |
| Zoom | `tools/adobe/relatorio_pdf_review.py zoom` | Recorte em alta resolucao pra confirmar numero/palavra suspeita antes de reportar |
| Anotador | `tools/adobe/relatorio_pdf_review.py annotate` | Grava copia do PDF com os achados como comentario (sticky note) |

## Output

Resposta no chat organizada por categoria (numerico/contexto primeiro, depois
ortografico, depois nomenclatura, depois formatacao), com pagina + trecho citado
+ porque esta errado. Fecha com o que foi conferido e nao tinha problema. Se
pedido, tambem uma copia `<nome do arquivo> - REVISADO.pdf` com os achados como
comentario.

## Fluxo

1. Rodar `extract` e usar a contagem real de paginas (o aviso automatico de
   tamanho do PDF pode estar errado).
2. Ler o texto extraido como mapa/indice — nunca como fonte de verdade.
3. Ler cada pagina renderizada via Read tool, procurando ortografia,
   nomenclatura e contexto/numeracao.
4. Sempre que houver total + partes, somar as partes e comparar — essa e a
   checagem que mais rende.
5. Fazer zoom pra confirmar qualquer achado numerico antes de reportar.
6. Reportar por categoria; se pedido, gerar o PDF anotado com `annotate`.
