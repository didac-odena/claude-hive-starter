---
allowed-tools: Bash(python ~/.claude/hive-bridge/bridge.py:*)
argument-hint: [--peek]
description: Lee el buzón de esta sesión Claude Code y muestra los mensajes pendientes. Por defecto archiva los mensajes tras leer (van a archive/ — no se pierden). Con --peek los deja pendientes para revisión posterior.
---

# Hive Inbox

Lee los mensajes pendientes en el buzón de la sesión actual (identificada por `HIVE_ALIAS`).

## Comportamiento por defecto

- Lista todos los mensajes pendientes con metadatos (from, timestamp, block, domain).
- **Archiva** los mensajes tras leerlos (los mueve de `inbox/` a `archive/`).
- Esto es lo que quieres en el 95% de casos: lees y procesas.

## Modo peek

Con `--peek` lista los mensajes **sin archivarlos**. Útil si:

- Quieres revisar qué hay sin procesar todavía.
- Quieres dejarlos pendientes para que el hook `SessionStart` los muestre la próxima vez.

## Ejecución

```bash
python ~/.claude/hive-bridge/bridge.py inbox $ARGUMENTS
```

## Tras leer

Si los mensajes contienen una **petición de respuesta**, considera mandar respuesta de vuelta con `/hive-send <from-alias> "<respuesta>" --in-reply-to <msg-id>`. El campo `inReplyTo` ayuda a la sesión emisora a correlacionar.
