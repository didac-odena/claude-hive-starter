"""
Routing check hook — detecta si la operacion en curso diverge del owner_agent
decretado para el bloque activo. Inyecta hint al modelo via systemMessage
(PreToolUse Edit|Write|NotebookEdit) o additionalContext (UserPromptSubmit).

Lee project_docs/session_locks.yaml del cwd. Si no es proyecto Hive (no existe
el archivo) o no hay sesion con owner_agent → silencio.

Mapping path → dominio en PATH_TO_DOMAIN. Mapping dominio → skill ID en
DOMAIN_TO_SKILL para sugerencia accionable.
"""
import json
import os
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("{}")
    sys.exit(0)


PATH_TO_DOMAIN = [
    # Bookkeeping — silencio (cualquier owner los puede tocar al cerrar)
    ("project_docs/ROADMAP.md", "_skip_"),
    ("project_docs/block_graph.yaml", "_skip_"),
    ("project_docs/session_locks.yaml", "_skip_"),
    ("project_docs/cross_decisions.md", "_skip_"),
    ("project_docs/active_plans/", "_skip_"),
    ("project_docs/questions_for_human.md", "_skip_"),
    ("project_docs/FUNDAMENTALS.md", "_skip_"),
    ("MEMORY.md", "_skip_"),
    ("docs/DEVLOG.md", "_skip_"),
    # Content Lead (i18n + copy)
    ("app/web/public/locales/", "content-lead"),
    ("project_docs/marketing/posts/", "content-lead"),
    ("project_docs/marketing/copy/", "content-lead"),
    # Frontend Lead (Eolo)
    ("app/web/src/", "frontend-lead"),
    ("app/web/scripts/", "frontend-lead"),
    ("app/web/public/", "frontend-lead"),
    ("app/web/", "frontend-lead"),
    # Backend Lead
    ("app/api/src/", "backend-lead"),
    ("app/api/prisma/", "backend-lead"),
    ("app/api/", "backend-lead"),
    # DevOps Lead
    (".github/workflows/", "devops-lead"),
    ("Dockerfile", "devops-lead"),
    ("docker-compose", "devops-lead"),
    # Marketing & Legal (Hades)
    ("project_docs/marketing/", "marketing-legal"),
    ("project_docs/legal/", "marketing-legal"),
    # Finance (Midas)
    ("project_docs/finance/", "finance-director"),
    ("project_docs/context/budget", "finance-director"),
]


DOMAIN_TO_SKILL = {
    "frontend-lead": "agents:ejecucion:frontend-lead",
    "backend-lead": "agents:ejecucion:backend-lead",
    "content-lead": "agents:ejecucion:content-lead",
    "devops-lead": "agents:ejecucion:devops-lead",
    "marketing-legal": "agents:direccion:marketing-legal",
    "finance-director": "agents:direccion:finance-director",
    "engineering-director": "agents:direccion:engineering-director",
    "product-director": "agents:direccion:product-director",
    "kadid": "agents:estrategia:kadid",
    "cto": "agents:estrategia:cto",
    "cpo": "agents:estrategia:cpo",
    "pm": "agents:direccion:pm",
    "secre": "agents:direccion:secre",
}


def normalize_path(file_path: str, cwd: str) -> str:
    fp = file_path.replace("\\", "/")
    cwd_norm = cwd.replace("\\", "/")
    if fp.startswith(cwd_norm + "/"):
        fp = fp[len(cwd_norm) + 1 :]
    return fp


def infer_domain(file_path: str, cwd: str):
    if not file_path:
        return None
    fp = normalize_path(file_path, cwd)
    best_domain = None
    best_len = 0
    for pattern, domain in PATH_TO_DOMAIN:
        if pattern in fp and len(pattern) > best_len:
            best_domain = domain
            best_len = len(pattern)
    return best_domain


def load_active_sessions(cwd: str):
    locks_path = Path(cwd) / "project_docs" / "session_locks.yaml"
    if not locks_path.exists():
        return []
    try:
        with open(locks_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        return data.get("active_sessions", []) or []
    except Exception:
        return []


def handle_pre_tool_use(payload, sessions):
    tool_name = payload.get("tool_name", "")
    if tool_name not in ("Edit", "Write", "NotebookEdit"):
        return {}
    tool_input = payload.get("tool_input", {}) or {}
    file_path = tool_input.get("file_path") or tool_input.get("notebook_path")
    if not file_path:
        return {}
    cwd = payload.get("cwd", os.getcwd())
    inferred = infer_domain(file_path, cwd)
    if inferred is None or inferred == "_skip_":
        return {}

    sessions_with_owner = [s for s in sessions if s.get("owner_agent")]

    for entry in sessions_with_owner:
        owner = entry.get("owner_agent")
        co_owners = entry.get("co_owners", []) or []
        if inferred in [owner] + co_owners:
            return {}

    if sessions_with_owner:
        owners_summary = ", ".join(
            f"{e.get('block', '?')}=<{e.get('owner_agent')}>"
            for e in sessions_with_owner
        )
        skill = DOMAIN_TO_SKILL.get(inferred, f"agents:?:{inferred}")
        msg = (
            f"[ROUTING PIVOT] file_path={file_path} infiere scope <{inferred}>. "
            f"Ninguna sesion activa lo cubre (owners: {owners_summary}). "
            f"Invoca Skill({skill}) o declara [Directo] con razon."
        )
        return {"systemMessage": msg}

    skill = DOMAIN_TO_SKILL.get(inferred, f"agents:?:{inferred}")
    msg = (
        f"[ROUTING] file_path={file_path} es scope <{inferred}>. "
        f"No hay owner_agent decretado en session_locks. "
        f"Considera Skill({skill}) o declara [Directo] con razon."
    )
    return {"systemMessage": msg}


def handle_user_prompt_submit(sessions):
    sessions_with_owner = [s for s in sessions if s.get("owner_agent")]
    if not sessions_with_owner:
        return {}
    parts = []
    for entry in sessions_with_owner:
        block = entry.get("block", "?")
        owner = entry.get("owner_agent")
        co = entry.get("co_owners", []) or []
        co_str = f" (+ {', '.join(co)})" if co else ""
        parts.append(f"{block} bajo <{owner}>{co_str}")
    ctx = (
        "[ROUTING] Bloques activos: "
        + "; ".join(parts)
        + ". Antes de actuar, verifica si la subtarea cae en su scope. "
        + "Si no, declara PIVOT con Skill correcto o [Directo] con razon."
    )
    return {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": ctx,
        }
    }


def main():
    try:
        raw = sys.stdin.read()
        payload = json.loads(raw) if raw.strip() else {}
    except Exception:
        print("{}")
        return

    cwd = payload.get("cwd", os.getcwd())
    sessions = load_active_sessions(cwd)
    hook_event = payload.get("hook_event_name", "")

    if hook_event == "PreToolUse":
        out = handle_pre_tool_use(payload, sessions)
    elif hook_event == "UserPromptSubmit":
        out = handle_user_prompt_submit(sessions)
    else:
        out = {}

    print(json.dumps(out) if out else "{}")


if __name__ == "__main__":
    main()
