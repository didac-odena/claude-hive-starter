<!-- hive-workflow-template: v2.0 -->
<!-- Placeholders a rellenar al instanciar:
       {TEST_COMMAND}       → comando de ejecucion de tests del proyecto (p.ej. `npm test`, `pytest`, `go test ./...`)
       {DOMAIN_MAP}         → mapa bloque→context file del proyecto (seccion "Mapa bloque → context file" al final)
     Todo lo demas son convenciones Hive fijas (no tocar).
-->

# Workflow Rules

## Principio rector: calidad > velocidad

Hacer las cosas bien a la primera cuesta menos que hacerlas rapido y tener que volver. Este principio esta por encima de cualquier otra optimizacion — tiempo, tokens, cantidad de bloques cerrados, plazo del MVP.

Que significa en la practica:
- Un bloque mal cerrado NO esta cerrado. Es deuda camuflada.
- Los pasos de este workflow no son sugerencias. Son controles de calidad. Saltarselos introduce deuda.
- Si un paso dice "verificar X", se verifica. No se asume.
- Cero atajos que obliguen a volver mas tarde. Si algo huele a "lo pulo luego", o se arregla ahora o se bloquea el cierre.
- Kadid bloquea cualquier trabajo que viole este principio, aunque eso retrase la sesion. Retrasar una sesion para hacerla bien siempre sale mas barato que cerrarla mal y volver.

Este principio aplica a TODOS los agentes del sistema Hive, sin excepcion.

## Sistema Hive — Orquestacion nativa
Hive esta siempre activo. No requiere invocacion explicita. Los agentes se invocan con `/agents/nivel/nombre`.
Catalogo: `~/.claude/commands/agents/` (estrategia, direccion, ejecucion).
Escalado: Ejecucion → Direccion → Estrategia. PM coordina entre bloques.
Documentos inviolables: `project_docs/FUNDAMENTALS.md`.

## REGLA PRINCIPAL — Declaracion obligatoria de agente

Antes de ejecutar cualquier tarea que modifique archivos, Claude Code debe declarar en una linea:

**[Agente: nombre] — tarea que va a ejecutar**

Si no hay agente apropiado para la tarea, declarar:

**[Directo] — razon por la que no se usa agente**

Esto aplica SIEMPRE. No hay excepcion. Si Claude Code se encuentra ejecutando trabajo sin haber declarado agente, debe parar, declarar, y continuar.

Al cierre de bloque, el informe final debe incluir una seccion:

### Agentes utilizados
| Agente | Tareas realizadas |
|--------|-------------------|
| (lista) | (lista) |

Si la tabla esta vacia o solo dice "Directo", Kadid debe evaluar si se deberian haber usado agentes y registrarlo como observacion.

## Regla de ejecucion
- REGLA CRITICA: ediciones de archivos siempre secuenciales o directas, NUNCA en paralelo. Agentes en paralelo solo para analisis/planificacion. Tras cada edicion de agente, verificar que los cambios se persistieron.

## Reglas transversales de calidad

Las 4 reglas de esta seccion son invariantes de calidad Hive. Aplican a cualquier sesion que modifique codigo, no solo a sesiones de auditoria/remediacion. Todas nacen de incidentes reales en proyectos previos donde su ausencia introdujo deuda invisible.

### Regla 1 — Test delta obligatorio

Cuando una sesion toque codigo cubierto por tests existentes:

1. **Antes** del primer cambio → ejecutar `{TEST_COMMAND}` y registrar el baseline en la primera linea del reporte de sesion con este formato exacto:
   `Tests baseline: X pass / Y fail [lista de nombres de los tests que fallan]`
2. **Despues** del ultimo cambio → re-ejecutar el mismo comando.
3. Si el numero o la identidad de los tests fallando cambia entre ambas ejecuciones, los nuevos fallos son **regresiones de esta sesion** y DEBEN arreglarse antes de cerrar. No se puede marcar como "pre-existente, fuera de scope" ningun test que no apareciese en el baseline.
4. Si los mismos tests siguen fallando con el mismo error, documentarlo en el cierre como "baseline intacto" y continuar.

