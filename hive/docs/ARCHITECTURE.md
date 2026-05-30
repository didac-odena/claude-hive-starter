# Architecture — Sistema Hive

## Vision general

Sistema Hive organiza a Claude Code como un equipo con 13 agentes especializados en 3 niveles. Kadid (orquestador) actua como guardian y orquestador. El sistema opera de forma nativa — no hay que pedirlo.

## Componentes del sistema

### 1. Agentes (13 archivos .md)

```
~/.claude/commands/agents/
  estrategia/  (3)  — Direccion y vision (Kadid, CTO, CPO)
  direccion/   (6)  — Gestion y coordinacion (PM, Eng Dir, Product Dir, Marketing & Legal, Finance, Secre)
  ejecucion/   (4)  — Ejecucion tecnica y contenido (Backend, Frontend, DevOps, Content)
```

Cada agente define:
- **Quien eres**: rol y enfoque
- **Contexto obligatorio**: archivos que lee al activarse
- **Responsabilidades**: lista concreta
- **Output esperado**: formato de entregables
- **Decides tu / Escalas**: limites de autoridad
- **Guardrails**: restricciones

### 2. Kadid (Fundador)

Siempre activo implicitamente. Triple funcion:
- **Guardian**: verifica que nada contradiga FUNDAMENTALS.md
- **Orquestador**: selecciona agentes, coordina flujo, convoca comites
- **Decisor**: resuelve conflictos entre agentes cuando la respuesta esta en los documentos

### 3. Documentos fundamentales

`project_docs/FUNDAMENTALS.md` define por proyecto:
- Documentos inviolables (Whitepaper, PRD, etc.)
- Invariantes derivadas
- Proceso de cambio (requiere aprobacion del usuario)

### 4. Capa de coordinacion

#### cross_decisions.md
Registro de decisiones que afectan a 2+ dominios.
Estados: PENDING → APPROVED → IMPLEMENTED

#### Pre-flight (PM)
Al abrir un bloque:
1. Verificar dependencias en ROADMAP
2. Verificar cross_decisions activas
3. Leer context file del dominio
4. Resultado: READY / BLOCKED / NEEDS_REVIEW

#### Post-validation
Al cerrar un bloque:
1. Verificar entregables
2. cross_decisions sin PENDING
3. Actualizar ROADMAP, context files, MEMORY

### 5. Context files

```
project_docs/context/
  product.md         — Estado del producto
  backend.md         — Estado del backend
  frontend.md        — Estado del frontend
  infrastructure.md  — Estado de infra
  marketing.md       — Estado de marketing
  legal.md           — Estado legal
  branding.md        — Estado de marca
```

### 6. MEMORY.md

Estado del proyecto, decisiones canonicas, bloques activos. Se carga automaticamente.

### 7. Skills (custom commands)

```
~/.claude/commands/
  commit-devlog.md, conventions.md, design-review.md, fix-bug.md,
  generate-tests.md, optimize-repo.md, perf-check.md, security-scan.md,
  skill-creator.md, skill-installer.md, init-project-workflow.md,
  hive-claim.md, hive-inbox.md, hive-list.md, hive-send.md
```

## Flujo de datos

```
Usuario propone trabajo
        |
        v
   Kadid evalua: bloque formal o tarea suelta?
        |
   Si bloque formal:
        |
   PM ejecuta pre-flight
        |
   Kadid selecciona agentes + presenta plan
        |
   Usuario aprueba
        |
   Ejecucion secuencial (NUNCA ediciones en paralelo)
        |
   Revision por agente diferente al ejecutor
        |
   Cierre: post-validation + informe final
        |
   Si tarea suelta:
        |
   Ejecutar directo, verificar contra FUNDAMENTALS
```

## Escalado

```
Content Lead → Marketing & Legal → Kadid
Backend/Frontend/DevOps Lead → Engineering Dir → CTO → Kadid
Product Director → CPO → Kadid
Finance Director → Kadid
PM / Secre → Kadid
Kadid → Owner del proyecto (irreversible / dinero)
```

## Principios de diseno

1. **Nativo**: el sistema esta siempre activo, no hay que pedirlo
2. **Aislamiento de contexto**: cada agente lee solo lo que necesita
3. **Coordinacion explicita**: decisiones cruzadas se registran, no se asumen
4. **Escalado claro**: si no tienes autoridad, escalas
5. **Documentacion viva**: context files se actualizan con cada cierre de bloque
6. **FUNDAMENTALS inviolables**: Kadid bloquea cualquier contradiccion
7. **Edicion secuencial**: agentes en paralelo solo para analisis, nunca para editar archivos
8. **Portabilidad**: el sistema se instala desde este repo con SETUP.md
