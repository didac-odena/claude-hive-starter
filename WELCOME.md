# Claude-Hive

Una capa de orquestación multi-agente sobre Claude Code, construida entera con primitivas que ya tienes: **markdown versionado, ficheros planos en git y los hooks nativos del CLI**. Cero servidor, cero daemon, cero framework. Si te quitan el sistema, lo que queda son ficheros legibles y un repo con historial.

La tesis: un modelo genérico con todo el contexto encima rinde peor que varios roles acotados, cada uno leyendo solo su dominio, coordinados por un estado explícito y auditable. Esto implementa eso sin pedirte que adoptes infraestructura.

---

## Cómo está construido

**Agentes = system prompts versionados, no procesos.** Cada uno de los 13 agentes es un `.md` bajo `commands/agents/<nivel>/`. Invocarlo (`/backend-lead`, `/kadid`, …) carga ese prompt y reorienta al modelo a ese rol: qué ficheros de contexto lee, qué decide vs qué escala, sus guardrails. Al ser markdown, son diffeables, revisables en PR y editables sin tocar código. El "CV" del agente vive en el repo del sistema; el conocimiento del proyecto vive en los context files del proyecto. Esa separación es lo que los hace portables.

**Aislamiento de contexto por convención.** Un agente lee `project_docs/context/<su-dominio>.md` y poco más, no el árbol entero. Menos ruido en la ventana, menos coste, respuestas más enfocadas. Es disciplina de contexto, no magia.

**Coordinación = ficheros planos en git.** No hay base de datos de estado. El estado de orquestación son cuatro ficheros versionados:

| Fichero | Rol |
|---|---|
| `session_locks.yaml` | Sesiones activas: `owned_files`, `owned_domains`, `owner_agent`. Lo que habilita concurrencia. |
| `block_graph.yaml` | DAG de bloques (`depends_on`, `touches`). |
| `cross_decisions.md` | Decisiones multi-dominio con racional. Estados PENDING → IMPLEMENTED. |
| `FUNDAMENTALS.md` | Invariantes inviolables. El guardián bloquea lo que las contradiga. |

Todo es texto, todo entra en el diff, todo es auditable a posteriori. No hay estado oculto que se desincronice del repo.

**Jerarquía y escalado.** Tres niveles — Estrategia (Kadid, CTO, CPO), Dirección (PM, Eng Dir, Product Dir, Marketing&Legal, Finance, Secre), Ejecución (Backend, Frontend, DevOps, Content). Escalas hacia arriba cuando excedes tu autoridad o la decisión cruza dominios; Kadid resuelve o sube al owner si es irreversible o cuesta dinero.

---

## Lo interesante: concurrencia

El sistema asume que abrirás **varias sesiones de Claude Code en paralelo** sobre el mismo repo. Dos mecanismos lo soportan:

**1. Locks por fichero (pre-flight).** Antes de abrir un bloque, se calcula qué ficheros va a tocar (`block_graph.touches`) y se contrasta con los `owned_files` de las sesiones vivas en `session_locks.yaml`. Si hay intersección → colisión, no arrancas. Dos sesiones pueden trabajar a la vez mientras no pisen los mismos ficheros. Al cerrar, se libera el lock (se borra la entry, no se comenta — el fichero solo refleja lo vivo).

**2. Routing por ownership (hook).** `routing-check.py` corre en cada `Edit|Write|NotebookEdit` y en cada prompt. Infiere el dominio del path tocado (longest-prefix match contra `PATH_TO_DOMAIN`) y lo compara con el `owner_agent` del bloque activo. Si editas algo fuera del dominio de tu bloque, inyecta un `systemMessage` sugiriendo el pivot al agente correcto o declarar `[Directo]` con razón. Routing semántico decidido una vez (al abrir bloque), validado barato en cada edición.

**3. Hive Bridge (mensajería inter-sesión).** Mailbox en filesystem, sin red. Cada sesión se identifica por `HIVE_ALIAS` (env) o por el PID del proceso `node` ancestro — cada sesión de Claude Code es un `node` distinto, así que dos sesiones en el mismo cwd se distinguen sin colisión. Enviar = escribir un JSON atómico (`os.replace`) en el `inbox/` del destino. Un hook `check` inyecta aviso cuando hay pendientes, con rate-limit de 30s en `PostToolUse` para sesiones autónomas. Opt-in: sin alias, no-op total.

---

## Los hooks (puntos de intercepción)

Todo el "automatismo" se apoya en los hooks nativos de Claude Code, no en un wrapper:

- **`rtk-rewrite.sh`** — `PreToolUse` sobre Bash. Reescribe comandos de salida pesada (`git diff/log/status`, `pytest`, `ls`, `find`…) para pasarlos por `rtk` y comprimir el output antes de que entre a la ventana. Si `rtk` no está en el PATH, deja pasar el comando intacto.
- **`routing-check.py`** — el routing por ownership de arriba. Si no es un repo Hive (no hay `session_locks.yaml`), silencio.
- **`hive-remind.py`** — `Stop` hook, recuerda cambios sin commitear al terminar.