**Por que**: sin baseline capturado al inicio, no hay forma de distinguir tests pre-existentes fallidos de regresiones introducidas en la propia sesion. Esa ambiguedad enmascara deuda y se paga en la auditoria siguiente.

**Aplica a**: todos los agentes de ejecucion (backend-lead, frontend-lead, devops-lead) y sesiones [Directo] que toquen codigo con tests.

### Regla 2 — Prohibicion de findings PARTIAL sin seguimiento

Un finding en un reporte de auditoria/remediacion NO puede cerrarse como `[PARTIAL]`. Las unicas opciones validas son:

- `[FIXED]` — resuelto completamente.
- `[DEFERRED]` — con bloqueo concreto nombrado Y subtarea o bloque creado segun la regla de decision de scope del proyecto (>30 min de trabajo → bloque nuevo, <30 min → subtarea dentro del bloque actual). El finding debe enlazar al bloque/subtarea.
- `[ACCEPTED]` — falso positivo o riesgo aceptado con justificacion explicita.

Si un fix se aplica parcialmente: el finding se marca `[FIXED]` por la parte resuelta, y se abre un finding nuevo (con su propia severidad y clasificacion) para la parte pendiente. **Nunca PARTIAL.**

**Por que**: un finding `[PARTIAL]` sin subtarea ni bloque de seguimiento flota como deuda invisible y solo se detecta en la revision posterior — cuando ya costara mas arreglarlo.

**Aplica a**: cualquier agente o skill que genere o gestione reports de findings (backend-lead, security-scan, audit flows, PM, engineering-director).

### Regla 3 — Tope de findings por commit

Durante sesiones de remediacion o refactor, un commit puede agrupar multiples findings SOLO si:

- Todos tocan el **mismo archivo**, o
- Todos tocan archivos del **mismo modulo/directorio** Y son de la **misma categoria** (misma clase de vulnerabilidad, mismo tipo de refactor).

Tope maximo: **4 findings por commit** si los findings tocan archivos distintos. Si hay mas, dividir en commits separados por subdominio.

**Excepcion**: cambios puramente cosmeticos (typos, formatting, renombrado de constantes) pueden agruparse sin limite si no cambian logica ejecutable.

**Por que**: agrupar findings heterogeneos en un solo commit hace inviable el rollback quirurgico y contradice el principio de atomicidad — un solo fix roto obliga a revertir todo el grupo.

**Aplica a**: todos los agentes de ejecucion durante sesiones de remediacion, refactor o auditoria.

### Regla 4 — CRITICAL interino → bloque obligatorio en la misma sesion

Si un finding CRITICAL se resuelve con un fix interino (workaround, feature flag, disable temporal, descarte de eventos, stub), en la MISMA sesion se debe completar los 3 pasos siguientes antes de poder cerrar:

1. **Crear bloque nuevo en `project_docs/ROADMAP.md`** con la resolucion definitiva. Un CRITICAL siempre es >30 min de trabajo, por tanto la regla de scope siempre exige bloque (nunca subtarea).
2. **Registrar cross-decision** en `project_docs/cross_decisions.md` con formato estandar, enlazando al finding y al bloque creado.
3. **Anadir marca `⚠️ INTERINO — resolucion en B[XX]`** al mensaje de commit del fix interino, de forma que `git log` exponga la deuda sin necesidad de abrir el audit report.

**No se puede cerrar la sesion sin estos 3 pasos completados.** Kadid es responsable de verificar cumplimiento en el gate de cierre.

**Por que**: un CRITICAL con fix interino y sin plan de resolucion es deuda invisible — peor, una deuda que el equipo cree resuelta. Obligar al bloque + cross-decision + marca en commit garantiza que `git log` y el ROADMAP exponen la deuda en todos los canales.

**Aplica a**: todos los agentes. Kadid bloquea el cierre si los 3 pasos no estan hechos.

## Persistencia de planes multi-paso

**Problema**: `TaskCreate` es solo en memoria. Si la sesion se cae (corte de luz, red, caida de servidores) durante la ejecucion de un plan multi-paso, se pierde el contexto de por donde iba el trabajo. La siguiente sesion arranca desde cero y obliga a reconstruir el plan.

