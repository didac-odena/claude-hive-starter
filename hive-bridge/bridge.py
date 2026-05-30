"""Hive Bridge — inter-session messaging for Claude Code via filesystem mailbox.

Each session is identified by either:
  1. The HIVE_ALIAS env var (set before claude started), OR
  2. A claim that maps the Claude Code process PID (ancestor 'node') to an alias.

Storage layout:
  ~/.claude/hive-bridge/
    sessions-by-pid.json                # { "<claude_pid>": {"alias": ..., "claimedAt": ...}, ... }
    sessions/<alias>/{manifest.json, inbox/, archive/, outbox/}

CLI subcommands:
  register <alias> [--cwd <path>]            internal: ensure session dirs exist
  claim <alias>                              associate THIS live session (by PID) to alias
  send <to-alias> <content> [...]            send a message to another session
  inbox [--alias X] [--peek]                 read your inbox; archives unless --peek
  list                                       list all known sessions
  check --mode {session-start|user-prompt|post-tool}
                                             hook entry point; emits JSON systemMessage

Atomic writes via os.replace (atomic on Windows from Python 3.3+).
"""

import argparse
import json
import os
import secrets
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Force UTF-8 on stdout/stderr (Windows defaults to cp1252)
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path.home() / ".claude" / "hive-bridge"
SESSIONS = ROOT / "sessions"
SESSIONS_MAP_FILE = ROOT / "sessions-by-pid.json"
RATE_LIMIT_SECONDS = 30  # for post-tool hook


# ---------- helpers ----------

def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def gen_id(prefix: str = "msg") -> str:
    return f"{prefix}-{secrets.token_hex(6)}"


def session_dir(alias: str) -> Path:
    return SESSIONS / alias


def write_json_atomic(path: Path, data: dict) -> None:
    tmp = path.with_suffix(path.suffix + f".tmp-{secrets.token_hex(4)}")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    os.replace(tmp, path)


def read_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def get_claude_session_pid() -> int | None:
    """Walk up the process tree to find the ancestor 'node' (Claude Code main process).

    Each Claude Code session is a separate node process; all its hooks and slash-command
    bashes share that ancestor PID. So PID-of-ancestor-node = unique session identifier.

    Returns None if psutil unavailable or no node ancestor found.
    """
    try:
        import psutil
    except Exception:
        return None
    try:
        cur = psutil.Process()
        depth = 0
        while cur and depth < 12:
            name = (cur.name() or "").lower()
            if name in ("node", "node.exe"):
                return cur.pid
            try:
                cur = cur.parent()
            except Exception:
                break
            depth += 1
    except Exception:
        return None
    return None


def is_pid_alive(pid: int) -> bool:
    try:
        import psutil
        return psutil.pid_exists(pid)
    except Exception:
        return True  # conservative: assume alive if we can't check


def read_sessions_map() -> dict:
    return read_json(SESSIONS_MAP_FILE) or {}


def write_sessions_map(m: dict) -> None:
    write_json_atomic(SESSIONS_MAP_FILE, m)


def gc_sessions_map(m: dict) -> dict:
    """Remove entries whose Claude PID is no longer alive."""
    return {pid: data for pid, data in m.items() if is_pid_alive(int(pid))}


def my_alias() -> str | None:
    """Resolve the alias for THIS process.

    Order of precedence:
      1. HIVE_ALIAS environment variable (set before claude started).
      2. sessions-by-pid.json lookup by ancestor Claude Code PID.
    """
    env = os.environ.get("HIVE_ALIAS")
    if env:
        return env
    pid = get_claude_session_pid()
    if pid is None:
        return None
    m = read_sessions_map()
    entry = m.get(str(pid))
    if entry:
        return entry.get("alias")
    return None


def ensure_session(alias: str, cwd: str | None = None) -> Path:
    d = session_dir(alias)
    (d / "inbox").mkdir(parents=True, exist_ok=True)
    (d / "archive").mkdir(parents=True, exist_ok=True)
    (d / "outbox").mkdir(parents=True, exist_ok=True)
    manifest = d / "manifest.json"
    data = {
        "alias": alias,
        "cwd": cwd or os.getcwd(),
        "startedAt": utc_now(),
        "lastSeen": utc_now(),
    }
    if manifest.exists():
        existing = read_json(manifest) or {}
        data["startedAt"] = existing.get("startedAt", data["startedAt"])
    write_json_atomic(manifest, data)
    return d


