"""
memory.py — Gerencia o histórico persistente de conversas (salvo em JSON local).
"""
import json
from datetime import datetime
from pathlib import Path

_DIR  = Path("memory")
_FILE = _DIR / "conversations.json"


def _ensure():
    _DIR.mkdir(exist_ok=True)
    if not _FILE.exists():
        _FILE.write_text("[]", encoding="utf-8")


def load_all() -> list:
    """Retorna todas as conversas salvas, ordenadas da mais recente à mais antiga."""
    _ensure()
    try:
        data = json.loads(_FILE.read_text(encoding="utf-8"))
        return sorted(data, key=lambda c: c["timestamp"], reverse=True)
    except Exception:
        return []


def save(name: str, messages: list) -> str:
    """Salva uma conversa. Retorna o ID gerado."""
    _ensure()
    convs = load_all()
    cid = datetime.now().strftime("%Y%m%d%H%M%S%f")
    convs.insert(0, {
        "id":        cid,
        "name":      name.strip() or f"Conversa {datetime.now().strftime('%d/%m %H:%M')}",
        "timestamp": datetime.now().isoformat(),
        "messages":  [m for m in messages if m["role"] in ("user", "assistant")],
    })
    _FILE.write_text(json.dumps(convs, ensure_ascii=False, indent=2), encoding="utf-8")
    return cid


def delete(cid: str):
    """Remove uma conversa pelo ID."""
    _ensure()
    convs = [c for c in load_all() if c["id"] != cid]
    _FILE.write_text(json.dumps(convs, ensure_ascii=False, indent=2), encoding="utf-8")


def get(cid: str) -> dict | None:
    """Retorna uma conversa específica pelo ID, ou None."""
    return next((c for c in load_all() if c["id"] == cid), None)