**Solucion**: cuando Kadid (u otro agente) aprueba un plan multi-paso, el plan se persiste en disco como archivo markdown con checkboxes, que se actualiza tras cada paso completado y se borra al cerrar el bloque.

### Cuando es obligatorio

- El bloque tiene **≥3 pasos diferenciados** en su plan de ejecucion, O
- Kadid aprueba un plan explicito al arrancar el bloque, O
- La sesion es multi-hora (>1h estimada).

Para sesiones cortas [Directo] (≤2 ediciones, ≤15 min) es opcional.

### Formato del archivo

Ruta: `project_docs/active_plans/<session_id>.md`

Plantilla minima:
```markdown
# Plan — <Bloque o tarea> — <titulo corto>

**Session ID**: <session_id>
**Bloque**: B<N> (o "[Directo]")
**Creado**: YYYY-MM-DDTHH:MM
**Estado**: IN_PROGRESS | PAUSED | ORPHAN

## Pasos

- [ ] 1. Paso concreto y verificable
- [ ] 2. Paso concreto y verificable
- [ ] 3. ...

## Notas
(contexto libre: decisiones tomadas, bloqueos, etc.)
```

### Actualizacion durante la sesion

- Al completar un paso → marcar `[x]` inmediatamente, antes de arrancar el siguiente. No batch.
- Si se descubre un paso nuevo no previsto → anadirlo a la lista con marca `(added)` para trazabilidad.
- Si se bloquea → cambiar `Estado: PAUSED` + anotar motivo en "Notas".

### Puntero desde session_locks.yaml

Cada entry en `active_sessions` debe incluir el campo `plan_file` con la ruta relativa al archivo (o `null` si la sesion no requiere plan persistente). El `plan_file` es la fuente de verdad unica del progreso — NO duplicar en `TaskCreate` salvo para UI local de la sesion actual.

### Borrado al cerrar bloque

El trigger de cierre elimina el archivo de `active_plans/` como parte del paso de release lock. No se archiva — el historico queda en el DEVLOG y el commit.

### Recuperacion de plan huerfano

Ver trigger "Recuperacion de plan huerfano" mas abajo.

**Aplica a**: Kadid y cualquier agente que orqueste planes multi-paso. Kadid verifica en el pre-flight que el plan_file existe si el bloque lo requiere.

## Trigger: apertura de bloque (pre-flight)
Cuando el usuario diga "Bloque [N] — [nombre]" o similar, ANTES de empezar:

1. **Lock check**: leer `project_docs/session_locks.yaml`. Calcular los archivos que este bloque va a tocar (consultar `project_docs/block_graph.yaml` → `touches` del bloque). Si algun archivo intersecta con los `owned_files` de otra sesion activa → reportar **BLOCKED por colision de archivo** con el bloque en conflicto. NO continuar.
2. **Dependency check**: leer `project_docs/block_graph.yaml` → `depends_on` del bloque. Verificar en ROADMAP.md que todas las dependencias estan HECHO. Si alguna no lo esta → reportar **BLOCKED por dependencia** con el bloque que falta.
3. Leer `project_docs/cross_decisions.md` — buscar decisiones activas que afecten al dominio del bloque
4. Leer `project_docs/context/[dominio].md` — estado actual del dominio
5. Si hay decisiones PENDING que afecten: informar al usuario antes de continuar
6. Si todo OK: **adquirir lock** → anadir entry al `active_sessions` de `session_locks.yaml` con `block`, `session_id` (formato: `YYYY-MM-DD-<model>-<slug>`), `started`, `owned_files` (los del block_graph), `owned_domains`, y `plan_file` (ruta del archivo si aplica, o `null`). Tambien anadir/actualizar fila en la tabla "Bloques activos" de `MEMORY.md` (la tabla es referencia rapida para humanos, el YAML es fuente de verdad para agentes).
7. **Crear plan file si aplica**: si el bloque tiene ≥3 pasos diferenciados, Kadid aprueba plan explicito, o la sesion es >1h → crear `project_docs/active_plans/<session_id>.md` con la plantilla de la seccion "Persistencia de planes multi-paso". Actualizar el campo `plan_file` de la entry en `session_locks.yaml` con la ruta relativa.
8. Reportar READY y continuar con el protocolo normal.

