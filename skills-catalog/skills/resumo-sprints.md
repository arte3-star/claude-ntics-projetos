---
name: resumo-sprints
description: |
  Lê todas as reuniões de sprint de coordenação da semana e gera um resumo consolidado, organizado por pessoa → projeto → decisões → alertas, dentro de uma subpágina semanal do documento "Sprints" do ClickUp (página "Resumo das Sprints").

  Acione SEMPRE que o usuário disser: "gera o resumo das sprints", "resumo das sprints da semana", "consolida as sprints", "resumo semanal das sprints", "rodar a rotina de sprints", "resumo das reuniões de sprint", ou qualquer variação. Também acione quando a rotina agendada de segunda-feira disparar.

  Esta skill substitui a leitura manual das reuniões de cada coordenador toda semana. Use proativamente quando o contexto for consolidar as sprints da equipe para o Lucas.
---

# Resumo das Sprints — NTICS Projetos

Você lê as reuniões de sprint de cada coordenador na semana e produz um **resumo consolidado** numa subpágina semanal. É a rotina que roda **toda segunda-feira no fim do dia** (e sob demanda).

## Princípios

1. **Nunca inventar.** Só entra o que foi dito na reunião / está na página de sprint / na transcrição. Se algo não foi lido, diga qual pessoa e por quê — nunca finja que cobriu tudo.
2. **Reconciliar referências de projeto.** Nas reuniões o mesmo projeto aparece como número (`125`), nome (`Gastronomia GRU`) ou patrocinador (`GRU`, `CNH`, `Peróxidos`). Unifique num único bloco por projeto, usando a tabela canônica abaixo. Título do bloco: `📌 Projeto <nº> — <nome curto> · <cidade/patrocinador>`.
3. **Separar decisão de status.** O resumo prioriza **decisões** (o que foi decidido/combinado/acordado) e **alertas** (riscos, travas, pontos de atenção, prazos apertados). Status corrido vira contexto de uma linha, não a lista inteira.
4. **Estrutura fixa.** Pessoa → projeto → Decisões → ⚠️ Alertas. Sem tabelas markdown (o ClickUp renderiza pipes como texto — usar cabeçalhos + bullets).
5. **Uma subpágina por semana.** Cada rodada cria (ou preenche) a subpágina `Semana DD/MM-DD/MM` sob a página "Resumo das Sprints".

---

## Destino (fixo)

- **Documento (doc_id):** `8cje8p1-59231` — documento "Sprints" (workspace `<ID_CLICKUP>`).
- **Página-mãe do resumo:** `Resumo das Sprints` → `parent_page_id = 8cje8p1-56231`.
- A subpágina da semana vai **dentro** de `8cje8p1-56231`, nomeada `Semana DD/MM-DD/MM` (ex.: `Semana 20/07-25/07`).
- URL do doc: https://app.clickup.com/<ID_CLICKUP>/v/dc/8cje8p1-59231/8cje8p1-56231

## Fontes (por pessoa)

O documento é organizado por **coordenador**, cada um com páginas semanais de sprint. Seções (parent_page_id):

| Coordenador | Seção (parent_page_id) | Formato típico da página da semana |
|-------------|------------------------|-------------------------------------|
| Jéssica Lora | `8cje8p1-33851` | Relatório estruturado (Relatório Semanal, por projeto) + transcrição bruta no fim |
| Mayara Ferreira | `8cje8p1-33871` | Varia (às vezes vazia — pode preencher ao longo da semana) |
| Raíza Araújo | `8cje8p1-33831` | Link para **Google Doc** (Observações do Gemini + transcrição) |
| Bruna Seibel | `8cje8p1-33911` | Cargo dissolvido — só incluir se houver sprint recente |

> A lista de coordenadores pode mudar. Sempre liste as páginas do doc antes de rodar (`list_document_pages`) e cubra quem tiver sprint na semana-alvo.

## Tabela canônica projeto → coordenador (para reconciliação)

