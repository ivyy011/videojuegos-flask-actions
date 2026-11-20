
import os
import pymysql

def obtener_conexion():
    return pymysql.connect(
        host='localhost',
        user='root',
        password=os.environ["MYSQL_PASSWORD"],
        db='juegos'
    )