Si durante el bloque se descubre que hay que tocar archivos adicionales no listados en `block_graph.yaml` → actualizar `touches` del bloque en block_graph + `owned_files` de la entry en session_locks ANTES de editarlos, y volver a verificar que no colisionan con otra sesion activa.

## Trigger: recuperacion de plan huerfano (inicio de sesion)

Al arrancar cualquier sesion nueva (antes del primer mensaje de trabajo del usuario), Kadid debe:

1. Leer `project_docs/session_locks.yaml` → `active_sessions`.
2. Si hay alguna entry con `plan_file` NO nulo → existen planes de sesiones previas que pueden estar huerfanos (la sesion previa no cerro correctamente, por caida o interrupcion).
3. Para cada entry con `plan_file`:
   - Leer el archivo del plan.
   - Resumir al usuario: bloque, session_id, pasos completados (`[x]`) y pendientes (`[ ]`), fecha de creacion.
4. Preguntar al usuario: **¿retomas el plan, lo descartas, o era otra sesion viva que sigue en curso?**
   - **Retomar** → marcar el plan como `Estado: IN_PROGRESS` de nuevo, adquirir el lock para la sesion actual (nuevo `session_id`), renombrar el archivo a `<nuevo_session_id>.md` y continuar desde el primer paso pendiente.
   - **Descartar** → eliminar el archivo del plan + la entry de `session_locks.yaml` + la fila de "Bloques activos" en MEMORY.md. Dejar los cambios del ROADMAP/archivos tocados como esten (el usuario decidira si revertirlos en la nueva sesion).
   - **Otra sesion viva** → no tocar nada, continuar con la sesion actual en otro bloque.
5. Solo despues de resolver todos los planes huerfanos se puede continuar con el trabajo del usuario.

**Por que**: sin esta verificacion, los planes persistidos se acumularian como ficheros huerfanos y perderian su utilidad. La recuperacion explicita es lo que cierra el ciclo.

## Trigger: decision cross-domain
Cuando una decision tomada durante una sesion afecte a 2+ dominios:

1. Registrar en `project_docs/cross_decisions.md` con formato estandar
2. Informar al usuario de los dominios afectados
3. Si el agente actual no tiene autoridad sobre todos los dominios → escalar al agente de Estrategia correspondiente

## Trigger: contradiccion con FUNDAMENTALS
Cuando cualquier decision o cambio contradiga un documento listado en `project_docs/FUNDAMENTALS.md`:

1. BLOQUEAR la decision inmediatamente
2. Citar el documento fundamental y la seccion que se contradice
3. Informar al usuario con alternativas que SI cumplan
4. Solo proceder si el usuario acepta explicitamente la excepcion

## Trigger: modificacion de agentes o skills
Cuando se cree, modifique o elimine un archivo en `~/.claude/commands/` (agentes o skills):

1. Al final de la sesion, si hubo cambios en agentes/skills, recordar al usuario hacer commit/push en `~/.claude/` (repo Claude-Hive)

## Trigger: cierre de bloque
Cuando el usuario diga "cierra bloque", "cierra el bloque", "cierra sesion", "bloque terminado", "bloque hecho" o similar:

1. **Post-validation**:
   - Verificar que no quedan decisiones PENDING en cross_decisions.md para este bloque.
   - **Test delta (regla 1)**: re-ejecutar tests y comparar con el baseline capturado al inicio. Si aparecieron fallos nuevos → arreglarlos antes de seguir con el cierre.
   - **Findings PARTIAL (regla 2)**: si esta sesion genero o gestiono findings, verificar que ninguno quedo como `[PARTIAL]`. Si alguno lo esta → reclasificar segun regla 2 antes de cerrar.
   - **CRITICAL interino (regla 4)**: si esta sesion aplico fix interino a un CRITICAL, verificar que existe bloque en ROADMAP, entry en cross_decisions.md, y marca `⚠️ INTERINO` en el commit. Si falta alguno → bloquear cierre.
