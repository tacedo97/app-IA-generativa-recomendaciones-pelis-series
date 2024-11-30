import os
from dotenv import load_dotenv
import cohere #LLM empleado para el desarrollo de la aplicación
from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate
import pymysql

#Cargamos las variables de entorno del archivo .env
load_dotenv()
trial_api_key = os.getenv("COHERE_TRIAL_API_KEY") #API key del llm de Cohere gratuita
aws_password = os.getenv("DB_PASSWORD") #Contraseña de la db de AWS

def popcornai_recommendation(user_input:str):
    #Definimos el llm de Cohere
    llm = ChatCohere(cohere_api_key=trial_api_key, max_tokens=100)

    #Creamos la plantilla del prompt
    template = ChatPromptTemplate([
        ("system", "You are an expert of series and films of all times (both old and new) name PopCornAI, who recommends series or films to users based on what they tell you they want to watch. You are helpful, inclusive, nice, educated and polite"),
        ("ai", "Hello, I'm PopcornAI and I'm here to recommend you a film or a serie based on what you introduce below:)"),
        ("human", user_input),
    ])

    #Generamos el prompt con el input del usuario, pasándolo a al template definido previamente
    prompt_value = template.invoke({"user_input":user_input})

    #Pasamos al modelo el prompt
    response = llm.invoke(prompt_value)

    return response.content

def aws_instance_connection():
    #Nos conectamos a la instancia de AWS
    popcornai_instance = pymysql.connect(host = "popcornai.crkoiw80araw.eu-west-1.rds.amazonaws.com",
                                        user = "admin",
                                        password = aws_password,
                                        cursorclass = pymysql.cursors.DictCursor
                                        )
    return popcornai_instance    