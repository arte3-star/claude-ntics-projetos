# Artigo Mensal — NTICS Projetos

> Compila os 4 roteiros/temas semanais em um artigo profissional para patrocinadores e publico B2B, posicionando a NTICS como guia estrategico em ESG.

---

## Contexto da Marca

Antes de comecar, leia:

1. `brand-book/02-identidade-verbal/tom-de-voz.md` — secoes 3.3 (Blog: 55% formal, 70% inspiracao) e 3.2 (Propostas B2B: 80% formal, 85% dados)
2. `brand-book/02-identidade-verbal/mensagens-chave.md` — elevator pitches, manifesto, proof points
3. `brand-book/data/brand-data.yaml` — metricas completas, credenciais, projetos
4. `brand-squad/tasks/create-brand-story.md` — framework StoryBrand SB7

---

## Inputs do Usuario

| Campo | Tipo | Obrigatorio | Descricao |
|-------|------|-------------|-----------|
| `roteiros_semanais` | string | Sim | Os 4 roteiros de video ou resumos dos temas semanais |
| `tema_mensal` | string | Sim | Tema central do mes |
| `patrocinador` | string | Nao | Nome do patrocinador (se aplicavel) |
| `links_videos` | string | Nao | URLs dos videos publicados para embedding |
| `dados_adicionais` | string | Nao | Metricas ou resultados extras para incluir |

---

## Execucao

### Fase 1: Extrair o Fio Narrativo

1. Analisar os 4 roteiros para encontrar a progressao logica
2. Usar o framework **ABT** do storytelling squad (`storytelling/tasks/build-narrative.md`):
   - **AND:** O contexto do tema (semana 1)
   - **BUT:** Os desafios e equivocos (semana 2)
   - **THEREFORE:** As solucoes e cases (semanas 3-4)
3. O artigo nao e 4 textos colados — e uma narrativa unica que INTEGRA os 4 temas

### Fase 2: Posicionamento StoryBrand

Usar o framework StoryBrand (`brand-squad/tasks/create-brand-story.md`):

- **Heroi:** O patrocinador / empresa leitora (nao a NTICS)
- **Problema:** A dificuldade do heroi com o tema ESG/CSR
- **Guia:** A NTICS (autoridade + empatia)
- **Plano:** O que a NTICS propoe / como o tema se resolve
- **Acao:** CTA consultivo
- **Sucesso:** O que muda quando o heroi age
- **Fracasso:** O custo de nao agir (sutil, nao ameacador)

### Fase 3: Escrita com Voz Dupla

O artigo tem 2 tons:

**Resumo Executivo (topo):**
- Tom de Proposta Comercial: 80% formal, 75% tecnico, 85% dados
- 2-3 paragrafos densos, orientados a resultado
- Para o decisor que le rapido

**Corpo do Artigo:**
- Tom de Blog/Conteudo Educativo: 55% formal, 60% tecnico, 70% inspiracao
- Tom de quem ensina com generosidade (arquetipo Sage)
- Aberturas com pergunta ou cenario
- Analogias do cotidiano
- Dados como suporte, nao protagonistas

### Fase 3.1: Regras de Posicionamento (padrao do artigo publicado em ntics.com.br)

O artigo mensal **e artigo de blog para o site da NTICS**, lido por diretores ESG, gestores de investimento social e patrocinadores. Nao e relatorio interno, nao e release de campanha, nao e agregador de pecas semanais. E peca autossuficiente que tem que se sustentar sozinha quando alguem cai nela por busca organica ou link compartilhado.

Referencia canonica: artigo M01 publicado em https://ntics.com.br/os-5-sinais-que-distinguem-empresas-maduras-em-responsabilidade-social/

**Regras de tom e estrutura (do publicado):**

