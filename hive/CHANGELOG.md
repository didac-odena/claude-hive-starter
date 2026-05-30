# Changelog — Claude-Hive

## [2.0.0] — 2026-04-12

### Changed
- Renombrado: Sistema Imperium → Sistema Hive
- Reestructuracion completa: 33 agentes → 11 agentes en 3 niveles (Estrategia, Direccion, Ejecucion)
- Nuevo agente Kadid (Fundador): guardian de FUNDAMENTALS, orquestador, decisor de direccion
- Orquestacion nativa: Hive siempre activo, no hay que pedirlo
- Workflow con flujo real: pre-flight → planificacion → ejecucion → revision → informe
- Comites entre agentes para resolver desacuerdos
- FUNDAMENTALS.md: documentos inviolables por proyecto
- Guardrail anti-edicion-paralela: agentes en paralelo solo para analisis
- Subagentes usan modelo de sesion (opus) en vez de haiku
- Hook renombrado: imperium-remind.py → hive-remind.py

### Agentes fusionados
- CTO absorbe Security Director
- CPO absorbe CLO
- Engineering Dir absorbe QA Lead + Data Lead
- Product Dir absorbe UX Lead
- Marketing & Legal absorbe CMO + Marketing Dir + Compliance Dir + 5 especialistas
- Backend Lead absorbe API Designer + DB Architect + Integration + Perf + Security Engineer
- Frontend Lead absorbe UI Developer + SEO Specialist
- DevOps Lead absorbe CI/CD Engineer + Monitoring Engineer
- Content Lead absorbe Copywriter + Social Media + Email Marketing + Community Manager

### Removed
- 22 agentes eliminados (fusionados en los 11 nuevos)
- Carpetas nivel-0, nivel-1, nivel-2, nivel-3 eliminadas
- CLAUDE_CODE_SUBAGENT_MODEL haiku eliminado

## [1.1.0] — 2026-04-10

### Changed
- Reescritura completa de los 33 agentes para portabilidad
- Eliminadas todas las referencias hardcodeadas a proyectos concretos
- Nuevo patron: agente = CV generico, context files = conocimiento del proyecto

## [1.0.0] — 2026-04-10

### Added
- 33 agentes organizados en 4 niveles (C-Suite, Direccion, Leads, Especialistas)
- 10 skills reutilizables
- Capa de coordinacion: cross_decisions.md, pre-flight checks, post-validation
- 5 templates
- Documentacion: ARCHITECTURE.md, AGENTS.md, TOKEN-EFFICIENCY.md
