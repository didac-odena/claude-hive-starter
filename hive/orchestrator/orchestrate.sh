#!/usr/bin/env bash
# Hive Orchestrator — Kadid genera plan y lo ejecuta
#
# Uso:
#   ./orchestrate.sh "Bloque 6 — Frontend"           → Kadid genera plan, pide OK, ejecuta
#   ./orchestrate.sh --plan plan.md                   → Ejecuta plan existente directamente
#   ./orchestrate.sh --gen-only "Bloque 6 — Frontend" → Solo genera plan sin ejecutar

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PLAN_EXECUTOR="$SCRIPT_DIR/orchestrate-plan.sh"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"

# Modo 1: ejecutar plan existente
if [[ "${1:-}" == "--plan" ]]; then
    exec "$PLAN_EXECUTOR" "${2:?Falta archivo de plan}"
fi

# Modo 2: solo generar plan
GEN_ONLY=false
if [[ "${1:-}" == "--gen-only" ]]; then
    GEN_ONLY=true
    shift
fi

BLOQUE="${1:?Uso: ./orchestrate.sh \"Bloque N — Nombre\"}"
PLAN_FILE="plan-${TIMESTAMP}.md"

echo "=== HIVE ORCHESTRATOR ==="
echo "Bloque: $BLOQUE"
echo ""
echo "--- Kadid generando plan ---"

PLAN_PROMPT="Eres Kadid, fundador del Sistema Hive.
Lee tu perfil en ~/.claude/hive/kadid-profile.md
Lee tu archivo de agente en ~/.claude/commands/agents/estrategia/kadid.md

El usuario quiere trabajar en: $BLOQUE

Genera un plan de ejecucion:

1. Ejecuta pre-flight: lee ROADMAP, cross_decisions, context file del dominio
2. Decide que agentes necesitas (minimo posible)
3. Define las tareas en orden, con el agente responsable de cada una
4. Incluye una tarea de revision por un agente diferente al ejecutor

FORMATO DE SALIDA (exacto, sin markdown extra, una tarea por linea):
TAREA | RUTA_AGENTE | PROMPT_PARA_EL_AGENTE

Ejemplo:
Pre-flight | direccion/pm | Ejecuta pre-flight del Bloque 6 Frontend del proyecto
Specs UI | direccion/product-director | Define user flows del dashboard
Componentes | ejecucion/frontend-lead | Propone arquitectura de componentes React
Revision | direccion/engineering-director | Revisa calidad y testing de la propuesta

Solo las lineas de tareas, nada mas. Sin encabezados, sin explicaciones."

claude --print "$PLAN_PROMPT" > "$PLAN_FILE" 2>&1

echo ""
echo "=== PLAN GENERADO ==="
cat "$PLAN_FILE"
echo ""

if $GEN_ONLY; then
    echo "Plan guardado en: $PLAN_FILE"
    echo "Para ejecutar: ./orchestrate.sh --plan $PLAN_FILE"
    exit 0
fi

echo "¿Ejecutar este plan? (s/N)"
read -r CONFIRM
if [[ "$CONFIRM" != "s" && "$CONFIRM" != "S" ]]; then
    echo "Plan guardado en: $PLAN_FILE — puedes editarlo y ejecutar con: ./orchestrate.sh --plan $PLAN_FILE"
    exit 0
fi

exec "$PLAN_EXECUTOR" "$PLAN_FILE"
