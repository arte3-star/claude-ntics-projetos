# Plataforma NTICS — Blueprint de Arquitetura

**Versão:** 0.1 (draft)
**Data:** 24 maio 2026
**Autor:** Lucas (NTICS / MTX) + Claude

---

## 1. Problema que estamos resolvendo

Cada projeto MTX hoje é montado do zero: planilhas, peças gráficas, relatórios, comunicação com o cliente. O humano gasta tempo no trabalho repetitivo (montar relatório semanal, brifar peça padrão, organizar grade horária) em vez do que só ele consegue fazer (engajar secretaria, encontrar produtor local, lidar com gráfica).

**Objetivo:** padronizar a entrega digital num pacote único que roda com IA no fundo, deixando o humano só para o que exige relacionamento.

---

## 2. Princípios de arquitetura

1. **Modular por projeto.** Um template único que se replica para qualquer projeto novo, sem reconstrução.
2. **IA no fundo, humano no controle.** Cloud Code processa e propõe; pessoas aprovam antes de qualquer coisa sair para o cliente.
3. **Editável por não-técnicos.** Responsáveis de projeto editam dados numa interface visual, sem precisar conversar com IA.
4. **Cliente acessa um portal vivo.** Em vez de relatórios PDF estáticos, o patrocinador entra num site e vê o estado atual.
5. **Começar com o que já temos.** Google Drive + ClickUp na primeira fase. Migrar para Airtable só se realmente travar.

---

## 3. As quatro camadas

