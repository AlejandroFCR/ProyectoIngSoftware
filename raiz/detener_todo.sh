#!/bin/bash

ROJO='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${ROJO}=========================================${NC}"
echo -e "${ROJO}  DETENIENDO SISTEMA BACKEND IOT v0.2a   ${NC}"
echo -e "${ROJO}=========================================${NC}"

# Matar Python de la API
if pkill -f "api_server.py"; then
    echo "✅ API REST detenida."
else
    echo "⚠️  La API no estaba corriendo."
fi

# Matar el script de Bash del procesador
if pkill -f "run_server.sh"; then
    echo "✅ Script Monitor (run_server) detenido."
else
    echo "⚠️  El monitor no estaba corriendo."
fi

# Matar el Python del procesador (por si acaso quedó colgado)
if pkill -f "procesador_iot.py"; then
    echo "✅ Procesador Python detenido."
fi

echo "--- Todo apagado correctamente ---"