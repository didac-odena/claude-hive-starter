#!/usr/bin/env bash
# Hive Orchestrator — Kadid lanza agentes secuencialmente via claude --print
#
# Uso:
#   ./orchestrate.sh <plan.md>
#
# El plan.md define las tareas y agentes. Kadid las ejecuta en orden,
# recoge outputs, y genera un informe final.

set -euo pipefail

PLAN_FILE="${1:?Uso: ./orchestrate.sh <plan.md>}"
OUTPUT_DIR="$(mktemp -d)"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
REPORT_FILE="hive-report-${TIMESTAMP}.md"

echo "=== HIVE ORCHESTRATOR ==="
echo "Plan: $PLAN_FILE"
echo "Output dir: $OUTPUT_DIR"
echo ""

# Leer tareas del plan (formato: TASK|AGENTE|PROMPT)
TASK_NUM=0
while IFS='|' read -r task agent prompt; do
    # Saltar lineas vacias y comentarios
    [[ -z "$task" || "$task" =~ ^# ]] && continue

    TASK_NUM=$((TASK_NUM + 1))
    task=$(echo "$task" | xargs)    # trim
    agent=$(echo "$agent" | xargs)
    prompt=$(echo "$prompt" | xargs)

    echo "--- Tarea $TASK_NUM: $task ---"
    echo "Agente: $agent"
    echo "Ejecutando..."

    # Construir prompt completo con contexto del agente
    FULL_PROMPT="Actua como el agente $agent del Sistema Hive. Lee tu archivo de agente en ~/.claude/commands/agents/$agent.md y sigue sus instrucciones.

Tarea: $prompt

REGLAS:
- Lee los archivos de contexto que tu agente requiere antes de actuar.
- Verifica contra project_docs/FUNDAMENTALS.md antes de tomar decisiones.
- NUNCA modifiques tests para que pasen. Arregla el codigo.
- NUNCA hardcodees valores para pasar validaciones.
- Output conciso y accionable."

    # Ejecutar agente y guardar output
    OUTPUT_FILE="$OUTPUT_DIR/task_${TASK_NUM}_$(echo "$agent" | tr '/' '_').md"

    if claude --print "$FULL_PROMPT" > "$OUTPUT_FILE" 2>&1; then
        echo "OK — Output guardado en $OUTPUT_FILE"
    else
        echo "ERROR — Agente fallo. Output parcial en $OUTPUT_FILE"
    fi

    echo ""
done < "$PLAN_FILE"

# Generar informe final
echo "=== Generando informe final ==="

REPORT_PROMPT="Eres Kadid, el fundador del Sistema Hive. Lee tu perfil en ~/.claude/hive/kadid-profile.md.

Acabo de ejecutar un plan con $TASK_NUM tareas. Los outputs de cada agente estan en estos archivos:
$(ls "$OUTPUT_DIR"/*.md 2>/dev/null | while read f; do echo "- $f"; done)

Lee cada output y genera un INFORME FINAL con:
1. Que se hizo (resumen por tarea)
2. Decisiones tomadas y justificacion
3. Problemas encontrados
4. Verificacion contra FUNDAMENTALS: OK o contradicciones
5. Siguiente paso recomendado

Formato limpio y conciso."

claude --print "$REPORT_PROMPT" > "$REPORT_FILE" 2>&1

echo ""
echo "=== INFORME FINAL ==="
cat "$REPORT_FILE"
echo ""
echo "Informe guardado en: $REPORT_FILE"
echo "Outputs individuales en: $OUTPUT_DIR/"
