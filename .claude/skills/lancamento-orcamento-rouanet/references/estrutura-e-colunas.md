# Estrutura da aba, mapa de colunas e fórmulas

## Como ler o PDF (SALIC)

- **Régua única: a coluna "VL. APROVADO"** é o total de cada item.
- **Itens glosados (VL. APROVADO = 0) NÃO entram.**
- **Itens restaurados** (0 na coluna "sugerido", mas valor cheio em "aprovado") **ENTRAM** — vale
  sempre a coluna APROVADO.
- De cada item válido extraia: descrição, cidade/UF, QTDE, OCOR., VL. UNITÁRIO e VL. APROVADO.

## Estrutura de blocos

Cada item ocupa um **bloco de 5 linhas**, começando na **linha 5**:

1. **1ª linha (laranja)** = dados do item — a única que se preenche.
2. **2ª a 4ª linha (verdes)** = ficam **vazias** (para lançar pagamentos na execução).
3. **5ª linha (azul)** = **SALDO** (já traz a fórmula do modelo).

Se faltarem blocos, **copie um bloco formatado inteiro** (5 linhas, ex.: `A5:L9`) e cole repetido
para baixo — isso preserva cores e fórmulas. Nunca digite blocos do zero. Use a Caixa de Nomes para
selecionar os intervalos com precisão.

## Mapa das colunas (o que vai na linha laranja)

| Col | Cabeçalho | O que vai (linha laranja) |
|---|---|---|
| A | nº item | número sequencial 1, 2, 3... |
| B | BENEFICIÁRIO | Descrição + Cidade/UF (ex.: "Palestrante - Rio de Janeiro/RJ") |
| C | PAGO EM | *(vazio — preenche na execução)* |
| D | REFERÊNCIA | unidade (MÊS, DIÁRIA, UNIDADE, SERVIÇO, TRECHO...) |
| E | Nº NF / DATA | *(vazio)* |
| F | QUANTIDADE | QTDE do PDF |
| G | OCORRENCIA | OCOR. do PDF |
| H | VALOR UNITARIO | VL. UNITÁRIO do PDF |
| I | TOTAL EXECUTADO | **fórmula `=F*G*H`** (ex.: na linha 5 → `=F5*G5*H5`) |
| J / K / L | Nota / Realocação / MinC | *(vazio)* |

Deixe **C, E, J, K e L vazias**. Não escreva nada nas linhas verdes nem na linha SALDO.

## Fórmulas do modelo (já vêm no bloco — não precisa digitar)

- **SALDO** (linha azul): `=SOMA(I<laranja>:I<verde3>)` — ex.: `=SOMA(I5:I8)`.
- **TOTAL GERAL** (linha final): `=SOMASE(H5:H<ultima>,"SALDO",I5:I<ultima>)`.

## Linha TOTAL GERAL

Depois do último bloco, deixe **1 linha em branco** e crie a linha de total:

- Coluna **H**: escreva `TOTAL GERAL`.
- Coluna **I**: fórmula `=SOMASE(H5:H<ultima_linha>,"SALDO",I5:I<ultima_linha>)`, onde
  `<ultima_linha> = 4 + 5 × número de itens` (ex.: 50 itens → linha 254).
- Copie o **formato de uma linha SALDO** (pincel de formatação) para ficar com R$ e o mesmo realce.

> Se o Sheets duplicar aspas/parênteses ao digitar a fórmula, **cole** a fórmula em vez de digitar.
