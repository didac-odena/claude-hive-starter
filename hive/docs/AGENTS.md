# Catalogo de Agentes — Sistema Hive

13 agentes organizados en 3 niveles. Invocacion: `/agents/[nivel]/[nombre]`

---

## Estrategia (3 agentes)

Vision, direccion y decisiones de alto nivel.

| Agente | Comando | Responsabilidad | Escala a |
|--------|---------|-----------------|----------|
| Kadid (Fundador) | `/agents/estrategia/kadid` | Guardian de FUNDAMENTALS, orquestador, decisiones de direccion | Usuario |
| CTO | `/agents/estrategia/cto` | Arquitectura, stack, seguridad global, deuda tecnica | Kadid |
| CPO | `/agents/estrategia/cpo` | Producto, pricing, modelo de negocio, compliance de producto | Kadid |

---

## Direccion (6 agentes)

Gestion y coordinacion. Traducen estrategia en planes ejecutables.

| Agente | Comando | Responsabilidad | Escala a |
|--------|---------|-----------------|----------|
| PM | `/agents/direccion/pm` | Coordinacion de bloques, pre-flight, post-validation | Kadid |
| Dir. Ingenieria | `/agents/direccion/engineering-director` | Calidad codigo, testing, datos, procesos dev | CTO |
| Dir. Producto | `/agents/direccion/product-director` | Specs, UX, flujos, criterios de aceptacion | CPO |
| Marketing & Legal | `/agents/direccion/marketing-legal` | Marketing, legal, compliance, contenido | Kadid / CPO |
| Finance Director | `/agents/direccion/finance-director` | Modelo economico, costes, pricing, presupuesto | Kadid |
| Secre | `/agents/direccion/secre` | Briefing organizativo, estado del proyecto, agenda | Kadid |

---

## Ejecucion (4 agentes)

Ejecucion tecnica y de contenido.

| Agente | Comando | Responsabilidad | Escala a |
|--------|---------|-----------------|----------|
| Backend Lead | `/agents/ejecucion/backend-lead` | API, DB, integraciones, seguridad aplicativa, performance | Dir. Ingenieria |
| Frontend Lead | `/agents/ejecucion/frontend-lead` | UI, design system, accesibilidad, SEO tecnico | Dir. Ingenieria |
| DevOps Lead | `/agents/ejecucion/devops-lead` | CI/CD, hosting, containers, monitoring | Dir. Ingenieria |
| Content Lead | `/agents/ejecucion/content-lead` | Copy, RRSS, email, comunidad | Marketing & Legal |

---

## Cuando usar cada nivel

| Necesidad | Nivel | Ejemplo |
|-----------|-------|---------|
| Definir direccion, resolver conflictos, verificar FUNDAMENTALS | Estrategia | "Priorizamos seguridad o velocidad?" |
| Planificar un bloque, coordinar equipos, definir specs | Direccion | "Pre-flight del Bloque 15" |
| Ejecutar tarea concreta | Ejecucion | "Crear endpoint REST para /api/users" |

## Protocolo de escalado

```
Ejecucion → Direccion → Estrategia → Owner del proyecto
```

1. Intentar resolver en el nivel actual
2. Si excede dominio o autoridad → escalar al superior
3. Si afecta a 2+ dominios → registrar en cross_decisions.md + escalar
4. Kadid resuelve o escala al owner si es irreversible / implica dinero

## Documentos fundamentales

Cada proyecto define en `project_docs/FUNDAMENTALS.md` que documentos son inviolables. Kadid verifica automaticamente que ninguna decision los contradiga.

## Regla de edicion

Agentes en paralelo SOLO para analisis y planificacion. Para editar archivos → ejecucion secuencial o directa. Las ediciones en paralelo no son fiables.
