# Bienvenido a Claude-Hive 🐝

Esto convierte a Claude Code en un **equipo** en lugar de un asistente suelto. En vez de un solo modelo genérico improvisando, tienes 13 roles especializados, un orquestador que protege las decisiones importantes, y un flujo de trabajo que evita dejar cosas a medias.

Si vienes de usar Claude Code "a pelo", esto te va a cambiar la forma de trabajar en proyectos serios.

---

## Por qué usarlo (beneficios)

- **13 agentes especializados, no un todoterreno.** Backend, frontend, devops, producto, legal/marketing, finanzas, QA… Cada agente lee **solo el contexto de su dominio**, así que sus respuestas son más enfocadas y no se diluyen. Invocas al que toca y habla como ese rol.
- **Un workflow que cierra bien.** El trabajo serio se organiza en **bloques**: antes de empezar hay un *pre-flight* (comprueba dependencias y que no choques con otra sesión), y al terminar un *cierre* con registro en el DEVLOG. Menos "empecé y lo dejé a medias".
- **Kadid, el guardián.** Hay un agente orquestador (Kadid) que protege tus documentos **FUNDAMENTALS** — si una decisión los contradice, la bloquea y te avisa. También decide qué agente lidera cada cosa.
- **Anti-deuda técnica por diseño.** Reglas duras que el sistema respeta: nunca tocar un test para que pase, nunca hardcodear para aprobar validaciones, no dejar findings "a medias". La calidad va por delante de la velocidad.
- **Memoria entre sesiones.** `MEMORY.md` (índice) + `project_docs/context/*` hacen que el proyecto "recuerde" decisiones y estado de una sesión a la siguiente.
- **Ahorro de tokens (RTK).** Un hook comprime ciertos comandos pesados (git diff/log, listados…) antes de que entren al contexto. Si no instalas `rtk`, no pasa nada: deja pasar el comando tal cual.
- **Trabajo en paralelo (Hive Bridge).** Puedes tener varias terminales de Claude abiertas a la vez y que **se manden mensajes** entre ellas sin copiar/pegar.
- **Skills listas.** Comandos como `/commit-devlog`, `/fix-bug`, `/generate-tests`, `/security-scan`, `/perf-check` — atajos a tareas comunes hechas con criterio.

---

## Los conceptos en 1 minuto

| Concepto | Qué es |
|---|---|
| **Agente** | Un rol con criterio propio. Se invoca con `/<nombre>` (ej. `/backend-lead`, `/kadid`). |
| **Niveles** | Estrategia (visión) → Dirección (coordina) → Ejecución (pica). Escalas hacia arriba si te falta autoridad. |
| **Bloque** | Una unidad de trabajo con principio y fin. Lo abres diciendo *"Bloque N — nombre"*. |
| **FUNDAMENTALS.md** | Tus documentos inviolables. Kadid no deja que nada los contradiga. |
| **cross_decisions.md** | Donde se registran las decisiones que afectan a varios dominios. |
| **Hooks** | Automatismos: RTK (tokens), routing-check (avisa si editas fuera de dominio), hive-remind (te recuerda commits). |

---

## Cómo usarlo bien

1. **Define tus FUNDAMENTALS al empezar.** En un proyecto nuevo, ejecuta `/init-project-workflow` y rellena `project_docs/FUNDAMENTALS.md` con lo que es sagrado (el PRD, el whitepaper, invariantes de negocio…). Sin eso, Kadid no puede hacer de guardián.

2. **Habla en bloques para trabajo serio.** En vez de "hazme el login", di *"Bloque 1 — autenticación con JWT y refresh tokens"*. El sistema hace pre-flight, planifica y cierra con DEVLOG. Para tareas sueltas de 2 minutos no hace falta.

3. **Invoca al agente del dominio.** ¿UI? `/frontend-lead`. ¿Endpoint o schema? `/backend-lead`. ¿Decisión de producto o pricing? `/cpo` o `/finance-director`. ¿No sabes por dónde empezar el día? `/secre` te da un briefing.

4. **Deja que Kadid orqueste lo grande.** Para decisiones que cruzan dominios o tocan FUNDAMENTALS, invoca `/kadid` y que coordine. Su trabajo es bloquear lo que rompe coherencia y elegir quién hace qué.

5. **Usa las skills en vez de pedirlo a mano.** `/commit-devlog` para commitear con entrada de DEVLOG; `/fix-bug` para depurar con método; `/security-scan` antes de exponer algo. Salen mejor que improvisando.

6. **Multi-terminal con el Bridge (opcional).** Si trabajas en dos cosas a la vez, arranca cada terminal con `export HIVE_ALIAS=backend-1` (o el nombre que quieras) antes de `claude`, y usa `/hive-send`, `/hive-inbox`, `/hive-list` para coordinarlas.

---

## Primeros 5 minutos (tras instalar)

```text
1. Reinicia Claude Code (para que cargue CLAUDE.md, hooks y status line).
2. En tu proyecto:  /init-project-workflow
   → crea project_docs/ con FUNDAMENTALS, MEMORY, ROADMAP, cross_decisions…
3. Edita project_docs/FUNDAMENTALS.md con tus documentos inviolables.
4. Di:  "secre"   → te da un briefing del estado y propone por dónde empezar.
5. Abre tu primer bloque:  "Bloque 1 — <lo que sea>".
```

---

## Filosofía

> **Calidad > velocidad, siempre.** Hacer rápido y mal cuesta más que hacer despacio y bien, porque obliga a volver.

El sistema está diseñado para que el trabajo quede **cerrado de verdad**, no "casi". Los pasos del workflow no son burocracia: son controles de calidad. Si alguno te estorba en una tarea trivial, sáltatelo — pero en lo serio, te ahorran volver.

Para el detalle de la metodología: `hive/README.md`, `hive/docs/ARCHITECTURE.md` y `hive/docs/AGENTS.md`.

Disfrútalo. 🐝
