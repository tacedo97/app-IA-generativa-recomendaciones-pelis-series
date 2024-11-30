import pymysql
import os
from dotenv import load_dotenv
import utils

#Definimos el objeto cursor que ejecutará las queries, conectándonos previamente a la instancia de AWS
cursor = utils.aws_instance_connection().cursor()

#Creamos la base de datos
create_db = '''CREATE DATABASE IF NOT EXISTS popcornai_db'''
cursor.execute(create_db)

#Creamos la tabla que necesitamos en la base de datos
use_db = '''USE popcornai_db''' #Primero indicamos en qué db vamos a crear la tabla
cursor.execute(use_db)
create_table = '''
                CREATE TABLE IF NOT EXISTS user_query_recommendation (
                    id INT NOT NULL auto_increment,
                    user_query TEXT NOT NULL,
                    query_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    recommendation TEXT NOT NULL,
                    recommendation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    answer_time FLOAT,
                    ip_adress VARCHAR(255),
                    PRIMARY KEY (id)
                )
               '''
cursor.execute(create_table)

#Ejecutamos un commit para guardar todos los cambios
utils.aws_instance_connection().commit()