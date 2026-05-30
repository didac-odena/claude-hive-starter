#!/usr/bin/env python3
"""
Status line for Claude Code.
Layout: Model | Effort | Band | CTX% | W%

- Effort: read from ~/.claude/settings.json (not present in stdin payload)
- CTX%: computed from current_usage (input+output+cache) / context_window_size
  so it matches the auto-compact threshold, not just the cached-input %.
- W%: rate_limits.seven_day.used_percentage from the stdin payload
  (appears only for Claude.ai Pro/Max after the first API response)
- Raw payload dumped to ~/.claude/.statusline-payload.json on every run
  for debugging unknown schema fields.
"""
import sys
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

CEST = timezone(timedelta(hours=2))
CET = timezone(timedelta(hours=1))

HOME = Path.home()
SETTINGS_PATH = HOME / ".claude" / "settings.json"
DEBUG_PATH = HOME / ".claude" / ".statusline-payload.json"


def spain_now():
    utc = datetime.now(timezone.utc)
    year = utc.year
    march_last_sun = 31 - (datetime(year, 3, 31).weekday() + 1) % 7
    oct_last_sun = 31 - (datetime(year, 10, 31).weekday() + 1) % 7
    cest_start = datetime(year, 3, march_last_sun, 1, tzinfo=timezone.utc)
    cest_end = datetime(year, 10, oct_last_sun, 1, tzinfo=timezone.utc)
    tz = CEST if cest_start <= utc < cest_end else CET
    return utc.astimezone(tz)


def get_band(hour):
    if 6 <= hour < 13:
        return "ECO", "\033[32m"
    elif 13 <= hour < 14:
        return "OK", "\033[33m"
    elif 14 <= hour < 20:
        return "PICO", "\033[31m"
    elif 20 <= hour < 24:
        return "OK", "\033[33m"
    else:
        return "ECO", "\033[32m"


def read_effort_from_settings():
    try:
        with open(SETTINGS_PATH, encoding="utf-8") as f:
            data = json.load(f)
        return data.get("effortLevel") or data.get("effort_level") or "?"
    except Exception:
        return "?"


def compute_ctx_pct(ctx):
    """Real context window usage including output tokens — matches auto-compact."""
    if not isinstance(ctx, dict):
        return None
    cu = ctx.get("current_usage") or {}
    size = ctx.get("context_window_size") or 0
    if size:
        used = (
            (cu.get("input_tokens") or 0)
            + (cu.get("output_tokens") or 0)
            + (cu.get("cache_creation_input_tokens") or 0)
            + (cu.get("cache_read_input_tokens") or 0)
        )
        if used:
            return round(100 * used / size)
    return ctx.get("used_percentage")


def extract_week_pct(payload):
    """Try several plausible locations for the 7-day rate-limit percentage."""
    rl = payload.get("rate_limits") or payload.get("rateLimits") or {}
    if isinstance(rl, dict):
        for key in ("seven_day", "sevenDay", "weekly", "week"):
            node = rl.get(key)
            if isinstance(node, dict):
                pct = node.get("used_percentage") or node.get("usedPercentage")
                if pct is not None:
                    return pct
    usage = payload.get("usage") or {}
    if isinstance(usage, dict):
        week = usage.get("weekly") or usage.get("seven_day")
        if isinstance(week, dict):
            pct = week.get("used_percentage") or week.get("usedPercentage")
            if pct is not None:
                return pct
    return None


def week_color(pct):
    if pct is None:
        return "\033[90m"
    if pct >= 85:
        return "\033[31m"
    if pct >= 60:
        return "\033[33m"
    return "\033[32m"


def main():
    raw = sys.stdin.read()
    try:
        payload = json.loads(raw)
    except Exception:
        print("Claude Code")
        return

    try:
        DEBUG_PATH.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8"
        )
    except Exception:
        pass

    model = payload.get("model", {}) or {}
    model_name = model.get("display_name") or model.get("id") or "Claude"

    effort = read_effort_from_settings()

    ctx_pct = compute_ctx_pct(payload.get("context_window"))
    week_pct = extract_week_pct(payload)

    now = spain_now()
    label, band_color = get_band(now.hour)
    reset = "\033[0m"

    parts = [model_name, str(effort), f"{band_color}{label}{reset}"]
    if ctx_pct is not None:
        parts.append(f"CTX {ctx_pct}%")
    if week_pct is not None:
        wcolor = week_color(week_pct)
        parts.append(f"{wcolor}W {int(round(float(week_pct)))}%{reset}")
    else:
        parts.append("\033[90mW —\033[0m")

    print(" | ".join(parts))


if __name__ == "__main__":
    main()
