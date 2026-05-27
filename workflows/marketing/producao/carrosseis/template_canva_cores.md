# Template Canva Carrossel NTICS — Padrão de Cores por Categoria

> Referência para aplicar **variações de cor** no template Canva (`DAHKfZML7q8`) de forma que cada uma das 8 páginas tenha identidade visual própria por categoria, alinhada ao padrão NTICS dos carrosséis Leonardo anteriores (cultura-na-comunidade-rabobank, cinegastroarte, educacao-cultural-statkraft, etc).

---

## Paleta NTICS oficial (`brand-book/data/brand-data.yaml`)

| Cor | Hex | Uso |
|-----|-----|-----|
| Verde Regeneração | `#3DAA35` | Badge Capa + A Empresa |
| Teal Futuro | `#00A5B8` | Badge O Projeto + Alcance |
| Amarelo Consciência | `#F5B800` | Badge Metodologia + destaque amarelo em todos os bodies |
| Laranja Ação | `#E86428` | Badge Resultados |
| Rosa Transformação | `#D41A6A` | Badge Impacto |
| Azul Petróleo | `#005F73` | Fundo do card teal + texto escuro em badges amarelos |
| Branco | `#FFFFFF` | Texto base + texto em badges coloridos |

---

## Estrutura por página (8 páginas do template)

### Página 1 — Capa
- **Badge:** "PROJETO DE IMPACTO"
  - Fundo: `#3DAA35` (verde)
  - Texto: `#FFFFFF` (branco)
- **Headline linha 1 (branca):** texto principal em `#FFFFFF`
- **Headline linha 2 (destaque):** palavra-chave em `#F5B800` (amarelo)
- **Body:** branco com destaque em `#F5B800` (patrocinador ou número-chave)

### Página 2 — O Projeto
- **Badge:** "O PROJETO"
  - Fundo: `#00A5B8` (teal)
  - Texto: `#FFFFFF` (branco)
- **Headline linha 1 (branca) + linha 2 (destaque amarelo):** `#F5B800`
- **Body:** branco com destaque `#F5B800`

### Página 3 — Metodologia
- **Badge:** "METODOLOGIA"
  - Fundo: `#F5B800` (amarelo)
  - Texto: `#005F73` (azul petróleo, escuro) ← **ÚNICA badge com texto escuro**
- **Headline:** linha 1 branca + linha 2 `#F5B800`
- **Body:** branco com destaque `#F5B800`

### Página 4 — Alcance
- **Badge:** "ALCANCE"
  - Fundo: `#00A5B8` (teal)
  - Texto: `#FFFFFF` (branco)
- **Headline:** lista bullets brancas com números em `#F5B800`
- **Body:** sem body (espaço todo da lista)

### Página 5 — A Empresa
- **Badge:** "A EMPRESA"
  - Fundo: `#3DAA35` (verde)
  - Texto: `#FFFFFF` (branco)
- **Headline:** linha 1 branca + linha 2 `#F5B800`
- **Body:** branco com destaque `#F5B800` (patrocinador, Lei, ODS)

### Página 6 — Resultados
- **Badge:** "RESULTADOS"
  - Fundo: `#E86428` (laranja)
  - Texto: `#FFFFFF` (branco)
- **Headline:** linha 1 branca + linha 2 `#F5B800`
- **Body:** branco com destaque `#F5B800` (nota, %, número-chave)

### Página 7 — Impacto
- **Badge:** "IMPACTO"
  - Fundo: `#D41A6A` (rosa)
  - Texto: `#FFFFFF` (branco)
- **Headline:** linha 1 branca + linha 2 `#F5B800` (N.NNN PESSOAS)
- **Body:** branco com destaque `#F5B800`

### Página 8 — CTA
- **Sem foto top half** — manter background do template
- **Badge:** "Conecte-se" ou "Próximos Cases"
  - Fundo: `#00A5B8` (teal) ou `#005F73` (azul petróleo escuro)
  - Texto: `#FFFFFF`
- **Headline:** "SIGA PARA / MAIS PROJETOS" (branca + linha 2 amarela ou branca)
- **Body:** texto convidando seguir @nticsprojetos

---

## Limitações técnicas da API Canva

A API Canva **não permite** mudar via código:
- ❌ Cor de fundo de SHAPE (a pill colorida do badge)
- ❌ Cor de uma região específica dentro de um elemento TEXT (sempre afeta o elemento inteiro)

Por isso, o template precisa ter **as variações de cor já prontas no Canva web** (uma página por categoria). A automação via API só:
- ✅ Substitui texto preservando formatação que já está aplicada
- ✅ Substitui foto via insert_fill
- ✅ Não toca nas cores existentes

---

## Como aplicar no template DAHKfZML7q8

1. Abrir o design no Canva web
2. Em cada uma das 8 páginas, ajustar:
   - Cor de fundo do badge (clicar no SHAPE → cor)
   - Cor do texto do badge (em Metodologia mudar para `#005F73`)
   - Cor da region 2 da headline (selecionar texto → muda só pra `#F5B800` amarelo)
3. Salvar

Quando o template estiver pronto com as 8 variações, eu duplico essas 8 páginas em cada carrossel novo e só edito textos/fotos via API — as cores ficam corretas automaticamente.
