# Fluxos de Automação — Cloud Code

**Status:** especificação (ainda não implementado)
**Pré-requisito:** ClickUp configurado com o padrão de campos descrito na seção 4

---

## 1. Visão geral

Cloud Code atua como a camada de orquestração entre o ClickUp (fonte da verdade dos dados) e o portal WordPress (apresentação ao cliente). Não substitui ferramentas — orquestra.

Três fluxos principais nesta fase:

1. **Sincronização diária** — lê ClickUp + Drive, atualiza dashboard e diário de campo
2. **Relatório semanal de sexta** — gera análise + rascunho de email
3. **Geração de peça gráfica** — popula template Figma sob demanda

---

## 2. Fluxo 1 — Sincronização diária

**Quando roda:** todos os dias úteis, 07h

**O que faz:**

```
1. Lê do ClickUp:
   - Tarefas concluídas nas últimas 24h
   - Comentários novos em qualquer tarefa do projeto
   - Status atualizados
   - Custom fields modificados (presença, registros, métricas)

2. Lê do Google Drive:
   - Arquivos novos na pasta /projetos/itapoa/diario-campo/
   - Identifica tipo: foto, vídeo, documento
   - Extrai metadados (data, escola, oficina)

3. Processa:
   - Agrupa por escola + por dia
   - Cria entrada nova no diário de campo
   - Recalcula métricas do dashboard (estudantes ativos, oficinas, %)
   - Identifica alertas (presença abaixo de 80%, atrasos)

4. Atualiza:
   - Posta entradas via API WordPress (custom post type "diario")
   - Atualiza valores do dashboard (custom post type "metricas")
   - Cria notificação interna se houver alerta
```

**Onde mora o código:**
- Script principal: `scripts/sincronizacao-diaria.py` (a criar)
- Roda em servidor (Vercel cron, ou GitHub Actions, ou cron no servidor WordPress)

**Prompt que o Cloud Code recebe:**
```
Você é o agente de sincronização do projeto {projeto_id}.

Leia as atualizações do ClickUp das últimas 24h via API. Para cada
atualização, classifique como: nova oficina realizada, registro de
campo, marco atingido, alerta de presença, ou ruído (ignorar).

Para entradas relevantes, gere uma versão limpa em português para
exibição pública, sem jargão interno. Mantenha tom factual.

Saída: JSON com array de objetos { tipo, escola, data, titulo,
descricao, fotos[], severidade }.
```

---

## 3. Fluxo 2 — Relatório semanal de sexta

**Quando roda:** toda sexta-feira, 08h

**O que faz:**

```
1. Lê:
   - Todas as atividades da semana (segunda a sexta)
   - Dashboard atualizado
   - Diário de campo dos últimos 7 dias
   - Métricas comparadas com semana anterior

2. Analisa:
   - O que avançou: oficinas realizadas, parcerias fechadas, marcos
   - O que travou: oficinas canceladas, presença baixa, atrasos
   - Destaques: registros únicos, conquistas inesperadas
   - Próximos passos: o que está agendado para a próxima semana

3. Gera:
   - Análise narrativa em 3-4 parágrafos
   - Lista de destaques (3 a 5 itens)
   - Lista de pontos de atenção (0 a 3 itens)
   - Lista de próximos eventos

4. Compõe email:
   - Assunto: "Relatório semanal #{N} — {projeto} — {data_inicio} a {data_fim}"
   - Corpo: saudação personalizada + análise + link para o dashboard
   - Anexo: nenhum (tudo no portal)

5. Salva como RASCUNHO no Gmail do responsável.
   Humano revisa, ajusta, dispara.
```

**Prompt que o Cloud Code recebe:**
```
Você está escrevendo o relatório semanal #{N} do projeto {projeto}
para {patrocinador}.

Tom: profissional mas próximo, factual, sem hype. Como se você
estivesse contando para um sócio o que aconteceu na semana.

Estrutura:
1. Abertura (1 frase com o highlight da semana)
2. O que avançou (1-2 parágrafos)
3. O que pede atenção (1 parágrafo, ou pule se não houver)
4. Destaques específicos (bullets curtos)
5. Próxima semana (bullets do que está agendado)

Limite total: 400 palavras. Não invente dados — use só o que
está no ClickUp e no Drive.

Saída: texto pronto para email + assunto sugerido.
```

---

## 4. Estrutura esperada do ClickUp

Para os fluxos funcionarem, cada projeto precisa de uma estrutura mínima no ClickUp:

### Lista por projeto: `NEG-ITAPOA-2026`

### Custom fields obrigatórios em cada task:

