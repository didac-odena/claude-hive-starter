---
allowed-tools: Bash(python ~/.claude/hive-bridge/bridge.py:*)
argument-hint: <alias>
description: Asocia ESTA sesión Claude Code (que ya está corriendo, sin HIVE_ALIAS exportada) a un alias del Hive Bridge usando el PID del proceso Claude Code como llave única. Permite que dos sesiones en el mismo cwd se distingan correctamente. Útil para conectar al bridge sesiones vivas que arrancaste antes de que el bridge existiera, sin necesidad de cerrarlas y reabrirlas. Ejemplo "/hive-claim frontend-1".
---

# Hive Claim

Asocia tu sesión Claude Code actual a un alias del Hive Bridge **sin reiniciar la sesión**.

## Cuándo usarlo

- La sesión ya estaba arrancada cuando el Hive Bridge se instaló.
- No tenías la env var `HIVE_ALIAS` exportada al arrancar `claude`.
- Quieres conectar esta sesión al bridge ahora mismo.

## Cómo funciona

El script sube el árbol de procesos hasta encontrar el ancestro `node` (el proceso de Claude Code) y usa **su PID** como identificador único de esta sesión. Escribe el mapeo `claude_pid → alias` en `~/.claude/hive-bridge/sessions-by-pid.json`.

A partir de ese momento, todos los slash commands del bridge (`/hive-send`, `/hive-inbox`) y los hooks resuelven tu alias buscando ese PID. Cada sesión Claude Code tiene su propio PID, así que **dos sesiones en el mismo cwd se distinguen sin problema**.

Cuando la sesión Claude Code muere, su PID desaparece del sistema. El siguiente `bridge.py list` o `claim` hace garbage collection automático de la entrada huérfana.

## Argumentos

- `$1` — alias deseado (ej. `frontend-1`, `marketing-b153`).

## Ejecución

```bash
python ~/.claude/hive-bridge/bridge.py claim "$1"
```

## Si falla

Mensaje de error típico: `"no encuentro el proceso ancestro 'node'"`. Pasa si:
- `psutil` no está instalado (`pip install psutil`).
- El árbol de procesos es raro (Claude Code corriendo dentro de WSL, contenedor, o entorno no estándar).

Fallback: cierra la sesión y reabre con `export HIVE_ALIAS=<alias>` antes de `claude`.
