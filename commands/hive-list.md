---
allowed-tools: Bash(python ~/.claude/hive-bridge/bridge.py:*)
description: Lista todas las sesiones Claude Code registradas en el Hive Bridge con su alias, último timestamp visto, número de mensajes pendientes en su inbox, y cwd. Útil para ver qué sesiones están activas antes de mandar un mensaje, o para descubrir si hay sesiones huérfanas registradas que ya no están vivas.
---

# Hive List

Lista todas las sesiones Claude Code que se han registrado alguna vez en el Hive Bridge.

## Ejecución

```bash
python ~/.claude/hive-bridge/bridge.py list
```

## Salida

Tabla con cuatro columnas:

- **ALIAS** — el nombre que la sesión exportó vía `HIVE_ALIAS` (ej. `frontend-1`).
- **PENDING** — número de mensajes pendientes en su inbox (sin leer).
- **LAST SEEN** — timestamp UTC de la última vez que esa sesión disparó un hook (SessionStart, UserPromptSubmit, PostToolUse).
- **CWD** — directorio de trabajo donde arrancó la sesión.

## Detectar sesiones zombies

Una sesión con `LAST SEEN` muy antiguo puede ser una sesión muerta cuyo registro persiste. La carpeta de esa sesión se puede borrar manualmente: `rm -rf ~/.claude/hive-bridge/sessions/<alias>/` (Unix) o `Remove-Item -Recurse ~/.claude/hive-bridge/sessions/<alias>/` (PowerShell).
