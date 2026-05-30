# Hive Bridge

Buzón filesystem entre sesiones Claude Code activas en la misma máquina. Sin servidor, sin red, sin dependencias externas (solo Python 3 estándar; `psutil` opcional para `/hive-claim`).

## Cómo funciona

Cada sesión Claude Code que arranca con la variable de entorno `HIVE_ALIAS` queda registrada y crea su buzón en `~/.claude/hive-bridge/sessions/<alias>/`. Mandar mensaje = escribir un JSON en el `inbox/` del destinatario. Recibir = leer tu propio `inbox/`. El sistema operativo hace de cartero.

## Setup por sesión

Antes de arrancar `claude` en una terminal, exporta el alias:

```bash
# Linux / macOS / Git Bash
export HIVE_ALIAS=backend-1
claude

# PowerShell
$env:HIVE_ALIAS = "backend-1"
claude
```

Si NO exportas `HIVE_ALIAS`, el bridge es no-op para esa sesión: los hooks no hacen nada y los slash commands fallan con error claro. Es **opt-in**.

## Slash commands disponibles

- **`/hive-send <alias-destino> "<mensaje>" [--block X] [--domain Y]`** — manda mensaje a otra sesión.
- **`/hive-inbox [--peek]`** — lee tu inbox; archiva tras leer (con `--peek` no archiva).
- **`/hive-list`** — lista todas las sesiones registradas con sus pendientes.
- **`/hive-claim <alias>`** — asocia una sesión ya arrancada (sin `HIVE_ALIAS`) a un alias usando su PID. Requiere `psutil`.

## Recepción automática (hooks)

Si añades los hooks del bridge a tu `~/.claude/settings.json` (vienen en `settings.json.example`):

| Hook | Cuándo dispara | Caso cubierto |
|---|---|---|
| `SessionStart` | Al arrancar la sesión | Mensajes acumulados desde la última vez |
| `UserPromptSubmit` | Antes de cada prompt del usuario | Trabajo interactivo normal |
| `PostToolUse` (rate-limit 30s) | Tras cada tool call si han pasado >30s | Sesión autónoma sin usuario delante |

Cuando hay mensajes pendientes, el hook emite un `systemMessage` que se inyecta al contexto del agente, empezando con **"📬 Hive Bridge: …"**.

## Identificación de sesión

1. **`HIVE_ALIAS` env var** si fue exportada antes de `claude`. Tiene precedencia.
2. **PID del proceso `node` ancestro** (el proceso Claude Code en sí), guardado en `sessions-by-pid.json` tras un `/hive-claim`. Cada sesión es un proceso `node` distinto, así que dos sesiones en el mismo cwd se distinguen sin problema.

Cuando una sesión muere, su PID desaparece del SO; el bridge hace GC automático en el siguiente `list` o `claim`. Dependencia: `psutil` (`pip install psutil`) — solo para `/hive-claim`.

## Storage layout

```
~/.claude/hive-bridge/
├── README.md                          # este archivo
├── bridge.py                          # script Python multiplataforma
├── sessions-by-pid.json               # runtime (no se commitea)
└── sessions/                          # runtime (no se commitea)
    └── <alias>/
        ├── manifest.json              # alias, cwd, startedAt, lastSeen
        ├── inbox/                     # mensajes pendientes (msg-*.json)
        ├── archive/                   # mensajes ya leídos
        ├── outbox/                    # copias auditoría de lo enviado
        └── .last-check                # marker rate-limit PostToolUse
```

## Anatomía de un mensaje

```json
{
  "id": "msg-<12 hex>",
  "from": "<sender-alias>",
  "to": "<target-alias>",
  "timestamp": "2026-01-01T20:00:00Z",
  "status": "pending",
  "content": "texto libre",
  "block": "B12",             // opcional
  "domain": "backend",        // opcional
  "inReplyTo": "msg-..."      // opcional
}
```

## Skill `hive-bridge-awareness`

Si la tienes instalada, `hive-bridge-awareness` enseña al agente cómo reaccionar al recibir un mensaje, cuándo enviar proactivamente, y cómo no romper su flujo al llegar una notificación.

## Limitaciones conocidas

- Solo misma máquina (filesystem local). Sin cifrado: asume entorno de confianza.
- Sin retransmisión si el destinatario no existe — el send falla con error claro.
- No transferir archivos grandes — pasar la ruta absoluta y que la otra sesión la lea.
- GC solo de PIDs muertos; una carpeta de sesión zombie se borra a mano (`rm -rf ~/.claude/hive-bridge/sessions/<alias>/`).
