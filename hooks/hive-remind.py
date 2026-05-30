"""
Stop hook — Reminds user if ~/.claude/ has uncommitted changes.
Prints a visible warning to stderr so it shows in the terminal.
"""
import subprocess
import sys
import os

CLAUDE_DIR = os.path.expanduser("~/.claude")

try:
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=CLAUDE_DIR,
        capture_output=True,
        text=True,
        timeout=5
    )
    if result.returncode == 0 and result.stdout.strip():
        count = len(result.stdout.strip().splitlines())
        print(
            f"\n{'='*50}\n"
            f"  HIVE: {count} cambio(s) sin commit en ~/.claude/\n"
            f"  cd ~/.claude && git add -A && git commit && git push\n"
            f"{'='*50}",
            file=sys.stderr
        )
except Exception:
    pass
