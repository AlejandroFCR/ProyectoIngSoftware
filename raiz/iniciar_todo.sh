#!/bin/bash

# Definimos colores para que se vea profesional
VERDE='\033[0;32m'
AZUL='\033[0;34m'
ROJO='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${AZUL}=========================================${NC}"
echo -e "${AZUL}   INICIANDO SISTEMA BACKEND IOT v0.2a    ${NC}"
echo -e "${AZUL}=========================================${NC}"

# 1. LIMPIEZA PREVENTIVA
# Intentamos cerrar instancias anteriores para evitar errores de "Puerto ocupado"
echo -e "${ROJO}[!] Deteniendo procesos antiguos...${NC}"
pkill -f "procesador_iot.py"
pkill -f "api_server.py"
# Esperamos un segundo para asegurar que se cerraron
sleep 1

# 2. INICIAR API REST (Usuarios/Login)
echo -e "${VERDE}[+] Iniciando API REST (FastAPI)...${NC}"
# nohup: evita que se cierre si te desconectas
# python3 -u: modo "unbuffered" para ver logs al instante
nohup ./../../bin/python3 -u api_server.py > logs_api.txt 2>&1 &
PID_API=$!
echo "    -> API corriendo con PID: $PID_API"
echo "    -> Logs disponibles en: logs_api.txt"

# 3. INICIAR PROCESADOR DE SENSORES (MQTT -> DB)
echo -e "${VERDE}[+] Iniciando Procesador de Sensores...${NC}"
nohup ./run_server.sh > logs_procesador.txt 2>&1 &
PID_PROC=$!
echo "    -> Procesador corriendo con PID: $PID_PROC"
echo "    -> Logs disponibles en: logs_procesador.txt"

# 4. RESUMEN
echo -e "${AZUL}=========================================${NC}"
echo -e "${VERDE}¡SISTEMA EN LÍNEA!${NC}"
echo -e "La API está escuchando en el puerto 8000."
echo -e "El procesador está vigilando la carpeta de archivos."
echo -e "${AZUL}=========================================${NC}"
echo -e "Para detener todo, ejecuta: ./detener_todo.sh"