2. **Commit acotado por owned_files**: si hay sesiones paralelas activas en `session_locks.yaml`, el commit de este bloque SOLO puede tocar los archivos listados en `owned_files` de su propia entry (mas `session_locks.yaml` y la tabla "Bloques activos" de MEMORY.md). NUNCA usar `git add -A`, `git add .`, ni `git commit -a`. Stagear archivo por archivo con `git add <path>` usando la lista de `owned_files`. Si `/commit-devlog` u otro skill hace `git add` amplio, saltarlo y commitear manualmente.
   - Si la sesion detecta que hay cambios en archivos FUERA de sus `owned_files` (trabajo residual, otra sesion sin cerrar, linter) → NO incluirlos, reportar al usuario que quedan cambios sin commitear.
   - Si es la UNICA sesion activa (ningun otro entry en `session_locks.yaml`) → se permite `/commit-devlog` con staging amplio como antes.
3. Ejecutar `/commit-devlog` (solo si unica sesion) o commit manual acotado (si hay paralelismo)
4. **Release lock**: eliminar la entry de este bloque de `project_docs/session_locks.yaml` (`active_sessions`). Tambien quitar del `block_graph.yaml` si ya no aplica (bloques HECHO se omiten del grafo). Si la entry tenia `plan_file`, **borrar el archivo** de `project_docs/active_plans/<session_id>.md` en el mismo paso (no archivar — el historico vive en DEVLOG/commit).
5. **Marcar bloque HECHO en `project_docs/ROADMAP.md` — TODAS las apariciones del bloque**:
   - Un bloque puede vivir en MULTIPLES tablas del ROADMAP (roadmap por fases, clasificacion de bloques, etc.). TODAS deben quedar con `| N ✅ |` + `HECHO YYYY-MM-DD`.
   - **Antes de editar**, listar todas las filas del bloque con grep: `grep -n "^| N " project_docs/ROADMAP.md` (sustituir N por el numero del bloque). Esa lista es la verdad de cuantas ediciones hay que hacer.
   - **Despues de editar**, re-ejecutar el mismo grep y verificar que TODAS las filas muestran ✅. Si alguna no lo tiene, el cierre NO esta completo — volver y arreglar antes de continuar.
   - **En el informe final al usuario**, pegar la lista de lineas del ROADMAP tocadas (formato `ROADMAP.md:213`, `ROADMAP.md:399`, etc.) como prueba de control. Esto no es opcional — es la unica forma de detectar desincronizaciones antes de que se acumulen.
6. Actualizar `project_docs/context/[dominio].md` con decisiones y artefactos producidos
7. Mover decisiones cross-domain de este bloque a estado IMPLEMENTED en cross_decisions.md
8. Eliminar el bloque de la tabla "Bloques activos" en MEMORY.md
9. Reportar al usuario los commits realizados

## Trigger: pregunta no resoluble por Kadid
Cuando un agente (incluido Kadid) necesita una decision humana y no puede resolverla con el contexto disponible (FUNDAMENTALS, PRD, cross_decisions, context files):

1. Anadir entry a `project_docs/questions_for_human.md` seccion "Pendientes" con el formato estandar (Q-NNN, bloque, fecha, dominio, pregunta, contexto, intentado, bloqueante)
2. Si la pregunta NO es bloqueante → continuar trabajando en lo que si se puede avanzar
3. Si SI es bloqueante para todo el bloque → reportar al usuario y pausar
4. Cuando el usuario responda → mover la Q a "Resueltas" con la respuesta

## Mapa bloque → context file

<!-- {DOMAIN_MAP}
     Rellenar al instanciar el template. Ejemplo de formato (sustituir por los dominios reales del proyecto):

     - Producto (bloques 1,2,...) → `context/product.md`
     - Branding (bloques 3,...) → `context/branding.md`
     - Legal (bloques 4,...) → `context/legal.md`
     - Backend (bloques 5,...) → `context/backend.md`
     - Frontend (bloques 6,...) → `context/frontend.md`
     - Infra (bloques 8,...) → `context/infrastructure.md`
     - Marketing (bloques 12,...) → `context/marketing.md`
-->
