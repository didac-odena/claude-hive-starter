#!/usr/bin/env bash
# RTK hook: rewrites bash commands through rtk for token compression.
# Falls back gracefully if rtk is not installed.

export PATH="$PATH:/c/Users/FullStack/.cargo/bin"
PYTHON="${PYTHON:-$(which python3 2>/dev/null || which python 2>/dev/null)}"

# Read payload from stdin before anything else consumes it
payload="$(cat)"

if ! command -v rtk &>/dev/null; then
  echo "{}"
  exit 0
fi

# Pass payload via env var to Python
RTK_PAYLOAD="$payload" "$PYTHON" -c "
import sys, json, re, os

try:
    data = json.loads(os.environ['RTK_PAYLOAD'])
    cmd = data.get('tool_input', {}).get('command', '')
except Exception:
    print('{}')
    sys.exit(0)

INTERCEPT = re.compile(
    r'^(git (diff|log|status|show|blame)|pytest|python -m pytest|npm test|pnpm test|cargo test|ls |tree |find )'
)
if INTERCEPT.match(cmd):
    print(json.dumps({
        'hookSpecificOutput': {
            'hookEventName': 'PreToolUse',
            'permissionDecision': 'allow',
            'updatedInput': {'command': 'rtk ' + cmd}
        }
    }))
else:
    print('{}')
"
