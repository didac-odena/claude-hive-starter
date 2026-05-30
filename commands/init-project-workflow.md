---
description: Instancia el workflow Hive completo en el proyecto actual. Copia el template agnostico WORKFLOW-template.md a .claude/rules/workflow.md rellenando placeholders, y crea los archivos canonicos de Hive (session_locks, ROADMAP, block_graph, cross_decisions, FUNDAMENTALS, active_plans/, MEMORY, DEVLOG) si no existen. Usar al inicializar un proyecto nuevo que va a usar el sistema Hive, o cuando el usuario diga "instala workflow hive", "init hive", "setup hive workflow".
---

# Init Project Workflow (Hive)

Instala el workflow Hive completo en el proyecto actual a partir del template agnostico `~/.claude/hive/templates/WORKFLOW-template.md` v2.0.

## Precondiciones

- Ejecutar desde la raiz de un proyecto (detectar con `.git/` o pedir confirmacion).
- NO ejecutar en `~/.claude` ni en directorios home.

## Workflow

1. **Verificar destino**: comprobar si ya existe `.claude/rules/workflow.md` en el proyecto.
   - Si existe Y tiene el marker `<!-- hive-workflow-template: v` → ya esta instanciado. Leer la version del marker. Si es anterior a v2.0 → ofrecer upgrade (reemplazo total con backup en `.claude/rules/workflow.md.bak`). Si es igual o posterior → informar al usuario y salir.
   - Si existe pero SIN marker → warning: es un workflow manual. Preguntar al usuario si sobrescribir (con backup) o abortar.
   - Si no existe → proceder.

2. **Leer el template**: `~/.claude/hive/templates/WORKFLOW-template.md`.

3. **Recopilar placeholders** preguntando al usuario (uno por uno, no batch):
   - `{TEST_COMMAND}`: comando de tests del proyecto. Sugerencias segun ficheros detectados:
     - Si existe `package.json` con script `test` → sugerir `npm test`
     - Si existe `pyproject.toml` o `pytest.ini` o `tests/conftest.py` → sugerir `python -m pytest tests/ --tb=short -q`
     - Si existe `go.mod` → sugerir `go test ./...`
     - Si existe `Cargo.toml` → sugerir `cargo test`
     - Si no se detecta nada → preguntar abiertamente.
   - `{DOMAIN_MAP}`: dominios del proyecto. Preguntar: "¿Que dominios tendra el proyecto? (separados por coma, p.ej. product, backend, frontend, infra, legal, marketing)". Para cada dominio que responda, generar una linea del formato `- <Dominio> (bloques ...) → \`context/<dominio>.md\``. Dejar el rango de bloques vacio (el usuario lo rellena a medida que crea bloques).

4. **Instanciar workflow**: sustituir placeholders en el template y escribir el resultado en `.claude/rules/workflow.md` del proyecto. Mantener el marker `<!-- hive-workflow-template: v2.0 -->` como primera linea para futuras actualizaciones.

5. **Crear archivos canonicos Hive** (solo los que NO existan ya — nunca sobrescribir):

   Para cada archivo, si no existe, crear desde el template correspondiente o con el stub minimo indicado:

   | Archivo destino | Fuente / stub |
   |---|---|
   | `project_docs/FUNDAMENTALS.md` | `~/.claude/hive/templates/FUNDAMENTALS-template.md` |
   | `project_docs/cross_decisions.md` | `~/.claude/hive/templates/cross-decisions-template.md` |
   | `project_docs/session_locks.yaml` | Stub ver mas abajo |
   | `project_docs/block_graph.yaml` | Stub ver mas abajo |
   | `project_docs/ROADMAP.md` | Stub ver mas abajo |
   | `project_docs/active_plans/README.md` | Stub ver mas abajo |
   | `project_docs/questions_for_human.md` | Stub ver mas abajo |
   | `docs/DEVLOG.md` | Stub ver mas abajo |
   | `MEMORY.md` | `~/.claude/hive/templates/MEMORY-template.md` |

   Para cada dominio declarado en `{DOMAIN_MAP}` crear tambien `project_docs/context/<dominio>.md` desde `~/.claude/hive/templates/context-domain-template.md` si no existe.

6. **Informe final al usuario**: listar en columnas (a) archivos creados desde cero, (b) archivos ya existentes (no tocados), (c) placeholders que han quedado vacios y que el usuario debe rellenar luego (p.ej. rangos de bloques del mapa de dominios, FUNDAMENTALS real, ROADMAP real). Incluir los pasos siguientes recomendados:
   - Editar `project_docs/FUNDAMENTALS.md` para listar los documentos inviolables reales del proyecto.
   - Crear la estructura inicial de `project_docs/ROADMAP.md` con los primeros bloques.
   - Definir dependencias entre bloques en `project_docs/block_graph.yaml`.

## Stubs

### `project_docs/session_locks.yaml`

