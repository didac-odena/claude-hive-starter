# Setup — Claude-Hive

Instrucciones para instalar el sistema Hive en una maquina nueva o proyecto nuevo.
Claude Code puede leer este archivo y ejecutar los pasos automaticamente.

---

## Instalacion en maquina nueva

El repo Claude-Hive ES `~/.claude/`. Para instalarlo en otra maquina:

```bash
git clone https://github.com/didac-odena/Claude-Hive.git ~/.claude
```

Tras clonar, ya tienes los 11 agentes + 10 skills + CLAUDE.md disponibles.

Crear `settings.json` adaptado a la maquina (no esta en el repo si esta en .gitignore).

---

## Configurar un proyecto nuevo

En el directorio raiz del proyecto:

### Paso 1: Crear estructura

```bash
mkdir -p .claude/rules .claude/commands
mkdir -p project_docs/context
```

### Paso 2: Copiar templates

```bash
cp ~/.claude/hive/templates/cross-decisions-template.md project_docs/cross_decisions.md
cp ~/.claude/hive/templates/WORKFLOW-template.md .claude/rules/workflow.md
cp ~/.claude/hive/templates/FUNDAMENTALS-template.md project_docs/FUNDAMENTALS.md
```

### Paso 3: Crear context files por dominio

```bash
for domain in backend frontend infrastructure product marketing legal branding; do
  cp ~/.claude/hive/templates/context-domain-template.md project_docs/context/$domain.md
done
```

### Paso 4: Configurar FUNDAMENTALS.md

Editar `project_docs/FUNDAMENTALS.md`:
- Listar documentos inviolables del proyecto
- Definir invariantes
- Este paso es CRITICO — sin FUNDAMENTALS, Kadid no puede actuar como guardian

### Paso 5: Personalizar workflow

Editar `.claude/rules/workflow.md`:
- Adaptar mapa bloque → context file
- Ajustar triggers si es necesario

### Paso 6: Verificar

```bash
ls ~/.claude/commands/agents/estrategia/   # 3 (Kadid, CTO, CPO)
ls ~/.claude/commands/agents/direccion/    # 4 (PM, Eng Dir, Product Dir, M&L)
ls ~/.claude/commands/agents/ejecucion/    # 4 (Backend, Frontend, DevOps, Content)

ls project_docs/context/
cat project_docs/FUNDAMENTALS.md | head -5
cat project_docs/cross_decisions.md | head -5
```

---

## Actualizaciones

```bash
cd ~/.claude
git pull
```

Los archivos de proyecto (context files, cross_decisions, FUNDAMENTALS, MEMORY) no estan en este repo — son especificos de cada proyecto.
