from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
import pymysql
from passlib.context import CryptContext
import uvicorn

app = FastAPI(title="Backend IoT App", description="API para Usuarios y Sensores")

#! Encriptación de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#! Configuración de BD (Usa la IP remota si corres esto en local, o 'localhost' si corre en el servidor)
DB_CONFIG = {
    'host': '187.225.114.52', #! 'localhost' si este script corre en el mismo servidor que la BD
    'user': 'root',           #? Crear usuarios con menos permisos para prod.
    'password': '123456789',   #? Contraseña del usuario de la BD
    'db': 'proyectVegtablePatch',
    'cursorclass': pymysql.cursors.DictCursor
}

#! MODELOS DE DATOS (Lo que Kotlin debe enviar)
class UsuarioRegistro(BaseModel):
    nombreUsuario: str
    correo: EmailStr
    password: str

class UsuarioLogin(BaseModel):
    correo: EmailStr
    password: str

#? FUNCIONES AUXILIARES
def get_db_connection():
    return pymysql.connect(**DB_CONFIG)

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

#? ENDPOINTS DEL API

@app.post("/registrar", status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: UsuarioRegistro):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            #! Verificar si ya existe el correo
            cursor.execute("SELECT idUsuario FROM Usuario WHERE correo = %s", (usuario.correo,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="El correo ya está registrado")

            #! Encriptar contraseña
            hashed_pw = hash_password(usuario.password)

            #! Insertar en la BD
            #? 1 por defecto, o 0 si requieren confirmar email (asunción de afirmación)
            sql = "INSERT INTO Usuario (nombreUsuario, correo, contrasena, validacion) VALUES (%s, %s, %s, 1)"
            cursor.execute(sql, (usuario.nombreUsuario, usuario.correo, hashed_pw))
            conn.commit()
            
            return {"mensaje": "Usuario creado exitosamente", "correo": usuario.correo}
    except pymysql.MySQLError as e:
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {e}")
    finally:
        conn.close()

@app.post("/login")
def login_usuario(credenciales: UsuarioLogin):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            #? Buscar usuario por correo
            sql = "SELECT idUsuario, nombreUsuario, contrasena FROM Usuario WHERE correo = %s"
            cursor.execute(sql, (credenciales.correo,))
            user_data = cursor.fetchone()

            if not user_data:
                raise HTTPException(status_code=401, detail="Credenciales incorrectas")

            #? Verificar contraseña
            if not verify_password(credenciales.password, user_data['contrasena']):
                raise HTTPException(status_code=401, detail="Credenciales incorrectas")

            #? Login exitoso -> Retornamos datos que la App necesite (ej. ID)
            return {
                "mensaje": "Login exitoso",
                "idUsuario": user_data['idUsuario'],
                "nombreUsuario": user_data['nombreUsuario']
            }
    finally:
        conn.close()

if __name__ == "__main__":
    #? host="0.0.0.0" permite que sea visible desde fuera (internet/red local)
    uvicorn.run(app, host="0.0.0.0", port=8000)