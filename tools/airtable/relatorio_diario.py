"""
Cria um registro de Relatório Diário no Airtable.
Pode ser chamado manualmente no terminal ao fim do dia.

Uso:
  cd tools/airtable
  python relatorio_diario.py
  python relatorio_diario.py --projeto 132 --data 2026-05-26
"""
import sys
import argparse
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import upsert_records
import yaml

CONFIG_PATH = Path(__file__).parent / "config.yaml"

PROJETOS = {
    "128": "Festival Agricultura Sustentável",
    "129": "Agrofuturo Cultural nas Escolas",
    "132": "Estação Samarco, Territórios do Futuro",
}


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError("config.yaml não encontrado. Rode setup_base.py primeiro.")
    return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8"))


def escolher_projeto(pre: str | None) -> tuple[str, str]:
    if pre and pre in PROJETOS:
        return pre, PROJETOS[pre]
    print("\nProjeto:")
    for k, v in PROJETOS.items():
        print(f"  [{k}] {v}")
    while True:
        c = input("Código do projeto: ").strip()
        if c in PROJETOS:
            return c, PROJETOS[c]
        print("  Inválido. Use 128, 129 ou 132.")


def input_multiline(prompt: str) -> str:
    """Lê input multi-linha até linha em branco dupla ou linha com só '.'."""
    print(f"{prompt} (termine com '.' numa linha vazia):")
    lines = []
    while True:
        line = input()
        if line.strip() == ".":
            break
        lines.append(line)
    return "\n".join(lines).strip()


def main():
    parser = argparse.ArgumentParser(description="Cria relatório diário no Airtable.")
    parser.add_argument("--projeto", help="Código do projeto (128, 129, 132)")
    parser.add_argument("--data", help="Data no formato YYYY-MM-DD (padrão: hoje)")
    parser.add_argument("--responsavel", help="Nome do responsável", default="Lucas Rotta")
    args = parser.parse_args()

    config = load_config()
    table_name = config["tables"]["Relatório Diário"]

    codigo, nome = escolher_projeto(args.projeto)
    data = args.data or str(date.today())
    responsavel = args.responsavel

    print(f"\nRelatório Diário — {nome} — {data}")
    print("-" * 50)

    feito = input_multiline("O que foi feito hoje")
    proximos = input_multiline("Próximos passos")
    bloqueios = input_multiline("Bloqueios / impedimentos (deixe vazio se não houver)")

    record = {
        "Data": data,
        "Projeto": nome,
        "Código Projeto": codigo,
        "O que foi feito": feito,
        "Próximos passos": proximos,
        "Bloqueios": bloqueios or "Nenhum",
        "Responsável": responsavel,
    }

    print("\nCriando registro no Airtable...")
    result = upsert_records(table_name, [record], ["Código Projeto", "Data"])
    criados = len(result.get("createdRecords", []))
    atualizados = len(result.get("updatedRecords", []))
    print(f"OK — criados: {criados} | atualizados: {atualizados}")
    print(f"Relatório de {data} registrado para {nome}.")


if __name__ == "__main__":
    main()
