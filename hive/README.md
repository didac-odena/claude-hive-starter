# Claude-Hive

Sistema de agentes multi-nivel para Claude Code. Organiza tu proyecto como una empresa con jerarquia completa: C-Suite, Directores, Leads y Especialistas.

## Estructura del repo

Este repo ES `~/.claude/`. Al clonarlo ahi, todo queda en su sitio nativo:

```
~/.claude/                          ← ESTE REPO
├── .gitignore                      # Excluye lo especifico de maquina
├── CLAUDE.md                       # Reglas globales (coding, naming, idioma)
│
├── commands/                       # Skills reutilizables (10)
│   ├── commit-devlog.md
│   ├── conventions.md
│   ├── ...
│   └── agents/                     # Sistema Hive (33 agentes)
│       ├── nivel-0/                # C-Suite (5)
│       ├── nivel-1/                # Direccion (6)
│       ├── nivel-2/                # Leads (6)
│       └── nivel-3/                # Especialistas (16)
│
└── hive/                       # Docs de la metodologia
    ├── README.md                   # Este archivo
    ├── SETUP.md                    # Instrucciones de instalacion
    ├── CHANGELOG.md
    ├── docs/
    │   ├── ARCHITECTURE.md
    │   ├── AGENTS.md
    │   └── TOKEN-EFFICIENCY.md
    └── templates/                  # Plantillas para proyectos nuevos
```

## Que incluye

### 33 Agentes en 4 niveles
- **Nivel 0 — C-Suite (5):** CEO, CTO, CPO, CMO, CLO
- **Nivel 1 — Direccion (6):** PM, Engineering Director, Product Director, Marketing Director, Compliance Director, Security Director
- **Nivel 2 — Leads (6):** Backend, Frontend, DevOps, QA, Data, UX
- **Nivel 3 — Especialistas (16):** API Designer, DB Architect, Integration Specialist, UI Developer, Performance Engineer, Security Engineer, SEO Specialist, Social Media, Copywriter, Email Marketing, Pricing Strategist, Community Manager, Privacy Officer, Compliance Analyst, CI/CD Engineer, Monitoring Engineer

### 10 Skills reutilizables
commit-devlog, conventions, design-review, fix-bug, generate-tests, optimize-repo, perf-check, security-scan, skill-creator, skill-installer

### Capa de coordinacion
- `cross_decisions.md` — registro de decisiones multi-dominio
- Pre-flight check al abrir bloque
- Post-validation al cerrar bloque

## Como usar

Ver `SETUP.md` para instalacion y configuracion de proyectos nuevos.

## Invocacion de agentes

```
/agents/nivel-0/ceo           — Decision estrategica
/agents/nivel-1/pm            — Coordinacion de bloques
/agents/nivel-2/backend-lead  — Trabajo backend
/agents/nivel-3/api-designer  — Diseno de API
```

## Escalado

```
Especialista → Lead → Director → C-Suite → Usuario (fundador)
```
