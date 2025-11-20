import json
import pymysql
import time
import os
import sys

# TODO: Modificar estos parámetros según la configuración de la base de datos o entorno de pruebas
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '123456789',
    'db': 'proyectVegtablePatch',
    'cursorclass': pymysql.cursors.DictCursor
}

FILE_INPUT = 'procesaCapturaDatos.txt'
FILE_BACKUP = 'datosRespaldo.txt'

def procesar_datos():
    #! Validación del archivo procesable
    if not os.path.exists(FILE_INPUT):
        print(f"No existe el archivo {FILE_INPUT}. Esperando ciclo...")
        return

    #! Conexión a la base de datos
    try:
        connection = pymysql.connect(**DB_CONFIG)
        print("Conexión a BD exitosa.")
    except Exception as e:
        print(f"Error conectando a la BD: {e}")
        return

    registros_procesados = 0

    try:
        with connection.cursor() as cursor:
            #? Lectura del archivo de entrada
            with open(FILE_INPUT, 'r') as f_in, open(FILE_BACKUP, 'a') as f_out:
                for linea in f_in:
                    linea = linea.strip()
                    if not linea: continue

                    try:
                        #! JSON Parsing
                        data = json.loads(linea)
                        
                        #! JSON Mapping (variables)
                        #TODO: Verificar nombres de campos JSON, MAC Address, etc.
                        mac_address = data.get('IdEsp32') #? MAC Address
                        val_ph = float(data.get('Ph', 0))
                        val_temp = float(data.get('Temperatura', 0))
                        val_humedad = float(data.get('Agua', 0)) #? Humedad del suelo
                        
                        #! Busqueda de ID y límites recomendados
                        #? Obtener MAC del sensor
                        sql_sensor = "SELECT idSensor, idPlanta FROM Sensor WHERE MAC = %s"
                        cursor.execute(sql_sensor, (mac_address,))
                        sensor_row = cursor.fetchone()

                        if not sensor_row:
                            print(f"ERROR: Sensor con MAC {mac_address} no registrado en DB. Saltando...")
                            continue
                        
                        id_sensor = sensor_row['idSensor']
                        id_planta = sensor_row['idPlanta']
                        
                        #? Obtener límites recomendados de la planta
                        sql_planta = """
                            SELECT phInitRecomendado, phFinRecomendado, 
                                temperaturaInitRecomendada, temperaturaFinRecomendada,
                                humedadInitRecomendada, humedadFinRecomendada
                            FROM Planta WHERE idPlanta = %s
                        """
                        cursor.execute(sql_planta, (id_planta,))
                        planta_row = cursor.fetchone()

                        if not planta_row:
                            print(f"ERROR: Planta {id_planta} no encontrada. Saltando...")
                            continue

                        #! Insertar datos en Bitacora
                        timestamp_actual = time.time() 

                        sql_insert = """
                            INSERT INTO Bitacora (
                                idSensor, idPlanta, 
                                temperaturaTomada, humedadTomada, phTomado, 
                                fechaHoraCaptura,
                                limiteInitTemperatura, limiteFinTemperatura,
                                limiteInitPh, limiteFinPh,
                                limiteInitHumedad, limiteFinHumedad
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
                        
                        valores = (
                            id_sensor, id_planta,
                            val_temp, val_humedad, val_ph,
                            timestamp_actual,
                            planta_row['temperaturaInitRecomendada'], planta_row['temperaturaFinRecomendada'],
                            planta_row['phInitRecomendado'], planta_row['phFinRecomendado'],
                            planta_row['humedadInitRecomendada'], planta_row['humedadFinRecomendada']
                        )
                        
                        cursor.execute(sql_insert, valores)
                        
                        #! Respaldar si todo salió bien
                        f_out.write(linea + "\n")
                        registros_procesados += 1

                    except json.JSONDecodeError:
                        print(f"Error de formato JSON en linea: {linea}")
                    except Exception as e_proc:
                        print(f"Error procesando linea: {e_proc}")

            #! Commit de todos los inserts
            connection.commit()
            
            #! Limpiar el archivo de entrada (vaciamos procesaCapturaDatos.txt)
            open(FILE_INPUT, 'w').close()
            
            print(f"Ciclo completado. Registros insertados: {registros_procesados}")

    finally:
        connection.close()

if __name__ == "__main__":
    procesar_datos()