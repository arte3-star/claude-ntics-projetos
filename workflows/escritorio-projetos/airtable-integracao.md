# SOP: Integração Airtable — Projetos NTICS

**Área:** Escritório de Projetos  
**Ferramenta:** Airtable (base "NTICS Projetos")  
**Scripts:** `tools/airtable/`

---

## Quando usar

- Consultar status de entregáveis, KPIs e financeiro dos projetos 128, 129 e 132
- Registrar relatório de trabalho diário
- Atualizar aprovação de peças de comunicação
- Atualizar dados financeiros conforme orçamentos chegarem

---

## Setup inicial (uma vez)

### 1. Criar Personal Access Token

Acesse [airtable.com/create/tokens](https://airtable.com/create/tokens) e crie um token com os scopes:
- `data.records:read`
- `data.records:write`
- `schema.bases:read`
- `schema.bases:write`

### 2. Criar o Base no Airtable

- Acesse [airtable.com](https://airtable.com) e crie um novo base chamado **"NTICS Projetos"**
- Copie o Base ID da URL: `https://airtable.com/appXXXXXXXXXXXXXX/...`

### 3. Configurar `.env` na raiz do projeto

```
AIRTABLE_TOKEN=patXXXXXXXXXXXXXXXX
AIRTABLE_BASE_ID=appXXXXXXXXXXXXXXXX
```

### 4. Instalar dependências

```bash
pip install requests PyYAML python-dotenv
```

### 5. Criar as 8 tabelas

```bash
cd tools/airtable
python setup_base.py
```

Isso cria as tabelas e salva os IDs em `tools/airtable/config.yaml`.

### 6. Popular com dados do SecondBrain

```bash
python sync_projects.py
```

Idempotente: pode ser rodado múltiplas vezes. Usa upsert — não duplica registros.

---

## Uso rotineiro

### Relatório diário (ao fim do dia)

```bash
cd tools/airtable
python relatorio_diario.py
```

Ou passando argumentos:

```bash
python relatorio_diario.py --projeto 132 --data 2026-05-26
```

### Atualizar dados após novas informações

Ao confirmar dados pendentes (orçamento, cidades, interlocutores), atualize **diretamente no Airtable** via interface web, ou atualize o SecondBrain e rode `python sync_projects.py` novamente.

---

## Estrutura das tabelas

| Tabela | Uso | Chave de upsert |
|---|---|---|
| Projetos | Registro mestre | Código |
| TAP | Termo de Abertura | Código |
| Metodologias | Temas, trilhas, eventos | ID |
| KPIs e Metas | Indicadores e metas | Código Projeto + Indicador |
| Execução | Entregas de design e conteúdo | ID Entregável |
| Aprovação de Peças | Fluxo de aprovação | Código Projeto + Peça |
| Financeiro | Frentes de custo | ID Frente |
| Relatório Diário | Log diário | Código Projeto + Data |

---

## Lacunas abertas (atualizar quando chegarem)

| Projeto | Campo | Como atualizar |
|---|---|---|
| 128 | Valor contratado final | Confirmar com Abilio → atualizar Projetos + Financeiro |
| 128 | Interlocutor CNH aprovação | Fernando confirma → atualizar Aprovação de Peças |
| 129 | Cidades de execução | Após kick-off → atualizar TAP + Metodologias |
| 129 | PRONAC e valor | Confirmar → atualizar Projetos + Financeiro |
| 132 | Valor total contratado | Solicitar a Cíntia/Abilio → atualizar Projetos + Financeiro |
| 132 | Orçamento por rubrica | Solicitar breakdown → atualizar Financeiro |
