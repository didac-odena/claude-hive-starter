# Changelog — Claude-Hive Starter

## [starter] — version agnostica

Version portable y sin referencias a ningun proyecto concreto, lista para instanciar.

### Incluye
- 13 agentes en 3 niveles (Estrategia, Direccion, Ejecucion), orquestados por Kadid.
- Workflow de bloques: pre-flight (locks + dependencias) → planificacion → ejecucion → post-validation → cierre con DEVLOG.
- Hooks portables: `rtk-rewrite.sh` (compresion de tokens), `routing-check.py` (ownership por bloque), `hive-remind.py` (aviso de cambios sin commit).
- Skills reutilizables (commit-devlog, conventions, design-review, fix-bug, generate-tests, optimize-repo, perf-check, security-scan, skill-creator, skill-installer, init-project-workflow) + comandos del Hive Bridge.
- Templates por proyecto: FUNDAMENTALS, MEMORY, WORKFLOW, cross-decisions, context-domain, rules-domain.
- `settings.json.example` sin secretos.

### Principios
- Orquestacion nativa: el sistema esta siempre activo, no hay que pedirlo.
- FUNDAMENTALS.md por proyecto: documentos inviolables que Kadid protege.
- Edicion secuencial: agentes en paralelo solo para analisis, nunca para editar archivos.
- Aislamiento de contexto: cada agente lee solo lo que necesita.