```
┌─────────────────────────────────────────────────────────────┐
│  CAMADA 4 — APRESENTAÇÃO                                    │
│  WordPress + subdomínios (itapoa.ntics.com.br, etc.)        │
│  Site público + área restrita do cliente                    │
└─────────────────────────────────────────────────────────────┘
                            ▲
┌─────────────────────────────────────────────────────────────┐
│  CAMADA 3 — PRODUÇÃO VISUAL                                 │
│  Figma API (peças gráficas: banners, cartazes, camisetas)   │
│  Templates pré-aprovados, Cloud Code popula com dados       │
└─────────────────────────────────────────────────────────────┘
                            ▲
┌─────────────────────────────────────────────────────────────┐
│  CAMADA 2 — CÉREBRO (orquestração)                          │
│  Cloud Code lê ClickUp, processa, decide, dispara           │
│  Roda em schedule semanal + on-demand                       │
└─────────────────────────────────────────────────────────────┘
                            ▲
┌─────────────────────────────────────────────────────────────┐
│  CAMADA 1 — CAPTURA (fonte da verdade)                      │
│  ClickUp (tarefas, atualizações, status)                    │
│  Google Drive (arquivos: fotos, vídeos, artes, docs)        │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. Stack escolhido (fase 1)

| Função | Ferramenta | Por quê |
|---|---|---|
| Site / portal | WordPress (subdomínios) | Já existe site da NTICS, responsáveis sabem editar |
| Tarefas / status | ClickUp | Já usado pela equipe |
| Arquivos brutos | Google Drive | Já é onde está tudo; aguenta vídeo |
| Cérebro / automação | Cloud Code | Lê ClickUp, processa, decide, dispara |
| Peças gráficas | Figma + API | Templates aprovados, exporta em alta resolução, programável |
| Email automático | Gmail (rascunho) | Cloud Code monta, humano revisa antes de enviar |
| Dashboard interno (futuro) | Avaliar Metabase ou dashboard custom no WordPress | Decisão adiada para fase 2 |

**Não usamos agora:** Airtable, Lovable, Make/Zapier, Supabase. Ficam como plano B se o teste com Google Drive + ClickUp travar.

---

## 5. Estrutura do portal (cada projeto)

### Área pública (qualquer um acessa)

- **Home / Sobre o projeto** — o que é, para quem, com quem
- **Metodologia** — abordagem, etapas, o que entrega
- **Onde acontece** — mapa de escolas / cidades engajadas
- **Galeria** — fotos de campo, registros públicos

### Área restrita (cliente / patrocinador, com login)

- **Dashboard** — visão geral viva: atividades realizadas, escolas engajadas, próximos eventos, % de execução
- **Relatório semanal** — disparado toda sexta, com análise dos pontos altos da semana
- **Aprovações de peças** — peças gráficas em fila, cliente aprova/comenta
- **Diário de campo** — cronológico, fotos/vídeos/registros do que está acontecendo
- **Informações comerciais** — o que foi vendido, metas, atividades contratadas, metodologia aplicada
- **Engajamento** — cidades, secretarias, escolas, produtor local

---

## 6. Fluxo da semana (exemplo)

**Segunda a quinta** — equipe atualiza ClickUp normalmente (tarefas, fotos, registros).

**Sexta-feira de manhã** — Cloud Code roda automático:
1. Lê todas as atualizações do ClickUp da semana
2. Lê arquivos novos no Google Drive (fotos / vídeos)
3. Atualiza dados do portal (dashboard, diário de campo)
4. Gera análise da semana: o que avançou, o que travou, pontos altos
5. Monta email com link para o dashboard + highlights
6. Salva como **rascunho** no Gmail

**Sexta à tarde** — responsável revisa o rascunho, ajusta se preciso, dispara.

---

## 7. Fluxo de peça gráfica

1. Equipe identifica que precisa de uma peça (ex: cartaz de oficina em Itapoá)
2. Cria task no ClickUp com tipo de peça + dados (texto, data, escola)
3. Cloud Code lê a task, identifica o template Figma correto
4. Via Figma API, popula o template com os dados + logomarca/cores do cliente já aprovadas no carrê
5. Exporta em alta resolução (PDF/TIFF) e sobe para área de aprovações no portal
6. Cliente entra no portal, aprova ou comenta
7. Se aprovado, arquivo final fica disponível para impressão

**Importante:** geração de imagem por IA (DALL-E, Midjourney) **não** entra no fluxo de impressão — não tem consistência suficiente. Tudo passa por template Figma.

---

## 8. Fases de implementação

### Fase 1 — Esqueleto (essa fase, agora)
- Estrutura de pastas e arquivos
- Blueprint (este documento)
- Mockup HTML do portal piloto Itapoá (já tem; vamos refinar)
- Documentação de fluxos de automação

### Fase 2 — Portal estático funcional
- Portar o mockup para WordPress
- Subdomínio `itapoa.ntics.com.br` configurado
- Área pública navegável
- Login simples para área restrita (cliente vê dados mockados primeiro)

### Fase 3 — Integração de dados
- Cloud Code conectado ao ClickUp do projeto Itapoá
- Dashboard puxa dados reais
- Diário de campo alimentado por arquivos do Google Drive

### Fase 4 — Automações
- Relatório semanal automático (rascunho no Gmail)
- Aprovação de peças (upload + workflow do cliente)
- Notificações para a equipe

### Fase 5 — Templating
- Generalizar tudo para virar template replicável
- Documentar como criar projeto novo a partir do template
- Treinar equipe

### Fase 6 — Peças gráficas
- Templates Figma para cada tipo de peça (banner, cartaz, camiseta, etc.)
- Integração Figma API ↔ Cloud Code
- Pipeline de aprovação visual no portal

---

## 9. Decisões em aberto

| # | Decisão | Status |
|---|---|---|
| 1 | Onde mora dado estruturado: ficar em ClickUp ou migrar para Airtable? | **Testar primeiro com ClickUp + Sheets** |
| 2 | Login do cliente: WordPress nativo ou solução custom? | Avaliar na fase 2 |
| 3 | Dashboard: HTML custom dentro do WP, ou Metabase embed? | Avaliar na fase 3 |
| 4 | Hospedagem dos arquivos para impressão: Google Drive ou Dropbox? | Manter Google Drive |
| 5 | Identidade visual do portal: tema único ou customizável por patrocinador? | Decidir antes da fase 2 |

---

## 10. Riscos identificados

- **API do Google Docs é lenta para edição** — mitigação: Cloud Code cria documentos novos quando precisa formatar, edita Sheets que é mais rápido
- **Geração de imagem por IA não bate qualidade de impressão** — mitigação: tudo via template Figma
- **Responsáveis não querem aprender ferramenta nova** — mitigação: WordPress + Google Drive já são conhecidos
- **Cliente quer ver coisas que ainda não temos** — mitigação: dashboard começa com o que dá hoje, evolui com feedback
