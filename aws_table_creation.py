import pymysql
import os
from dotenv import load_dotenv
import utils

#We define the cursor object that will execute the queries after connecting to the AWS instance
cursor = utils.aws_instance_connection().cursor()

#Database creation
create_db = '''CREATE DATABASE IF NOT EXISTS popcornai_db'''
cursor.execute(create_db)

#Table creation
use_db = '''USE popcornai_db''' #Indicating the db in which we want to create the table
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

#Commit to save changes
utils.aws_instance_connection().commit()