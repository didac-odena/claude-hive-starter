# Claude-Hive Starter

Sistema de agentes multi-nivel para **Claude Code**. Organiza tu proyecto como un equipo con jerarquia — Estrategia, Direccion y Ejecucion — coordinado por un orquestador (Kadid) y un workflow de bloques con pre-flight, locks y post-validation.

Esta es la version **agnostica** del sistema: sin referencias a ningun proyecto concreto, lista para instanciar en el tuyo.

> 👋 ¿Primera vez? Empieza por **[WELCOME.md](WELCOME.md)** — qué es, qué beneficios tiene y cómo usarlo bien.

## Que incluye

```
~/.claude/                          ← este repo se clona aqui
├── CLAUDE.md                       # Reglas globales (idioma, code language, YAGNI, naming, metodologia Hive)
├── settings.json.example           # Plantilla de config (hooks + permisos), SIN secretos
├── status.py                       # Status line (modelo, contexto %, banda horaria)
├── commands/                       # Skills + agentes
│   ├── commit-devlog.md, conventions.md, design-review.md, fix-bug.md,
│   ├── generate-tests.md, optimize-repo.md, perf-check.md, security-scan.md,
│   ├── skill-creator.md, skill-installer.md, init-project-workflow.md
│   ├── hive-claim.md, hive-inbox.md, hive-list.md, hive-send.md   # Hive Bridge (mensajeria entre sesiones)
│   └── agents/                     # Los 13 agentes en 3 niveles
│       ├── estrategia/             # Kadid, CTO (Hefesto), CPO (Hermes)
│       ├── direccion/              # PM (Cronos), Engineering Director (Apolo), Product Director (Zeus),
│       │                           #   Marketing & Legal (Hades), Finance Director (Midas), Secre
│       └── ejecucion/              # Backend Lead, Frontend Lead (Eolo), DevOps Lead, Content Lead (Afrodita)
├── hooks/                          # Hooks de Claude Code
│   ├── rtk-rewrite.sh              # Compresion de tokens (RTK)
│   ├── routing-check.py            # Detecta si una edicion diverge del owner del bloque activo
│   └── hive-remind.py             # Avisa de cambios sin commit
├── hive-bridge/                    # Mensajeria entre sesiones Claude paralelas (bridge.py)
└── hive/                          # Docs de la metodologia + templates
    ├── SETUP.md, CHANGELOG.md, kadid-profile.md, training-protocol.md
    ├── docs/                       # ARCHITECTURE.md, AGENTS.md, TOKEN-EFFICIENCY.md
    ├── orchestrator/               # Orquestador de planes multi-agente
    └── templates/                  # FUNDAMENTALS, MEMORY, WORKFLOW, etc. para instanciar por proyecto
```

### 13 agentes en 3 niveles
- **Estrategia (3):** Kadid (fundador/guardian/orquestador), CTO (Hefesto), CPO (Hermes)
- **Direccion (6):** PM (Cronos), Engineering Director (Apolo), Product Director (Zeus), Marketing & Legal (Hades), Finance Director (Midas), Secre
- **Ejecucion (4):** Backend Lead, Frontend Lead (Eolo), DevOps Lead, Content Lead (Afrodita)

### Skills reutilizables
`commit-devlog`, `conventions`, `design-review`, `fix-bug`, `generate-tests`, `optimize-repo`, `perf-check`, `security-scan`, `skill-creator`, `skill-installer`, `init-project-workflow`, y los comandos del Hive Bridge (`hive-*`).

### Metodologia Hive
- Kadid siempre activo — no hay que invocarlo.
- `FUNDAMENTALS.md` por proyecto — documentos inviolables.
- Flujo de bloque: pre-flight (locks + dependencias) → planificacion → ejecucion → post-validation → cierre con DEVLOG.
- `cross_decisions.md` para decisiones multi-dominio; `block_graph.yaml` para dependencias; `session_locks.yaml` para sesiones paralelas.

## Instalacion

### Opcion 0 — deja que Claude lo instale (recomendado)
Clona el repo, abre Claude Code dentro y dile: **"Lee INSTALL.md e instala el sistema en mi ~/.claude"**. Claude fusiona el contenido en tu `~/.claude` sin pisar tu config (hace backup de `CLAUDE.md`/`settings.json`, resuelve rutas y engancha los hooks). Ver [INSTALL.md](INSTALL.md). Reinicia Claude Code al terminar.

```bash
git clone https://github.com/<tu-usuario>/claude-hive-starter.git
cd claude-hive-starter && claude   # luego, dentro: "Lee INSTALL.md e instalalo"
```

### Opcion A — clonar como tu `~/.claude/` (manual)
Si quieres adoptar todo el sistema (recomendado para empezar):

```bash
# Haz backup de tu ~/.claude actual si tienes uno
git clone https://github.com/<tu-usuario>/claude-hive-starter.git ~/.claude
cd ~/.claude
cp settings.json.example settings.json
# Edita settings.json: sustituye <CLAUDE_HOME> por la ruta absoluta de tu ~/.claude
```

`<CLAUDE_HOME>` es la ruta a tu carpeta `.claude` (ej. `C:/Users/TU_USUARIO/.claude` en Windows, `/home/tu-usuario/.claude` en Linux/Mac). Los hooks (`rtk-rewrite.sh`, `routing-check.py`, `hive-remind.py`) y la status line (`status.py`) se resuelven desde ahi.

### Opcion B — instanciar solo el workflow en un proyecto existente
Si ya tienes tu `~/.claude/` y solo quieres el workflow Hive en un repo:

```
/init-project-workflow
```

Crea `.claude/rules/workflow.md` (desde el template agnostico) y los archivos canonicos del Hive (`FUNDAMENTALS.md`, `MEMORY.md`, `ROADMAP.md`, `block_graph.yaml`, `session_locks.yaml`, `cross_decisions.md`, `active_plans/`, `DEVLOG.md`) si no existen.

## Hooks (opcional pero recomendado)
- **RTK** (`rtk-rewrite.sh`) — comprime tokens en operaciones Bash.
- **routing-check** (`routing-check.py`) — si tienes un bloque activo con `owner_agent` en `session_locks.yaml`, avisa cuando una edicion cae fuera de su dominio. Si no es un proyecto Hive (no existe `session_locks.yaml`), se queda en silencio.
- **hive-remind** (`hive-remind.py`) — recordatorio de cambios sin commitear al parar.

El mapa de rutas→dominio de `routing-check.py` (`PATH_TO_DOMAIN`) trae defaults para un stack web tipico (`app/web/`, `app/api/`); adaptalo a la estructura de tu proyecto.

## Notas
- Las reglas de `CLAUDE.md` (incluido el idioma) son un punto de partida — ajustalas a tu preferencia.
- Los registros de aprendizaje de `hive/kadid-profile.md` empiezan vacios y se llenan con el uso.
- Algunas skills referencian plugins externos (Figma MCP, `ui-ux-pro-max`, HyperFrames, suite Impeccable/Taste) que se instalan aparte; sin ellos, los agentes funcionan igual.
