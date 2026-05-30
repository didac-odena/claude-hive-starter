# INSTALL — Claude-Hive Starter

Documento de instalacion pensado para que **Claude Code lo lea y lo ejecute**.

## Uso (lo que hace la persona)

```bash
git clone https://github.com/<usuario>/claude-hive-starter.git
cd claude-hive-starter
claude
```

Y dentro de Claude Code, decir:

> **"Lee INSTALL.md e instala el sistema en mi ~/.claude"**

Claude ejecutara los pasos de abajo. Al terminar, **reinicia Claude Code** para que cargue `CLAUDE.md`, los hooks y la status line.

---

## Instrucciones para Claude (ejecutor)

Objetivo: fusionar el contenido portable de este repo dentro del `~/.claude/` del usuario **sin destruir su configuracion existente**. Es un MERGE, no un wipe.

### Reglas de seguridad (NO negociables)
- **NUNCA** borres ni sobrescribas: `.credentials.json`, el `settings.json` real, `projects/`, `sessions/`, `history.jsonl`, `todos/`, `shell-snapshots/`. Son datos del usuario.
- Haz **backup** antes de tocar cualquier fichero que ya exista.
- Si un paso es ambiguo o potencialmente destructivo, **PARA y pregunta** al usuario.

### Paso 0 — Detectar entorno
- Resuelve la ruta de `~/.claude`: `$HOME/.claude` (Mac/Linux) o `$env:USERPROFILE\.claude` (Windows). Llamala `CLAUDE_HOME`.
- Si no existe, el usuario probablemente no tiene Claude Code instalado del todo — avisale antes de seguir.

### Paso 1 — Backup
- Si existe `CLAUDE_HOME/CLAUDE.md` → copialo a `CLAUDE_HOME/CLAUDE.md.bak`.
- Si existe `CLAUDE_HOME/settings.json` → copialo a `CLAUDE_HOME/settings.json.bak`.

### Paso 2 — Copiar contenido portable (merge)
Copia desde el repo a `CLAUDE_HOME`, fusionando carpetas (no borres lo que el usuario ya tenga dentro):
- `commands/`    → `CLAUDE_HOME/commands/`
- `hive/`        → `CLAUDE_HOME/hive/`
- `hive-bridge/` → `CLAUDE_HOME/hive-bridge/` (mensajeria entre sesiones; las carpetas `sessions/` runtime se crean solas)
- `hooks/`       → `CLAUDE_HOME/hooks/`
- `status.py`    → `CLAUDE_HOME/status.py`

### Paso 3 — CLAUDE.md
- Si el usuario **NO** tenia `CLAUDE.md` → copia el del repo a `CLAUDE_HOME/CLAUDE.md`.
- Si **YA** tenia uno (ya respaldado en Paso 1) → **no lo pises a ciegas**. Preguntale si quiere: (a) reemplazarlo por el del starter, (b) conservar el suyo, o (c) que le ayudes a fusionar ambos.

### Paso 4 — settings.json (engancha hooks + status line)
- Si el usuario **NO** tenia `settings.json` → copia `settings.json.example` a `CLAUDE_HOME/settings.json` y **sustituye TODOS los `<CLAUDE_HOME>`** por la ruta absoluta real.
- Si **YA** tenia uno → **no lo pises**. Muestrale los bloques `hooks` y `statusLine` del `settings.json.example` (con `<CLAUDE_HOME>` ya resuelto) y ofrece fusionarlos en su `settings.json` (añadir los hooks `rtk-rewrite` / `routing-check` / `hive-remind` y la `statusLine` si aun no los tiene).

### Paso 5 — Dependencias opcionales
Los hooks **degradan con gracia** si falta su dependencia (no rompen Claude). Para activarlos del todo:
- **RTK** (compresion de tokens, `rtk-rewrite.sh`): requiere el binario `rtk` en el PATH. Si no esta, el hook deja pasar el comando sin comprimir.
- **routing-check.py**: requiere `pyyaml` (`pip install pyyaml`). Si falta, el hook se silencia.
- **Hive Bridge** (`/hive-claim`): requiere `psutil` (`pip install psutil`). El resto de comandos del bridge funcionan solo con `HIVE_ALIAS` exportado.
Comprueba cuales tiene el usuario e informale de lo que falta (es opcional).

### Paso 6 — Verificar y reportar
- `CLAUDE_HOME/commands/agents/` contiene `estrategia/`, `direccion/`, `ejecucion/` (13 agentes en total).
- `CLAUDE_HOME/hooks/` contiene `rtk-rewrite.sh`, `routing-check.py`, `hive-remind.py`.
- `CLAUDE_HOME/settings.json` no tiene ningun `<CLAUDE_HOME>` sin resolver.
- Resumen al usuario: que se instalo, que backups se crearon (`.bak`), que dependencias opcionales faltan, y recordatorio de **reiniciar Claude Code**.

---

## Nota — comandos del Hive Bridge

Los comandos `/hive-claim`, `/hive-inbox`, `/hive-list`, `/hive-send` permiten mensajeria entre sesiones Claude Code paralelas. Para usarlos, exporta `HIVE_ALIAS=<nombre>` antes de arrancar `claude` en cada terminal. Es opt-in: sin alias no hacen nada, asi que no molestan si no los usas. Detalle en `hive-bridge/README.md`.

## Desinstalar / revertir
Restaura los `.bak` creados en el Paso 1 sobre `CLAUDE.md` y `settings.json`, y borra del `~/.claude` las carpetas/archivos que añadio el starter si no los quieres.
