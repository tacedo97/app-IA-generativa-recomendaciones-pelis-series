from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates #Para renderizar la plantilla HTML
from pydantic import BaseModel
import uvicorn
from transformers import AutoTokenizer, AutoModelForCausalLM
import cohere #LLM empleado para el desarrollo de la aplicación
from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate
import utils
from datetime import datetime
import pymysql
import markdown

#Definimos la variable de la aplicación
app = FastAPI()

# Configuración de Jinja2 para templates
templates = Jinja2Templates(directory="templates")

#Endpoint inicial que describe el ejercicio
#@app.get('/')
#async def hello():
#    return '''Hola! Bienvenido a la API utilizada para el desarrollo del sistema de recomendación de películas y series'''

#Endpoint que recoge la consulta del usuario
#@app.post('/ask_recommendation')
#async def asking_recommendation(user_query:str):
#    try:
#        return {"response":f"Consulta del usuario: {user_query}"}
#    except Exception as e:
#        raise HTTPException(detail="Ha habido un fallo en el envío de la consulta a PopcornAI:" + str(e))

#Endpoint que devuelve la recomendación en base a la consulta del usuario
@app.get("/recommendation")
async def llm_recommendation(request:Request, user_query:str):
    try:
        query_timestamp = datetime.now().isoformat() #Variable en la que incluimos la fecha y hora a la que el usuario manda la consulta
        recommendation = utils.popcornai_recommendation(user_query) #Recomendación generada por el llm
        recommendation_timestamp = datetime.now().isoformat() #Variable en la que incluimos la fecha y hora a la que el llm manda la recomendación en base a la consulta
        answer_time = (datetime.fromisoformat(recommendation_timestamp) - datetime.fromisoformat(query_timestamp)).total_seconds() #Tiempo que tarda el llm (en segundos) en responder
        ip_adress = request.client.host
        utils.insert_query_recommendation(user_query, query_timestamp, recommendation, recommendation_timestamp, answer_time, ip_adress)
        return recommendation
    except Exception as e:
        query_timestamp = datetime.now().isoformat()
        recommendation = "Ha habido un fallo al generar la recomendación:" + str(e)
        recommendation_timestamp = datetime.now().isoformat()
        answer_time = (datetime.fromisoformat(recommendation_timestamp) - datetime.fromisoformat(query_timestamp)).total_seconds() #Tiempo que tarda el llm (en segundos) en responder
        ip_adress = request.client.host
        utils.insert_query_recommendation(user_query, query_timestamp, recommendation, recommendation_timestamp, answer_time, ip_adress)
        raise HTTPException(detail="Ha habido un fallo al generar la recomendación:" + str(e))

@app.get("/", response_class=HTMLResponse)
async def render_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/recommendation_ui", response_class=HTMLResponse)
async def get_recommendation(request: Request, user_query: str = Form(...)):
    try:
        query_timestamp = datetime.now().isoformat() #Variable en la que incluimos la fecha y hora a la que el usuario manda la consulta
        recommendation = utils.popcornai_recommendation(user_query) #Recomendación generada por el llm
        recommendation_timestamp = datetime.now().isoformat() #Variable en la que incluimos la fecha y hora a la que el llm manda la recomendación en base a la consulta
        answer_time = (datetime.fromisoformat(recommendation_timestamp) - datetime.fromisoformat(query_timestamp)).total_seconds() #Tiempo que tarda el llm (en segundos) en responder
        ip_adress = request.client.host
        utils.insert_query_recommendation(user_query, query_timestamp, recommendation, recommendation_timestamp, answer_time, ip_adress)
        #Renderizamos la respuesta en el HTML
        return templates.TemplateResponse(
            "index.html", 
            {"request": request, "recommendation": markdown.markdown(recommendation)} #Formateamos la recomendación para convertir los saltos de línea y los textos en negrita en etiquetas HTML
        )
    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "recommendation": f"Hubo un error: {str(e)}"}
        )

# Ejecutar la aplicación
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)