| Campo | Tipo | Uso |
|---|---|---|
| `Tipo` | dropdown | Oficina · Registro · Articulação · Comunicação · Aprovação |
| `Escola` | dropdown | EEB Itapoá · EMEF Bela Vista · EEB Pontal · EMEF Tabuleiro · EEB Barra do Saí |
| `Data execução` | date | Quando aconteceu (não a deadline) |
| `Estudantes presentes` | number | Para tasks tipo Oficina |
| `Etapa` | dropdown | Imersão · Vocação · Modelagem · Festival |
| `Visível ao cliente` | checkbox | Default `true`; marca `false` para coisas internas |
| `Fotos` | URL | Link para pasta no Drive com os registros |
| `Severidade` | dropdown | Normal · Destaque · Atenção · Crítico |

### Status que importam:

- `Backlog` → `Em andamento` → `Concluído` → `Reportado ao cliente`

Quando uma task chega em `Concluído` e tem `Visível ao cliente = true`, ela vira candidato a entrar no próximo diário de campo / relatório.

---

## 5. Fluxo 3 — Geração de peça gráfica

**Quando roda:** quando uma task de tipo `Comunicação` é criada com status `Pronto para gerar`

**O que faz:**

```
1. Lê a task:
   - Tipo de peça (cartaz A2, banner 3x1m, flyer A5, camiseta, etc.)
   - Texto principal
   - Data / local / oficina
   - Identifica template Figma correspondente

2. Carrega template Figma via API:
   - Acessa o file_id pré-cadastrado por tipo de peça
   - Identifica layers de texto e imagem (placeholders)

3. Popula:
   - Texto: substitui placeholders pelos campos da task
   - Cores: aplica paleta do cliente (já no carrê aprovado)
   - Logomarca: insere logo correta (cliente + Lei Rouanet + NTICS)

4. Exporta:
   - Alta resolução (PDF para impressão, PNG para digital)
   - Salva no Drive: /projetos/itapoa/aprovacoes/pendentes/

5. Cria entrada de aprovação:
   - Posta no portal WordPress (custom post type "aprovacao")
   - Status: AGUARDANDO
   - Notifica responsável NTICS

6. Quando cliente aprova no portal:
   - Move arquivo: /pendentes/ → /aprovadas/
   - Atualiza status no ClickUp para `Aprovado`
   - Notifica equipe de produção
```

**Templates Figma a criar (fase 6):**

- `cartaz-a2-evento` — placeholders: título, data, local, horário, escolas envolvidas
- `cartaz-a2-oficina` — placeholders: tema, oficineiro, data, escola
- `banner-3x1` — placeholders: título, subtítulo, etapa
- `flyer-a5-digital` — placeholders: convite, data, link
- `camiseta-frente-costas` — placeholders: turma, número
- `apresentacao-institucional` — slides editáveis com dados do projeto

Cada template tem variantes para 5 paletas (uma por patrocinador comum).

---

## 6. Permissões e credenciais

| Sistema | Credencial | Onde mora |
|---|---|---|
| ClickUp | API Token | Vault / .env do servidor |
| Google Drive | OAuth Service Account | JSON no servidor |
| Gmail (rascunhos) | OAuth do responsável | JSON no servidor |
| WordPress | App Password | .env |
| Figma | Personal Access Token | .env |

**Nunca** colocar credenciais em código versionado. Usar `.env` + `.gitignore`.

---

## 7. Tratamento de erros

Para cada fluxo, prever:

- **Timeout / API offline:** retry 3x com backoff, depois log + notificação ao admin
- **Dado incompleto na task:** pular a task, registrar no log, não bloquear o lote
- **Template Figma corrompido:** falhar a peça específica, manter as demais
- **Email não salvou como rascunho:** logar erro, notificar via Slack/WhatsApp

Log centralizado em `logs/automacao-{YYYYMMDD}.log` — Cloud Code revisa semanalmente.

---

## 8. Roadmap de implementação

| Fase | Entregável | Esforço estimado |
|---|---|---|
| 4.1 | Setup ClickUp com custom fields padrão | 1 dia |
| 4.2 | Script de sincronização diária (read-only, dry-run) | 2-3 dias |
| 4.3 | Posting no WordPress via API | 2 dias |
| 4.4 | Relatório semanal + Gmail draft | 2 dias |
| 4.5 | Testes em produção com projeto Itapoá | 1 semana |
| 4.6 | Templates Figma + geração de peça | 5-7 dias |
| 4.7 | Workflow de aprovação no portal | 3 dias |

Total estimado para o piloto completo: **~4 semanas de trabalho focado**.

---

## 9. O que NÃO vai automatizar (mantém humano)

- Decisão de qual oficina fazer quando
- Escolha de parceiros e produtores locais
- Aprovação final de peças (cliente decide)
- Conversa com secretaria de educação
- Negociação de espaço, equipamento, logística
- Conteúdo pedagógico das oficinas
- Qualquer comunicação externa não-programática

A automação cuida do **transporte, organização e formatação** dos dados. As decisões e relacionamentos seguem com pessoas.