def list_inbox(alias: str) -> list[Path]:
    d = session_dir(alias) / "inbox"
    if not d.is_dir():
        return []
    return sorted(d.glob("msg-*.json"))


def archive_message(alias: str, msg_path: Path) -> None:
    archive = session_dir(alias) / "archive"
    os.replace(msg_path, archive / msg_path.name)


# ---------- subcommands ----------

def cmd_register(args) -> int:
    if not args.alias:
        print("ERROR: alias required", file=sys.stderr)
        return 2
    ensure_session(args.alias, args.cwd)
    print(args.alias)
    return 0


def cmd_claim(args) -> int:
    """Associate THIS live Claude Code session (by ancestor node PID) with an alias.
    Works even if the session was started without HIVE_ALIAS exported."""
    alias = args.alias
    pid = get_claude_session_pid()
    if pid is None:
        print(
            "ERROR: no encuentro el proceso ancestro 'node' de esta sesión Claude Code. "
            "¿psutil no instalado o entorno raro? Como fallback exporta HIVE_ALIAS y reinicia.",
            file=sys.stderr,
        )
        return 1
    m = read_sessions_map()
    m = gc_sessions_map(m)
    previous = m.get(str(pid), {}).get("alias")
    m[str(pid)] = {"alias": alias, "claimedAt": utc_now(), "cwd": os.getcwd()}
    write_sessions_map(m)
    ensure_session(alias, os.getcwd())
    if previous and previous != alias:
        print(f"OVERRIDE: la sesión Claude Code (pid {pid}) estaba asociada a '{previous}'. Ahora '{alias}'.")
    else:
        print(f"OK: sesión Claude Code (pid {pid}) asociada al alias '{alias}'.")
    print("Esta asociación persiste mientras viva el proceso de Claude Code; al cerrar la sesión, se limpia automáticamente la próxima vez que el bridge se ejecute.")
    return 0


def cmd_send(args) -> int:
    sender = my_alias()
    if not sender:
        print(
            "ERROR: esta sesión no tiene alias. Ejecuta `/hive-claim <alias>` o exporta HIVE_ALIAS antes de arrancar claude.",
            file=sys.stderr,
        )
        return 2
    target = args.to
    target_dir = session_dir(target)
    if not target_dir.is_dir():
        print(f"ERROR: target session '{target}' not found at {target_dir}", file=sys.stderr)
        return 1
    ensure_session(sender)
    msg = {
        "id": gen_id("msg"),
        "from": sender,
        "to": target,
        "timestamp": utc_now(),
        "status": "pending",
        "content": args.content,
    }
    if args.block:
        msg["block"] = args.block
    if args.domain:
        msg["domain"] = args.domain
    if args.in_reply_to:
        msg["inReplyTo"] = args.in_reply_to
    inbox_path = target_dir / "inbox" / f"{msg['id']}.json"
    write_json_atomic(inbox_path, msg)
    outbox_path = session_dir(sender) / "outbox" / f"{msg['id']}.json"
    write_json_atomic(outbox_path, {**msg, "status": "sent"})
    print(msg["id"])
    return 0


def cmd_inbox(args) -> int:
    alias = args.alias or my_alias()
    if not alias:
        print(
            "ERROR: esta sesión no tiene alias. Ejecuta `/hive-claim <alias>` o pasa --alias.",
            file=sys.stderr,
        )
        return 2
    ensure_session(alias)
    msgs = list_inbox(alias)
    if not msgs:
        print(f"Inbox of '{alias}': empty.")
        return 0
    print(f"Inbox of '{alias}': {len(msgs)} pending message(s).\n")
    for p in msgs:
        m = read_json(p)
        if not m:
            continue
        print(f"--- {m['id']} ---")
        print(f"  From:      {m.get('from', '?')}")
        print(f"  At:        {m.get('timestamp', '?')}")
        if m.get("block"):
            print(f"  Block:     {m['block']}")
        if m.get("domain"):
            print(f"  Domain:    {m['domain']}")
        if m.get("inReplyTo"):
            print(f"  In reply:  {m['inReplyTo']}")
        print(f"  Content:   {m.get('content', '')}")
        print()
        if not args.peek:
            archive_message(alias, p)
    if args.peek:
        print("(peek mode — messages NOT archived)")
    else:
        print(f"Archived {len(msgs)} message(s) to archive/.")
    return 0


