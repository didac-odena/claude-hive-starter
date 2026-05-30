# [Nombre del Proyecto] — Project Memory

## What is [Proyecto]
- [Descripcion breve del proyecto en 2-3 lineas]

## Sistema Hive — Agentes

13 agentes en 3 niveles. Invocar con `/agents/nivel/nombre`.
- **Estrategia:** /kadid (orquestador+guardian), /cto (arquitectura+seguridad), /cpo (producto+legal-producto)
- **Direccion:** /pm (coordinacion), /engineering-director (calidad+QA+data), /product-director (specs+UX), /marketing-legal (marketing+compliance+contenido legal), /finance-director (modelo economico+costes), /secre (briefing+agenda)
- **Ejecucion:** /backend-lead, /frontend-lead, /devops-lead, /content-lead
- **Coordinacion:** `project_docs/cross_decisions.md`
- **FUNDAMENTALS.md:** documentos inviolables del proyecto
- **Escalado:** Ejecucion → Direccion → Estrategia

## Sistema Hive — Protocolo de trabajo

Hive es nativo: siempre activo, no requiere invocacion. Los triggers estan en `.claude/rules/workflow.md`.

### Inicio de sesion
Di: **"Bloque [N] — [nombre]"** o **"Fase [N]"**
1. Pre-flight automatico: cross_decisions + dependencias + contexto del dominio.
2. Confirma en una linea que va a hacer → ejecuta.

### Cierre de sesion
Di: **"cierra bloque"** o similar. Trigger automatico en `.claude/rules/workflow.md`.

### Bloques activos
| Bloque | Tarea | Modelo | Fase |
|---|---|---|---|
| - | - | - | - |

## Workflow — preferencias usuario
- Chat en espanol (Espana). Codigo en ingles.
- Al ~80% tokens: parar, guardar, avisar.

## Misc
- DEVLOG: `docs/DEVLOG.md` (canonico)
