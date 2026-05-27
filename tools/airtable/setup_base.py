"""
Cria as 8 tabelas no Airtable e salva os IDs em config.yaml.
Rodar UMA VEZ após criar o base vazio no Airtable.

Uso:
  cd tools/airtable
  python setup_base.py
"""
import sys
import yaml
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import meta_post, meta_get, BASE_ID

CONFIG_PATH = Path(__file__).parent / "config.yaml"

TABLES = [
    {
        "name": "Projetos",
        "description": "Registro mestre de cada projeto NTICS.",
        "fields": [
            {"name": "Código", "type": "singleLineText"},
            {"name": "Nome", "type": "singleLineText"},
            {"name": "Patrocinador", "type": "singleLineText"},
            {"name": "Sub-marca", "type": "singleLineText"},
            {"name": "Lei", "type": "singleSelect", "options": {"choices": [
                {"name": "Rouanet"}, {"name": "Corporativo direto"}, {"name": "Pronac"}, {"name": "Outro"},
            ]}},
            {"name": "PRONAC", "type": "singleLineText"},
            {"name": "Empresa Proponente", "type": "singleLineText"},
            {"name": "CNPJ Proponente", "type": "singleLineText"},
            {"name": "Fase", "type": "singleSelect", "options": {"choices": [
                {"name": "pre-kickoff"}, {"name": "kickoff-pendente"}, {"name": "execucao"},
                {"name": "encerramento"}, {"name": "concluido"},
            ]}},
            {"name": "Orçamento Original (R$)", "type": "number", "options": {"precision": 2}},
            {"name": "Orçamento Aprovado (R$)", "type": "number", "options": {"precision": 2}},
            {"name": "Executor Direto", "type": "singleLineText"},
            {"name": "Responsável Técnico", "type": "singleLineText"},
            {"name": "Pasta Drive", "type": "url"},
            {"name": "ClickUp Lista", "type": "url"},
            {"name": "Atualizado em", "type": "date", "options": {"dateFormat": {"name": "iso"}}},
            {"name": "Observações", "type": "multilineText"},
        ],
    },
    {
        "name": "TAP",
        "description": "Termo de Abertura de Projeto por projeto.",
        "fields": [
            {"name": "Projeto", "type": "singleLineText"},
            {"name": "Código", "type": "singleLineText"},
            {"name": "Status TAP", "type": "singleSelect", "options": {"choices": [
                {"name": "rascunho"}, {"name": "pendente formal"}, {"name": "assinado"},
            ]}},
            {"name": "Objetivo Geral", "type": "multilineText"},
            {"name": "Escopo", "type": "multilineText"},
            {"name": "Cidades", "type": "multilineText"},
            {"name": "Público-alvo", "type": "multilineText"},
            {"name": "Entregas Principais", "type": "multilineText"},
            {"name": "Resultados Esperados", "type": "multilineText"},
            {"name": "Legislação / Programa", "type": "singleLineText"},
            {"name": "Observações", "type": "multilineText"},
        ],
    },
    {
        "name": "Metodologias",
        "description": "Temas de oficinas e trilhas formativas por projeto.",
        "fields": [
            {"name": "ID", "type": "singleLineText"},
            {"name": "Projeto", "type": "singleLineText"},
            {"name": "Código Projeto", "type": "singleLineText"},
            {"name": "Nome", "type": "singleLineText"},
            {"name": "Tipo", "type": "singleSelect", "options": {"choices": [
                {"name": "oficina-cultural-minc"}, {"name": "oficina-tematica"},
                {"name": "trilha-formativa"}, {"name": "peça-teatro"},
                {"name": "evento"}, {"name": "seminario"}, {"name": "feira"},
            ]}},
            {"name": "Conceitos / Tópicos", "type": "multilineText"},
            {"name": "Atividade / Metodologia", "type": "multilineText"},
            {"name": "Carga Horária", "type": "singleLineText"},
            {"name": "ODS", "type": "multilineText"},
            {"name": "Linguagem MinC", "type": "singleLineText"},
            {"name": "Observações", "type": "multilineText"},
        ],
    },
    {
        "name": "KPIs e Metas",
        "description": "Indicadores com meta e realizado por projeto.",
        "fields": [
            {"name": "Projeto", "type": "singleLineText"},
            {"name": "Código Projeto", "type": "singleLineText"},
            {"name": "Indicador", "type": "singleLineText"},
            {"name": "Meta", "type": "singleLineText"},
            {"name": "Realizado", "type": "singleLineText"},
            {"name": "Unidade", "type": "singleLineText"},
            {"name": "Status", "type": "singleSelect", "options": {"choices": [
                {"name": "a confirmar"}, {"name": "no prazo"}, {"name": "atrasado"},
                {"name": "em risco"}, {"name": "atingido"},
            ]}},
            {"name": "Observações", "type": "multilineText"},
        ],
    },
    {
        "name": "Execução",
        "description": "Entregas de design e conteúdo por projeto, com status.",
        "fields": [
            {"name": "ID Entregável", "type": "singleLineText"},
            {"name": "Projeto", "type": "singleLineText"},
            {"name": "Código Projeto", "type": "singleLineText"},
            {"name": "Nome", "type": "singleLineText"},
            {"name": "Bloco", "type": "singleSelect", "options": {"choices": [
                {"name": "A - Pré-projeto digital"}, {"name": "B - Material pedagógico"},
                {"name": "C - Estrutura de campo"}, {"name": "D - Certificados"},
                {"name": "Conteúdo / Redes"}, {"name": "Operacional"}, {"name": "Outro"},
            ]}},
            {"name": "Tipo", "type": "singleLineText"},
            {"name": "Status", "type": "singleSelect", "options": {"choices": [
                {"name": "pendente"}, {"name": "em andamento"}, {"name": "aguardando aprovação"},
                {"name": "aprovado"}, {"name": "concluído"}, {"name": "cancelado"},
            ]}},
            {"name": "Prioridade", "type": "singleSelect", "options": {"choices": [
                {"name": "P1"}, {"name": "P2"}, {"name": "P3"},
            ]}},
            {"name": "Dependência", "type": "multilineText"},
            {"name": "Skill / Ferramenta", "type": "singleLineText"},
            {"name": "Observações", "type": "multilineText"},
        ],
    },
    {
        "name": "Aprovação de Peças",
        "description": "Fluxo de aprovação de comunicação por projeto.",
        "fields": [
            {"name": "Peça", "type": "singleLineText"},
            {"name": "Projeto", "type": "singleLineText"},
            {"name": "Código Projeto", "type": "singleLineText"},
            {"name": "Tipo", "type": "singleLineText"},
            {"name": "Status", "type": "singleSelect", "options": {"choices": [
                {"name": "produção"}, {"name": "revisão interna"}, {"name": "enviado para cliente"},
                {"name": "aguardando aprovação"}, {"name": "aprovado"}, {"name": "revisão solicitada"},
                {"name": "reprovado"}, {"name": "publicado"},
            ]}},
            {"name": "Aprovador Interno", "type": "singleLineText"},
            {"name": "Aprovador Cliente", "type": "singleLineText"},
            {"name": "Canal de Aprovação", "type": "singleLineText"},
            {"name": "Data Envio", "type": "date", "options": {"dateFormat": {"name": "iso"}}},
            {"name": "Prazo Resposta", "type": "singleLineText"},
            {"name": "Link Drive / Arquivo", "type": "url"},
            {"name": "Observações", "type": "multilineText"},
        ],
    },
    {
        "name": "Financeiro",
        "description": "Frentes de custo e orçamento por projeto.",
        "fields": [
            {"name": "ID Frente", "type": "singleLineText"},
            {"name": "Projeto", "type": "singleLineText"},
            {"name": "Código Projeto", "type": "singleLineText"},
            {"name": "Categoria", "type": "singleLineText"},
            {"name": "Descrição", "type": "multilineText"},
            {"name": "Fornecedor", "type": "singleLineText"},
            {"name": "Custo Estimado (R$)", "type": "singleLineText"},
            {"name": "Aprovado (R$)", "type": "number", "options": {"precision": 2}},
            {"name": "Realizado (R$)", "type": "number", "options": {"precision": 2}},
            {"name": "Status", "type": "singleSelect", "options": {"choices": [
                {"name": "a cotar"}, {"name": "orçado"}, {"name": "aprovado"},
                {"name": "contratado"}, {"name": "pago"}, {"name": "cancelado"},
            ]}},
            {"name": "Observações", "type": "multilineText"},
        ],
    },
    {
        "name": "Relatório Diário",
        "description": "Log diário de execução por projeto.",
        "fields": [
            {"name": "Data", "type": "date", "options": {"dateFormat": {"name": "iso"}}},
            {"name": "Projeto", "type": "singleLineText"},
            {"name": "Código Projeto", "type": "singleLineText"},
            {"name": "O que foi feito", "type": "multilineText"},
            {"name": "Próximos passos", "type": "multilineText"},
            {"name": "Bloqueios", "type": "multilineText"},
            {"name": "Responsável", "type": "singleLineText"},
        ],
    },
]


