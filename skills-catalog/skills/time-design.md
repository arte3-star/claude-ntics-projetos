---
name: time-design
user-invocable: true
description: |
  Monta Agent Team de design (Leonardo AI, Adobe Illustrator/After Effects, Gamma) para produzir assets visuais em paralelo.

  Acione quando o usuario disser: "monta o time de design", "agent team de design", "produz varios assets de uma vez", "kit completo de pecas", "time pra fazer o visual".

  Para uma peca so, use a skill especifica (carrossel-cliente, capa-video, kv-derivar).
---

> 📚 **Referência Leonardo AI:** O Image Creator deste time usa Leonardo AI seguindo a estrutura já validada da skill. Se surgir erro da API, dúvida sobre payload ou resultado visual inesperado, consulte `workflows/marketing/referencia/leonardo_ai_core.md` como base de conhecimento complementar (modos, erros conhecidos, exemplos).

> Nota: o workflow detalhado `workflows/marketing/team_design_content.md` nao existe no repositorio. A especificacao autoritativa e a que esta nesta propria skill. Nao improvise um workflow ausente: se faltar detalhe, pergunte ao Lucas.

Use Agent Teams para criar o time. Monte os teammates conforme descrito no workflow:
- **Lead** (design-lead): coordena e valida qualidade
- **Image Creator**: gera imagens via Leonardo AI
- **Adobe Specialist**: adapta arte, vetoriza, renderiza motion
- **Presentation Maker**: cria apresentacoes via Gamma MCP

Pergunte ao usuario qual tipo de projeto (carrossel, apresentacao, motion, kit completo) e quais inputs ele tem disponiveis.