def cmd_list(args) -> int:
    if not SESSIONS.is_dir():
        print("No sessions registered yet.")
        return 0
    # GC dead PIDs first
    m = read_sessions_map()
    cleaned = gc_sessions_map(m)
    if cleaned != m:
        write_sessions_map(cleaned)
    pid_by_alias = {data.get("alias"): pid for pid, data in cleaned.items()}
    rows = []
    for d in sorted(SESSIONS.iterdir()):
        if not d.is_dir():
            continue
        manifest = d / "manifest.json"
        mf = read_json(manifest) or {}
        inbox_count = len(list_inbox(d.name))
        live_pid = pid_by_alias.get(d.name, "-")
        rows.append((d.name, mf.get("cwd", "?"), mf.get("lastSeen", "?"), inbox_count, live_pid))
    if not rows:
        print("No sessions registered yet.")
        return 0
    width = max(len(r[0]) for r in rows)
    print(f"{'ALIAS'.ljust(width)}  PENDING  LAST SEEN              CLAUDE_PID  CWD")
    for alias, cwd, last, n, pid in rows:
        print(f"{alias.ljust(width)}  {str(n).rjust(7)}  {last:<22} {str(pid):<10}  {cwd}")
    return 0


def cmd_check(args) -> int:
    """Hook entry point. Output JSON to stdout for Claude Code to inject systemMessage."""
    alias = my_alias()
    if not alias:
        return 0  # opt-in; silent no-op
    ensure_session(alias)

    if args.mode == "post-tool":
        marker = session_dir(alias) / ".last-check"
        now = time.time()
        try:
            last = float(marker.read_text(encoding="utf-8").strip())
        except Exception:
            last = 0.0
        if now - last < RATE_LIMIT_SECONDS:
            return 0
        marker.write_text(str(now), encoding="utf-8")

    if args.mode in ("session-start", "user-prompt"):
        manifest = session_dir(alias) / "manifest.json"
        m = read_json(manifest) or {}
        m["lastSeen"] = utc_now()
        m.setdefault("alias", alias)
        m.setdefault("cwd", os.getcwd())
        m.setdefault("startedAt", m.get("startedAt", utc_now()))
        write_json_atomic(manifest, m)

    msgs = list_inbox(alias)
    if not msgs:
        return 0

    lines = [f"📬 Hive Bridge: {len(msgs)} mensaje(s) pendiente(s) en el buzón de '{alias}'."]
    for p in msgs:
        m = read_json(p)
        if not m:
            continue
        meta = []
        if m.get("block"):
            meta.append(f"block={m['block']}")
        if m.get("domain"):
            meta.append(f"domain={m['domain']}")
        if m.get("inReplyTo"):
            meta.append(f"reply-to={m['inReplyTo']}")
        meta_str = f" [{', '.join(meta)}]" if meta else ""
        lines.append(f"  • [{m['id']}] de {m.get('from', '?')}{meta_str}: {m.get('content', '')}")
    lines.append("")
    lines.append(
        "Para procesar: ejecuta `/hive-inbox` (los archiva tras leer) o pídeme que lo haga. "
        "Si tu tarea actual no es bloqueante, atiende esto ahora; si lo es, anótalo y sigue."
    )
    payload = {"systemMessage": "\n".join(lines)}
    print(json.dumps(payload))
    return 0


# ---------- main ----------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="bridge", description="Hive Bridge inter-session messaging")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("register", help="register or refresh this session")
    s.add_argument("alias")
    s.add_argument("--cwd", default=None)

    s = sub.add_parser("claim", help="associate THIS live Claude Code session (by ancestor PID) with an alias")
    s.add_argument("alias")

    s = sub.add_parser("send", help="send a message to another session")
    s.add_argument("to", help="target alias")
    s.add_argument("content", help="message body")
    s.add_argument("--block", default=None)
    s.add_argument("--domain", default=None)
    s.add_argument("--in-reply-to", dest="in_reply_to", default=None)

    s = sub.add_parser("inbox", help="read your inbox; archives unless --peek")
    s.add_argument("--alias", default=None)
    s.add_argument("--peek", action="store_true")

    sub.add_parser("list", help="list registered sessions")

    s = sub.add_parser("check", help="hook entry point (internal)")
    s.add_argument("--mode", choices=["session-start", "user-prompt", "post-tool"], required=True)

    return p


def main() -> int:
    SESSIONS.mkdir(parents=True, exist_ok=True)
    args = build_parser().parse_args()
    handlers = {
        "register": cmd_register,
        "claim": cmd_claim,
        "send": cmd_send,
        "inbox": cmd_inbox,
        "list": cmd_list,
        "check": cmd_check,
    }
    return handlers[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
