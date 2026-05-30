# Claude-Hive

Sistema de agentes multi-nivel para Claude Code. Organiza tu proyecto como un equipo con jerarquia: Estrategia, Direccion y Ejecucion, coordinado por un orquestador (Kadid).

## Estructura del repo

Este repo se clona como `~/.claude/`. Al clonarlo ahi, todo queda en su sitio nativo:

```
~/.claude/                          ← ESTE REPO
├── .gitignore                      # Excluye lo especifico de maquina
├── CLAUDE.md                       # Reglas globales (coding, naming, idioma)
├── settings.json.example           # Plantilla de config (hooks + permisos), sin secretos
├── status.py                       # Status line
│
├── commands/                       # Skills reutilizables
│   ├── commit-devlog.md, conventions.md, design-review.md, ...
│   ├── init-project-workflow.md
│   ├── hive-claim.md, hive-inbox.md, hive-list.md, hive-send.md
│   └── agents/                     # Sistema Hive (13 agentes)
│       ├── estrategia/             # Kadid, CTO, CPO
│       ├── direccion/              # PM, Eng Dir, Product Dir, Marketing & Legal, Finance, Secre
│       └── ejecucion/              # Backend, Frontend, DevOps, Content
│
├── hooks/                          # rtk-rewrite.sh, routing-check.py, hive-remind.py
│
└── hive/                           # Docs de la metodologia
    ├── README.md                   # Este archivo
    ├── SETUP.md                    # Instrucciones de instalacion
    ├── CHANGELOG.md
    ├── kadid-profile.md            # Criterio de decision de Kadid
    ├── training-protocol.md
    ├── docs/                       # ARCHITECTURE.md, AGENTS.md, TOKEN-EFFICIENCY.md
    ├── orchestrator/               # Orquestador de planes multi-agente
    └── templates/                  # Plantillas para proyectos nuevos
```

## Que incluye

### 13 Agentes en 3 niveles
- **Estrategia (3):** Kadid (orquestador/guardian), CTO, CPO
- **Direccion (6):** PM, Engineering Director, Product Director, Marketing & Legal, Finance Director, Secre
- **Ejecucion (4):** Backend Lead, Frontend Lead, DevOps Lead, Content Lead

### Skills reutilizables
commit-devlog, conventions, design-review, fix-bug, generate-tests, optimize-repo, perf-check, security-scan, skill-creator, skill-installer, init-project-workflow, y los comandos del Hive Bridge (hive-*).

### Capa de coordinacion
- `cross_decisions.md` — registro de decisiones multi-dominio
- Pre-flight check al abrir bloque (locks + dependencias)
- Post-validation al cerrar bloque

## Como usar

Ver `SETUP.md` para instalacion y configuracion de proyectos nuevos.

## Invocacion de agentes

```
/agents/estrategia/kadid          — Orquestacion, guardian de FUNDAMENTALS
/agents/direccion/pm              — Coordinacion de bloques
/agents/ejecucion/backend-lead    — Trabajo backend
```

## Escalado

```
Ejecucion → Direccion → Estrategia → Owner del proyecto
```