Todos degradan con gracia: si falta una dependencia (`rtk`, `pyyaml`, `psutil`), el hook se silencia, no rompe la sesión.

---

## El loop de trabajo

El trabajo serio va en **bloques**. No es burocracia: son los controles de calidad que evitan el "casi terminado".

```
"Bloque N — <nombre>"
   │
   ├─ pre-flight ── lock check (colisión de ficheros) ──┐
   │               dependency check (block_graph)        ├─ BLOCKED → no arrancas
   │               cross_decisions activas               ┘
   │
   ├─ plan persistido en active_plans/<session_id>.md   (crash-recovery: si la
   │                                                      sesión muere, la siguiente
   │                                                      lo retoma desde disco)
   ├─ ejecución (ediciones secuenciales; agentes en
   │             paralelo solo para análisis)
   │
   └─ cierre ── test-delta (baseline vs final → caza regresiones)
               sin findings PARTIAL (FIXED | DEFERRED+bloque | ACCEPTED)
               DEVLOG + commit acotado a owned_files
               release lock
```

Reglas duras que el sistema respeta de serie: **nunca** tocar un test para que pase (se arregla el código que valida), **nunca** hardcodear para aprobar una validación, un CRITICAL con fix interino exige bloque de resolución en la misma sesión. Si una regla te estorba en algo trivial, sáltatela — están pensadas para lo que cuesta volver, no para fricción gratuita.

---

## Cómo sacarle partido

- **Define FUNDAMENTALS primero.** `/init-project-workflow` instancia `project_docs/` en tu repo. Rellena `FUNDAMENTALS.md` con lo que es sagrado (contrato de API, modelo de datos, invariantes de negocio). Sin eso, el guardián no tiene contra qué validar.
- **Piensa en bloques, no en prompts sueltos**, para cualquier cosa con dependencias o que toque varios ficheros. Para un fix de dos líneas, invocación directa y listo.
- **Invoca el dominio:** `/backend-lead` (API/schema), `/frontend-lead` (UI/design system), `/cpo`·`/finance-director` (producto/pricing), `/secre` (briefing de estado). Kadid para lo cross-domain y lo que toca FUNDAMENTALS.
- **Adapta `routing-check.py`.** El `PATH_TO_DOMAIN` trae defaults de un stack web (`app/web/`, `app/api/`). Reescríbelo a la estructura real de tu repo — es donde el routing por ownership empieza a pagar.
- **Multi-terminal:** `export HIVE_ALIAS=backend-1` antes de `claude` en cada sesión, y `/hive-send`·`/hive-inbox`·`/hive-list` para coordinarlas.

---

## Trade-offs (lo que NO es)

- **Es disciplina por convención reforzada con hints, no enforcement duro.** Los agentes son system prompts; el modelo puede desviarse. Los hooks inyectan sugerencias, no abortan (salvo lo que pase por el sistema de permisos). El valor está en hacer el estado explícito y barato de verificar, no en garantías formales.
- **El Bridge es local y sin cifrar.** Misma máquina, filesystem compartido, entorno de confianza. Sin retransmisión: si el destino no existe, el send falla con error claro.
- **El estado vive en git, con lo bueno y lo malo.** Auditable y diffeable, pero si trabajas en paralelo tienes que ser disciplinado con los `owned_files` para que los locks signifiquen algo.

---

## Quickstart

```bash
# tras instalar (ver INSTALL.md) y reiniciar Claude Code, en tu repo:
/init-project-workflow          # instancia project_docs/ (FUNDAMENTALS, MEMORY, block_graph, …)
$EDITOR project_docs/FUNDAMENTALS.md   # define tus invariantes
# luego, en Claude:
"secre"                         # briefing de estado + propuesta de agenda
"Bloque 1 — <lo que sea>"       # abre el primer bloque (pre-flight automático)
```

## Mapa del repo

- `commands/agents/` — los 13 system prompts, por nivel.
- `commands/` — skills (`commit-devlog`, `fix-bug`, `generate-tests`, `security-scan`, `perf-check`, `init-project-workflow`, …).
- `hooks/` — `rtk-rewrite.sh`, `routing-check.py`, `hive-remind.py`.
- `hive-bridge/` — `bridge.py` + protocolo del mailbox.
- `hive/` — metodología (`docs/ARCHITECTURE.md`, `docs/AGENTS.md`) y `templates/` que `init-project-workflow` instancia.
- `CLAUDE.md` — reglas globales que se cargan en cada sesión.

El detalle de la metodología y el reparto de autoridad está en `hive/docs/`.
