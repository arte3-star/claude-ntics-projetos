"""Shared helpers for Airtable integration."""
import os
import time
import requests
import urllib3
from pathlib import Path
from dotenv import load_dotenv

# Windows: certifi doesn't include the Windows certificate store.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Load .env from project root or tools/airtable/
_root = Path(__file__).parent.parent.parent
load_dotenv(_root / ".env")
load_dotenv(Path(__file__).parent / ".env")

BASE_URL = "https://api.airtable.com/v0"
META_URL = "https://api.airtable.com/v0/meta"

TOKEN = os.environ.get("AIRTABLE_TOKEN", "")
BASE_ID = os.environ.get("AIRTABLE_BASE_ID", "")


def _headers():
    if not TOKEN:
        raise RuntimeError("AIRTABLE_TOKEN não definido. Crie o arquivo .env com a chave.")
    return {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}


def _request(method: str, url: str, **kwargs) -> dict:
    """Faz requisição com retry em rate limit (429)."""
    for attempt in range(5):
        resp = requests.request(method, url, headers=_headers(), verify=False, **kwargs)
        if resp.status_code == 429:
            wait = int(resp.headers.get("Retry-After", 30))
            print(f"  Rate limit — aguardando {wait}s...")
            time.sleep(wait)
            continue
        resp.raise_for_status()
        return resp.json()
    raise RuntimeError(f"Rate limit persistente após 5 tentativas: {url}")


def get(path: str) -> dict:
    return _request("GET", f"{BASE_URL}{path}")


def post(path: str, body: dict) -> dict:
    return _request("POST", f"{BASE_URL}{path}", json=body)


def patch(path: str, body: dict) -> dict:
    return _request("PATCH", f"{BASE_URL}{path}", json=body)


def meta_get(path: str) -> dict:
    return _request("GET", f"{META_URL}{path}")


def meta_post(path: str, body: dict) -> dict:
    return _request("POST", f"{META_URL}{path}", json=body)


def create_records(table_id_or_name: str, records: list[dict]) -> list[dict]:
    """Envia registros em lotes de 10 (limite da API)."""
    created = []
    for i in range(0, len(records), 10):
        batch = records[i:i + 10]
        result = post(f"/{BASE_ID}/{table_id_or_name}", {"records": [{"fields": r} for r in batch]})
        created.extend(result.get("records", []))
        time.sleep(0.2)
    return created


def upsert_records(table_id_or_name: str, records: list[dict], key_fields: list[str]) -> dict:
    """Upsert por campos-chave (evita duplicatas ao re-rodar o sync)."""
    all_results = {"createdRecords": [], "updatedRecords": []}
    for i in range(0, len(records), 10):
        batch = records[i:i + 10]
        body = {
            "performUpsert": {"fieldsToMergeOn": key_fields},
            "records": [{"fields": r} for r in batch],
        }
        result = patch(f"/{BASE_ID}/{table_id_or_name}", body)
        all_results["createdRecords"].extend(result.get("createdRecords", []))
        all_results["updatedRecords"].extend(result.get("updatedRecords", []))
        time.sleep(0.2)
    return all_results
