#!/bin/bash

# Definir archivos
ARCHIVO_CAPTURA="capturaDatos.txt"
ARCHIVO_PROCESO="procesaCapturaDatos.txt"

echo "Iniciando servidor de procesamiento IoT..."

while true; do
    # 1. Verificar si capturaDatos.txt tiene contenido
    if [ -s $ARCHIVO_CAPTURA ]; then
        # 2. Mover atómicamente los datos para que Python los procese
        # Usamos 'cat' y luego vaciamos para evitar bloquear a Mosquitto mucho tiempo
        # O mejor: renombramos (mv) si el sistema lo permite, pero como mosquitto hace append,
        # lo más seguro es copiar y vaciar rápido.
        
        # Bloqueo simple: copiamos contenido a procesa y vaciamos captura
        cat $ARCHIVO_CAPTURA >> $ARCHIVO_PROCESO
        > $ARCHIVO_CAPTURA
        
        echo "[$(date)] Datos detectados. Ejecutando procesador..."
        
        # 3. Ejecutar el script de Python
        ./../../bin/python3 procesador_iot.py 
        
    else
        # Si no hay datos, solo esperamos
        echo "[$(date)] Esperando datos..."
    fi

    # Esperar 5 segundos como pide el requerimiento [cite: 26]
    sleep 5
done