1. **Titulo do artigo NAO e o tema mensal abstrato.** Use o nome de uma das 4 secoes, em formato de titulo de blog que gera curiosidade. M01 tem 4 secoes, o titulo do artigo virou "Os 5 sinais que distinguem empresas maduras em RS" (secao 03). Tema mensal vira contexto interno; titulo publico tem que vender clique.
2. **Logo abaixo do H1 vem o `.article-deck`**, paragrafo de destaque (~50 palavras) que resume a tese central. E o que aparece no preview do compartilhamento social.
3. **Resumo Executivo** e um H2 + 1-2 paragrafos de texto corrido. NAO usar caixa estilizada `.executive-summary` (era padrao antigo).
4. **4 secoes H2 com tese-titulo**, no padrao "Tese: subtese explicativa" (ex: "Juventude como investimento: a estrategia ESG mais barata..."). Sem section-number (01/02). Sem "Semana N".
5. **Cada secao tem 3-4 paragrafos densos** + 1 elemento visual a cada 2 secoes (imagem inline com figcaption descritiva, ou blockquote, ou lista curta). Nao precisa todos.
6. **Use projetos NTICS reais como exemplos que provam o ponto**, nao como pitch. M01 publicado cita Conhecendo os ODS (326 mil pessoas, 868 cidades, 1,19M indireto), ODS Cultural nas Escolas (Repsol como patrocinador), Amazonia 2030 (Kambeba). 2-3 projetos no artigo inteiro. Citar patrocinador apenas se o case nao funcionar sem ele.
7. **Blockquotes = citacao real de autoridade externa.** M01 cita Larry Fink/BlackRock. NAO fabricar estatisticas no formato "estudos mostram que 3,2x...". Se nao tem fonte verificavel, nao escreve. Se quer dado, use numero real NTICS ou referencia publica (BlackRock, McKinsey, OIT, Banco Mundial, Bill Gates Foundation, ONU/Pacto Global).
8. **Imagens inline com fotos reais de projetos NTICS** ou, se gerada via Leonardo, prompts que pareçam documentais autenticos brasileiros, NAO corporativos genericos (sala de reuniao, executivos em call). Cena: jovens em oficina, roda de conversa comunitaria, professor em sala publica, mae participando de capacitacao. Figcaption descreve o programa e ja inclui o numero relevante (vira ponto de prova sem precisar repetir no paragrafo).
9. **Conclusao = H2 com frase manifesto/pergunta + 2-3 paragrafos amarrando.** Sem CTA box gradiente. M01 termina com "Consciencia e o Ponto de Partida. Proposito e o Motor.", M02 com "Autoridade e o que sobra quando o ciclo de incentivo acaba".
10. **No fim, apenas 1 bloco:** `.ntics-about` com boilerplate institucional. Citar 4 patrocinadores (Nubank, Bayer, Eneva, Whirlpool no padrao M01) sao OK quando estao dentro do bloco "Sobre a NTICS", nao no corpo do artigo.

**O que NAO incluir no body (foi tentado e e errado):**
- `.video-cta` em cada secao com "Semana N, Video: ..." -- jargao interno; leitor do site nao sabe que existem semanas.
- `.stats-row` no topo com 24 anos / 1.060+ / 11,4M / NPS 88 -- esses numeros aparecem no `.ntics-about` no fim, nao gritando no topo.
- `.cta-box` gradiente com "Conversa com o time NTICS" -- WordPress/Uncode cuida do CTA na pagina; o body nao precisa duplicar.
- `<dl class="seo-meta">` no corpo do artigo -- SEO meta vai no `<head>` do WordPress (campo da pagina), nao dentro do `<article>`.
- "Semana 1", "Semana 2", "Semana 3", "Semana 4" em qualquer ponto -- o artigo e peca autossuficiente, nao agregador de 4 releases.

### Fase 4: Conexao com videos (sem video-cta no corpo)

- O artigo NAO referencia os videos das 4 semanas. Eles vivem em outro circuito (Instagram, LinkedIn).
- Se quiser dar visibilidade aos videos, faca no canal proprio (post de Linkedin com link do artigo + lista dos 4 reels), nao dentro do artigo do site.
- Excecao: se um video especifico ilustra um conceito que o artigo ja discute, embed dele pode ser usado pontualmente (1x), mas sem o rotulo "Semana N".