def create_tables() -> dict:
    """Cria as 8 tabelas. Ignora tabelas já existentes pelo nome."""
    if not BASE_ID:
        raise RuntimeError("AIRTABLE_BASE_ID não definido no .env")

    # Tabelas existentes
    existing = {t["name"]: t["id"] for t in meta_get(f"/bases/{BASE_ID}/tables").get("tables", [])}

    table_ids = {}
    for table in TABLES:
        name = table["name"]
        if name in existing:
            print(f"  [skip] '{name}' já existe — id: {existing[name]}")
            table_ids[name] = existing[name]
            continue
        print(f"  [criar] '{name}'...")
        result = meta_post(f"/bases/{BASE_ID}/tables", table)
        table_ids[name] = result["id"]
        print(f"         id: {result['id']}")
        time.sleep(0.3)

    return table_ids


def save_config(table_ids: dict):
    config = {"base_id": BASE_ID, "tables": table_ids}
    CONFIG_PATH.write_text(yaml.dump(config, allow_unicode=True, default_flow_style=False), encoding="utf-8")
    print(f"\nConfig salvo em: {CONFIG_PATH}")


if __name__ == "__main__":
    import time
    print(f"Base ID: {BASE_ID}\n")
    ids = create_tables()
    save_config(ids)
    print("\nSetup concluído. Próximo passo: python sync_projects.py")