| Projeto | Nome curto · patrocinador/cidade | Coordenador |
|---------|-----------------------------------|-------------|
| #115 | Cultura Robótica 2ED · SP + Curitiba (Peróxidos / BTG-Tupi) | Raíza |
| #116 | Cultura Robótica · Áster | Raíza / Mayara |
| #117 | Teatro · Whirlpool | Raíza |
| #119 | PEC · Sylvamo | Raíza |
| #124 | Gastronomia · COMPAGAS | Mayara |
| #125 | Gastronomia · GRU (Guarulhos) | Jéssica |
| #126 | Ecoarte Container · GRU (Guarulhos) | Jéssica |
| #127 | PIE · GRU + Sotreq (Guarulhos) | Jéssica |
| #128 | Festival Agricultura · CNH Case IH (PR) | Raíza |
| #129 | Agrofuturo · CNH (MT) | Raíza |
| TAG | Negócio Cultural 3ED (#121) | Abílio / Fernando |

Itens sem número (ex.: "Exposição do aeroporto", "Comunicação do caminhão") entram como bloco próprio dentro do projeto-pai quando identificável (a exposição/caminhão de Guarulhos são do 125/127).

---

## Passo a passo

### 1. Determinar a semana-alvo
- Rodando na segunda-feira: a semana é **segunda → sábado** da própria semana (ex.: rodando 20/07, semana `20/07-25/07`).
- Se o usuário pedir uma semana específica, use-a.
- Nome da subpágina: `Semana DD/MM-DD/MM`.

### 2. Listar as páginas do doc
- `clickup_list_document_pages(document_id="8cje8p1-59231", max_page_depth=-1)`.
- Em cada seção de coordenador, achar a página da semana-alvo. Os nomes variam: `Sprint DD/MM`, `DD/MM`, `SprintDD/MM`. Compare pela data (a data da sprint costuma ser a segunda-feira da semana, mas pode ser outro dia — pegue a página cuja data cai na semana-alvo).

### 3. Ler cada fonte
- `clickup_get_document_pages(document_id, page_ids=[...], content_format="text/md")`.
- **Se a página tem relatório estruturado** (Jéssica): use as seções por projeto (Atualizações / Próximos Passos) e refine com a transcrição para extrair decisões e alertas.
- **Se a página é só um link de Google Doc** (Raíza): extraia o `fileId` da URL e leia com `read_file_content(fileId)` (Google Drive MCP). O Google Doc traz um resumo do Gemini (Resumo / Próximas etapas / Detalhes) + transcrição — ótima base; confirme decisões/alertas na transcrição.
- **Se a página está vazia**: registre "sem sprint registrada nesta semana" para essa pessoa. Não invente.

### 4. Extrair por projeto
Para cada projeto falado na reunião de cada pessoa:
- **Decisões**: o que foi decidido/combinado, prazos definidos, contratações fechadas, mudanças de escopo, próximos marcos com data.
- **⚠️ Alertas**: riscos, travas, dependências, prazos apertados, problemas com fornecedor/equipe, budget apertado, pendências que podem atrasar.
- Junte referências do mesmo projeto (número/nome/patrocinador) num bloco só.

### 5. Montar e gravar a subpágina
- Formato exato em `references/formato-saida.md`.
- Cabeçalho com a janela da semana, quais reuniões foram lidas e quem ficou de fora.
- **Se a subpágina `Semana DD/MM-DD/MM` já existe** sob `8cje8p1-56231`: preencher/atualizar com `clickup_update_document_page(document_id, page_id, content, name)`. (Atenção: `update` **substitui** o conteúdo inteiro.)
- **Se não existe**: criar com `clickup_create_document_page(document_id="8cje8p1-59231", parent_page_id="8cje8p1-56231", name="Semana DD/MM-DD/MM", content=..., content_format="text/md")`.

### 6. Fechar
- Informar ao Lucas: link da subpágina, quantas reuniões foram lidas, quem ficou de fora e por quê.
- Sempre entregar link clicável (padrão do Lucas).

---

## Cuidados NTICS

- **Budget confidencial 128/129**: o valor captado/cheio (~R$660k/R$600k) NÃO entra em nenhum lugar. Só "budget disponível/execução" pode aparecer.
- **Processos por cargo, não pessoa** — mas aqui o resumo é por pessoa que **conduziu a sprint** (coordenador), o que é correto para este artefato.
- **Nomes de fornecedores/equipe** podem entrar (é doc interno operacional), mas trate incidentes com cuidado factual (o que aconteceu, sem julgamento).
- **"Cláudio" = Claude**, **ENITIX/Anityx = NTICS** — grafias de transcrição, não registrar como entidades reais.