### Fase 5: SEO e Metadados (vao para o WordPress, nao para o body)

Esses campos devem ser entregues junto com o HTML do body, mas para serem preenchidos nos campos do CMS, nao dentro do `<article>`:

- **Titulo SEO:** maximo 60 caracteres, replica o titulo do artigo (que ja segue padrao blog provocativo).
- **Meta descricao:** maximo 160 caracteres, parafraseia o deck.
- **Slug URL:** kebab-case do titulo, sem palavras vazias.
- **Categoria:** "Artigos".
- **Tags:** ESG, Responsabilidade Social, + 1-2 termos da tese central.
- **Imagem destacada:** o hero gerado (1152x896), enviado separadamente.
- **Tempo de leitura:** calcular ~200 palavras/minuto.

### Fase 6: Componentes HTML obrigatorios no Body (padrao publicado)

O body do artigo (`<article class="article-body">`) deve conter, nessa ordem:

1. `<p class="article-deck">` -- subtitulo/deck de destaque, ~50 palavras, abaixo do H1 que o WordPress renderiza pelo titulo.
2. `<h2>Resumo Executivo</h2>` + 1-2 paragrafos de texto corrido (sem caixa estilizada).
3. 4 secoes, cada uma:
   - `<h2>{Tese-titulo da secao}</h2>` (sem section-number)
   - 3-4 paragrafos densos
   - Opcional: 1 `<figure class="article-image">` com figcaption descritiva (idealmente em 2 das 4 secoes, ja com fato/numero do projeto)
   - Opcional: 1 `<blockquote>` com citacao real (idealmente em 1-2 secoes)
   - Opcional: 1 lista ou texto corrido com elementos numerados quando enriquecer o argumento
4. `<h2>{Frase-manifesto da conclusao}</h2>` + 2-3 paragrafos amarrando os 4 temas e fechando a tese.
5. `<div class="ntics-about">` -- bloco "Sobre a NTICS Projetos" com 1 paragrafo institucional (24 anos, 1.060+ projetos, 11,4M pessoas, 165 cidades, NPS 88, certificacoes, 4 patrocinadores ancora, escritorios).

**Eliminados do padrao** (estavam em versao anterior do workflow, foram identificados como ruido pelo Lucas em 2026-05-22):
- ~~`.article-lead` em caixa azul~~
- ~~`.executive-summary` em caixa cinza com borda azul~~
- ~~`.stats-row` no topo~~
- ~~`.video-cta` em cada secao~~
- ~~`.cta-box` gradiente azul no fim~~
- ~~`<dl class="seo-meta">` no fim do body~~

---

## Formato de Saida

```markdown
# {Titulo do Artigo}

**Tema:** {tema mensal}
**Mes/Ano:** {mes}
**Palavras:** {contagem}
**Publico-alvo:** Patrocinadores, diretores ESG, gestores de responsabilidade social

---

## Resumo Executivo

{2-3 paragrafos em tom B2B: dados, resultados, valor estrategico. Para o decisor que le rapido.}

---

## Introducao

{Por que este tema importa agora. Hook com dado ou cenario. Conexao com a realidade do leitor.}

## 1. {Titulo da Secao — baseado na Semana 1}

{Conteudo integrado do video/tema da semana 1}

> Assista ao video: [{titulo do video}]({link})

## 2. {Titulo da Secao — baseado na Semana 2}

{Conteudo integrado do video/tema da semana 2}

> Assista ao video: [{titulo do video}]({link})

## 3. {Titulo da Secao — baseado na Semana 3}

{Conteudo integrado}

> Assista ao video: [{titulo do video}]({link})

## 4. {Titulo da Secao — baseado na Semana 4}

{Conteudo integrado}

> Assista ao video: [{titulo do video}]({link})

## Conclusao: {Frase visionaria}

{Amarrar tudo. Visao de futuro. CTA consultivo e nao-agressivo.}

---

## Sobre a NTICS Projetos

{Boilerplate: 24 anos, 1.060+ projetos, 11,4M pessoas, NPS 88, ISO 9001, Pacto Global ONU. Extrair de brand-data.yaml.}

---

## Metadados SEO

- **Titulo SEO:** {max 60 chars}
- **Meta descricao:** {max 160 chars}
- **Palavras-chave:** {5-8 termos}
- **Tags:** {categorias}
```

