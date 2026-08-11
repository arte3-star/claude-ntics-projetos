# Prompt canônico de preenchimento

Entregue este bloco **verbatim** para o usuário colar na barra lateral do Claude no Chrome, com a
aba nova em foco e o PDF do SALIC disponível. Só é permitido personalizar o nome/PRONAC do projeto
se ele pedir; o corpo das regras não muda.

```
Você está na minha planilha de prestação de contas Rouanet no Google Sheets.
Eu JÁ criei a aba do novo projeto (duplicada do MODELO, já renomeada e com o
título A1 ajustado) e ela está ABERTA/ativa. Não crie nem renomeie abas.

TAREFA: preencher o orçamento desta aba a partir do PDF do orçamento aprovado
(SALIC) que estou te enviando.

== COMO LER O PDF ==
- Use SEMPRE a coluna "VL. APROVADO" como o total de cada item.
- NÃO inclua itens com VL. APROVADO = 0 (foram glosados). Atenção: alguns itens
  aparecem com 0 na coluna "sugerido" mas com valor cheio em "aprovado" (foram
  restaurados) — esses ENTRAM. A régua é SEMPRE a coluna APROVADO.
- De cada item válido, extraia: descrição, cidade/UF, QTDE, OCOR.,
  VL. UNITÁRIO e VL. APROVADO.

== ESTRUTURA DA ABA ==
Cada item ocupa um BLOCO de 5 linhas, começando na linha 5:
  - 1ª linha do bloco (laranja) = dados do item
  - 3 linhas seguintes (verdes) = ficam VAZIAS (são para lançar pagamentos depois)
  - 5ª linha (azul) = SALDO
Preencha SOMENTE a linha laranja, nestas colunas:
  A = número sequencial (1, 2, 3, ...)
  B = "Descrição - Cidade/UF"   (ex: "Palestrante - Rio de Janeiro/RJ")
  D = unidade (MÊS, DIÁRIA, UNIDADE, SERVIÇO, TRECHO... conforme a natureza)
  F = QTDE
  G = OCOR.
  H = VL. UNITÁRIO
  I = FÓRMULA  =F<linha>*G<linha>*H<linha>   (ex: na linha 5 -> =F5*G5*H5)
Deixe C, E, J, K e L vazias. NÃO escreva nada nas linhas verdes nem na linha SALDO
(a linha SALDO já tem a fórmula =SOMA(...) do modelo).

== PASSOS ==
1) Conte os itens válidos. Se faltarem blocos, selecione um bloco formatado inteiro
   (5 linhas, ex.: A5:L9), copie e cole repetido para baixo até ter blocos para
   todos os itens (isso preserva cores e fórmulas). Use a Caixa de Nomes para
   selecionar os intervalos com precisão. Preencha colando os dados de uma vez,
   não célula a célula.
2) Preencha todos os itens.
3) Depois do último bloco, deixe 1 linha em branco e crie a linha de total:
   - na coluna H, escreva:  TOTAL GERAL
   - na coluna I, a fórmula:  =SOMASE(H5:H<ultima_linha>,"SALDO",I5:I<ultima_linha>)
     (onde <ultima_linha> = 4 + 5 × número de itens; ex.: 50 itens -> linha 254)
   - copie o formato de uma linha SALDO para essa linha (pincel de formatação),
     para ficar com R$ e o mesmo realce.
   Obs.: se ao digitar a fórmula o Sheets duplicar aspas/parênteses, COLE a fórmula
   em vez de digitar.
4) CONFERÊNCIA OBRIGATÓRIA: o valor do TOTAL GERAL tem que bater EXATAMENTE com o
   "Total do Projeto" (coluna VL. APROVADO) da última página do PDF. Me diga os
   dois valores e confirme se batem.

Trabalhe por etapas: preencha a primeira etapa/cidade, me mostre, e só continue
depois que eu confirmar. Se algum total não bater, PARE e me avise.
```
