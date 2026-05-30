---
allowed-tools: Bash(python ~/.claude/hive-bridge/bridge.py:*)
argument-hint: <alias-destino> "<mensaje>" [--block X] [--domain Y]
description: Envía un mensaje desde esta sesión Claude Code a otra sesión registrada con HIVE_ALIAS. Útil cuando trabajas en sesiones paralelas y quieres pasar contexto entre ellas sin copiar/pegar manual. Ej. "/hive-send backend-1 'el endpoint de pagos ya está listo'".
---

# Hive Send

Envía un mensaje desde tu sesión actual al buzón de otra sesión Claude Code identificada por su alias.

## Requisitos

- Esta sesión tiene que tener `HIVE_ALIAS` exportado (ej. `export HIVE_ALIAS=frontend-1` antes de arrancar `claude`).
- La sesión destino tiene que estar registrada (basta con que haya arrancado al menos una vez con su alias).

## Argumentos

- `$1` — alias de la sesión destino (ej. `backend-1`).
- `$2` — contenido del mensaje (entre comillas si tiene espacios).
- `--block <id>` — opcional, etiqueta el mensaje con un bloque (ej. `B175`).
- `--domain <dominio>` — opcional, etiqueta el mensaje con un dominio (ej. `backend`).

## Ejecución

```bash
python ~/.claude/hive-bridge/bridge.py send "$ARGUMENTS"
```

Tras ejecutar, devuelve el ID del mensaje (formato `msg-<hex>`). Quedará pendiente en el inbox del destino hasta que esa sesión lo lea.

## Cuándo usarlo

- Una sesión descubre algo útil para otra sesión paralela.
- Quieres pasar resultado de un sub-paso sin parar a copiar/pegar.
- Estás coordinando dos agentes Hive trabajando en bloques relacionados.

## Cuándo NO usarlo

- Si solo hay una sesión activa.
- Para guardar notas internas de la sesión actual (eso va al plan_file o a memoria).
- Para mensajes muy largos o transferir archivos (usa rutas a disco en su lugar).