---

## Checklist de Qualidade

- [ ] Os 4 temas semanais estao integrados (narrativa unica, nao 4 textos colados)
- [ ] Arco ABT coerente do inicio ao fim
- [ ] NTICS posicionada como guia (StoryBrand), nao como heroi
- [ ] Resumo executivo em tom B2B (80% formal, 85% dados)
- [ ] Corpo em tom Blog (55% formal, 70% inspiracao)
- [ ] Pelo menos 4 proof points do brand-data.yaml
- [ ] `.video-cta` em cada uma das 4 secoes
- [ ] CTA consultivo, nao vendedor
- [ ] Boilerplate NTICS atualizado
- [ ] Metadados SEO completos
- [ ] **No maximo 1 projeto NTICS especifico citado no artigo inteiro** (regra Fase 3.1)
- [ ] **Zero nomes de patrocinadores/clientes no corpo nem no boilerplate** (regra Fase 3.1)
- [ ] **No maximo 2 mencoes a "NTICS" no corpo das 4 secoes** (CTA box, ntics-about e seo-meta nao contam)
- [ ] **Conclusao em modo manifesto**, nao em modo venda
- [ ] **Pitch isolado no `.cta-box`**, nunca no meio do texto
- [ ] 1 blockquote com dado de estudo em cada secao (peso analitico)
- [ ] Sem travessoes em-dash (`—`) -- regra global CLAUDE.md
- [ ] Estrutura dos 9 blocos da Fase 6 presente na ordem

---

## Adaptacao LinkedIn Article

Alem do formato Markdown para o site, gerar versao para **LinkedIn Article** nativo.

### Como adaptar

1. **Formato:** Publicar como LinkedIn Article (ferramenta nativa da plataforma)
2. **LinkedIn Newsletter:** Se a newsletter "ESG em Foco" estiver ativa, publicar como edicao da newsletter (notificacao push para assinantes)
3. **Titulo:** Max 60 caracteres, com numero ou dado concreto (ex: "1.060 projetos depois: o que aprendemos sobre impacto real")
4. **Imagem de capa:** Usar a mesma imagem hero do artigo do site (1152x896)
5. **Tom:** Subir para 70% formal, 75% dados (vs 55%/60% do blog)
6. **Estrutura:** Manter a mesma do artigo (resumo executivo + 4 secoes + conclusao)
7. **Adaptacoes de tom:**
   - Resumo executivo: mais direto, orientado a resultado
   - Corpo: menos analogias, mais dados e referencias
   - CTA: consultivo (ex: "Quer explorar como leis de incentivo podem financiar um projeto como este?")
8. **Boilerplate NTICS:** Manter no final com dados atualizados do `brand-data.yaml`
9. **Links:** Incluir links para videos correspondentes

### Output adicional

Adicionar ao formato de saida uma secao:

```markdown
---

## LinkedIn Article

**Titulo LinkedIn:** {max 60 chars, com dado concreto}
**Imagem de capa:** {path da imagem hero}
**Newsletter ESG em Foco:** Sim/Nao (publicar como edicao?)
**Corpo adaptado:** {artigo com tom ajustado para LinkedIn — 70% formal, 75% dados}
```

Referencia completa: `workflows/marketing/referencia/linkedin_strategy.md`

---

## Conexao com Outras Skills

- Input vem de: `/roteiro-video` (os 4 roteiros semanais)
- Conteudo alimenta: `/email-marketing` (secao "Artigo Destaque")
- Conteudo alimenta: LinkedIn Article / Newsletter "ESG em Foco" (Pilar 3)