```yaml
# Fuente de verdad para coordinacion entre sesiones Claude Code paralelas.
# Los agentes leen este archivo al arrancar un bloque y escriben al cerrar.
# Para vista humana rapida: tabla "Bloques activos" en MEMORY.md (se mantiene en paralelo).
#
# Protocolo:
# - Apertura de bloque → append entry aqui (ver workflow.md "Trigger: apertura de bloque")
# - Cierre de bloque    → remove entry de aqui
# - Si owned_files de una nueva sesion intersecta con otra activa → BLOCKED (serie obligatoria)
#
# Formato de cada entry:
#   block: "B1"                           # ID del bloque del ROADMAP
#   session_id: "YYYY-MM-DD-model-slug"   # identificador libre pero unico
#   started: "YYYY-MM-DDTHH:MM"           # timestamp de apertura
#   owned_files:                          # archivos que la sesion va a tocar
#     - "path/relativo/al/repo"
#   owned_domains:                        # dominios del mapa workflow.md
#     - "backend"
#   plan_file: "project_docs/active_plans/<session_id>.md"  # null si no requiere plan persistente
#   notes: "opcional — razon, estado parcial, etc."

active_sessions: []
```

### `project_docs/block_graph.yaml`

```yaml
# Grafo de bloques: dependencias y archivos tocados por cada bloque.
# Los agentes leen este archivo en el pre-flight para validar dependencias y calcular locks.
#
# Formato:
# blocks:
#   B1:
#     depends_on: []                      # lista de bloques prerequisitos
#     touches:                            # archivos/directorios que el bloque va a tocar
#       - "src/module/..."
#     domains: ["backend"]                # dominios afectados

blocks: {}
```

### `project_docs/ROADMAP.md`

```markdown
# Roadmap del proyecto

> Bloques de trabajo ordenados. Cada bloque es una unidad de sesion cerrable.
> Formato de estado: `PENDIENTE` / `EN CURSO` / `HECHO YYYY-MM-DD`.

## Bloques

| N | Nombre | Dominio | Estado |
|---|--------|---------|--------|
| 1 | ... | ... | PENDIENTE |
```

### `project_docs/active_plans/README.md`

```markdown
# Active Plans

Este directorio contiene los **planes multi-paso en curso** de sesiones Claude Code activas. Es el mecanismo de persistencia que permite retomar un bloque si la sesion se interrumpe (corte de luz, red, caida de servidores, crash del cliente).

## Contrato

- **Un archivo por sesion activa** con plan multi-paso, nombrado `<session_id>.md` (el mismo `session_id` que aparece en `project_docs/session_locks.yaml`).
- **Fuente de verdad unica** del progreso de la sesion. No duplicar en `TaskCreate` salvo para la UI local de la sesion actual.
- **Se borra al cerrar el bloque** como parte del trigger de cierre (no se archiva — el historico vive en `docs/DEVLOG.md` y los commits).
- **Se detecta al arrancar sesion nueva** — si hay archivos aqui cuyo `session_id` esta en `session_locks.yaml`, Kadid pregunta al usuario si retoma, descarta, o es otra sesion viva.

Ver contrato completo en `.claude/rules/workflow.md` → seccion "Persistencia de planes multi-paso".
```

### `project_docs/questions_for_human.md`

```markdown
# Preguntas pendientes para el humano

> Cola de decisiones que Kadid (u otro agente) no puede resolver sin input humano.
> Formato: Q-NNN, bloque, fecha, dominio, pregunta, contexto, intentado, bloqueante (S/N).

## Pendientes

_(vacio)_

## Resueltas

_(vacio)_
```

### `docs/DEVLOG.md`

```markdown
# DEVLOG

> Log canonico de decisiones tecnicas y cierres de bloque. Una entrada por bloque cerrado.
```

## Pendiente — Worktrees + hook ownership (CD-078, 2026-05-01)

El template `WORKFLOW-template.md` v2.0 NO incluye aun la seccion "Paralelismo, worktrees y hook de ownership" introducida por CD-078 el 2026-05-01. Cuando se actualice a v3.0 incorporara:
- Lista canon `shared_metadata` (transversales que no chocan en pre-flight).
- Worktrees por sesion paralela (`git worktree add ../<proyecto>-worktrees/<session_id>`).
- Hook pre-commit (`.githooks/pre-commit` + `git config core.hooksPath .githooks`).
- Politica merge canon (`git rebase origin/main` + tests post-rebase + `git merge --no-ff` + push con reintento + cleanup atomico).
- Recuperacion de worktrees huerfanos.

Mientras tanto, en proyectos instanciados con v2.0 que adopten CD-078 manualmente, crear un `.githooks/pre-commit` propio y ejecutar `git config core.hooksPath .githooks` en el clone. Adaptar la lista `shared_metadata` del hook a los archivos transversales del proyecto.

## Guardrails

- Nunca sobrescribir archivos existentes sin crear un `.bak` primero y confirmar con el usuario.
- Nunca ejecutar en `~/.claude` o directorios home — solo en raices de proyecto con `.git/`.
- Nunca modificar el template `~/.claude/hive/templates/WORKFLOW-template.md`. Esta skill SOLO lee el template, nunca lo escribe.
- Nunca rellenar placeholders con valores inventados. Si el usuario no sabe uno, dejarlo explicito con `<TODO: rellenar>` y listarlo en el informe final.
- Nunca crear `.claude/rules/workflow.md` sin el marker de version como primera linea — es lo que permite futuras actualizaciones.
- Si el proyecto usa una raiz de docs distinta a `project_docs/` (p.ej. `docs/`), preguntar al usuario si quiere adoptar la convencion Hive (`project_docs/`) o mantener la suya. Si mantiene la suya, avisar que algunos agentes pueden no encontrar los archivos.
