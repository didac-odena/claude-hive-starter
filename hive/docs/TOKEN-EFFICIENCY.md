# Token Efficiency — Guia de gestion de tokens

## Principios

1. **Exploration-first**: usar Grep/Glob antes de Read. Solo abrir un archivo cuando una busqueda confirma que es el correcto.
2. **Read once**: no leer el mismo archivo dos veces en una sesion salvo que haya cambiado.
3. **Context isolation**: cada agente lee solo sus archivos obligatorios, no todo el proyecto.
4. **Compact output**: tests con `--tb=short -q`, logs filtrados, sin dumps innecesarios.
5. **RTK**: el hook rtk-rewrite.sh comprime output de git, pytest, ls, tree, find automaticamente.

## Estrategias por fase de sesion

### Al abrir sesion
- MEMORY.md se carga automaticamente (mantener < 200 lineas)
- Leer solo el context file del dominio relevante
- NO leer ROADMAP.md salvo inicio de fase nueva o cierre de bloque

### Durante el trabajo
- Archivos target (editar, debuggear): leer completos
- Archivos auxiliares (verificar import, check util): usar offset/limit
- Para buscar: Grep > Glob > Read. Nunca find/cat via bash
- **Ediciones siempre secuenciales** — no lanzar multiples agentes editando en paralelo

### Al cerrar sesion
- MEMORY.md: actualizar solo si hay info estable y reutilizable
- Context files: actualizar con decisiones y artefactos
- Si ~80% tokens (autocompact al 70%): parar, guardar estado, avisar al usuario

## MEMORY.md — buenas practicas

### Que incluir
- Decisiones canonicas confirmadas en multiples sesiones
- Arquitectura clave, paths criticos, estructura del proyecto
- Preferencias de workflow del usuario
- Soluciones a problemas recurrentes

### Que NO incluir
- Estado de la sesion actual (task in-progress, temp state)
- Info no verificada o de una sola lectura
- Duplicados de CLAUDE.md o rules files
- Especulaciones

### Mantener compacto
- Limite: 200 lineas (las demas se truncan en carga)
- Usar archivos satelite para detalle (memory/completed_phases.md, etc.)
- Linkear desde MEMORY.md a los satelites

## Agentes y tokens

### Por que 3 niveles
No es burocracia — es para aislar contexto:
- Un Content Lead no necesita leer el schema de la DB
- Un Backend Lead no necesita leer la estrategia de marketing
- Solo Kadid y el nivel Estrategia leen todo (y solo cuando hay conflictos)

### Coste por nivel (aproximado)
| Nivel | Archivos que lee | Tokens estimados |
|-------|-----------------|-----------------|
| Ejecucion | 1-2 context + reglas | ~2-4k |
| Direccion | 2-4 context + docs de area | ~4-10k |
| Estrategia | Todos los context + MEMORY + ROADMAP + FUNDAMENTALS | ~15-25k |

### Cuando usar cada nivel
- Tarea acotada en un dominio → ejecucion (minimo contexto)
- Tarea cross-domain o de coordinacion → direccion
- Conflicto, decision estrategica, o verificacion de FUNDAMENTALS → estrategia
- Duda sobre donde escalar → PM (direccion)

## Config de tokens activa

| Setting | Valor | Efecto |
|---------|-------|--------|
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | 70 | Compacta contexto al 70% para mantenerlo limpio |
| `CLAUDE_CODE_SUBAGENT_MODEL` | (no definido) | Subagentes usan el modelo de la sesion (opus) |
| RTK hook | Activo | Comprime output de git, pytest, ls, tree, find |
| Status line | Activo | Muestra modelo, CTX%, banda horaria (ECO/OK/PICO) |

## Rules files vs CLAUDE.md vs MEMORY.md

| Archivo | Proposito | Carga | Edicion |
|---------|-----------|-------|---------|
| CLAUDE.md (global) | Reglas universales (idioma, naming, YAGNI) | Automatica siempre | Rara vez |
| CLAUDE.md (proyecto) | Reglas del proyecto | Automatica siempre | Cuando cambia el stack |
| .claude/rules/*.md | Reglas por dominio tecnico | Automatica siempre | Cuando cambian las reglas |
| MEMORY.md | Estado del proyecto y decisiones | Automatica siempre | Cada cierre de bloque |
| context/*.md | Estado por dominio | Bajo demanda (agente lee) | Cada cierre de bloque |
| FUNDAMENTALS.md | Documentos inviolables | Bajo demanda (Kadid lee) | Solo con aprobacion usuario |

## Anti-patrones

- Leer ROADMAP.md en cada sesion "por si acaso" → solo cuando sea necesario
- Lanzar agentes editando en paralelo → los cambios no se persisten. Solo analisis en paralelo.
- Guardar en MEMORY info de sesion actual → se desactualiza y ocupa espacio
- Leer archivos enteros para buscar una linea → usar Grep primero
- Usar agente de Estrategia para tarea de Ejecucion → desperdicio de tokens de contexto
- Agente reporta "hecho" sin verificar → siempre comprobar que los cambios estan en disco
