# Conferência final e erros comuns

## Checklist de conferência final

- [ ] Nome da aba no padrão `PRONAC_NOME` (ex.: `2512916_PROGRAMA...`).
- [ ] Título A1 no padrão `Orçamento_NOME_PRONAC`.
- [ ] Todos os itens com **VL. APROVADO > 0** foram lançados (itens glosados a R$0 ficam de fora).
- [ ] Coluna I das linhas laranja é **fórmula** `=F*G*H` (clique numa célula e veja na barra de
      fórmulas).
- [ ] Linhas verdes e SALDO **sem valores digitados** (só as fórmulas do modelo).
- [ ] SALDO do 1º item nasce **igual ao total** do item (sem pagamentos lançados).
- [ ] Linha **TOTAL GERAL** criada, com R$ e realce.
- [ ] **TOTAL GERAL = "Total do Projeto" (VL. APROVADO) do PDF** — idênticos.

## Erros comuns e solução

| Erro | Solução |
|---|---|
| Renomeou/editou a aba errada (ex.: o MODELO) | Desfaça na hora (Ctrl+Z) e use **botão direito → Renomear** na aba certa. |
| Total não bate por uns reais | Quase sempre é item glosado incluído por engano, ou um item restaurado deixado de fora. Confira a coluna **VL. APROVADO** item a item. |
| Valores aparecem como "$" e não "R$" | Copie o formato de uma linha SALDO (pincel de formatação) para a célula. |
| Cores/formatação sumiram em itens novos | Os blocos extras precisam ser **copiados de um bloco formatado**; nunca digitados do zero. |
| Fórmula entrou como texto | Cole a fórmula em vez de digitar (evita o Sheets duplicar aspas). |
