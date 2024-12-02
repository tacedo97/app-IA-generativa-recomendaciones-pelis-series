from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates #To render the HTML template
from pydantic import BaseModel
import uvicorn
from transformers import AutoTokenizer, AutoModelForCausalLM
import cohere #LLLM used for the development of the application
from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate
import utils
from datetime import datetime
import pymysql
import markdown

#We define the app variable
app = FastAPI()

#Configuration of Jinja2 for templates
templates = Jinja2Templates(directory="templates")

#Endpoint for the initial visualization of index.html
@app.get("/", response_class=HTMLResponse)
async def render_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

#Endpoint in which the user obtains a series/film recommendation of the Cohere llm depending on the sent query
@app.post("/recommendation_ui", response_class=HTMLResponse)
async def get_recommendation(request: Request, user_query: str = Form(...)):
    query_timestamp = datetime.now().isoformat() #Date/Time in which the user sends the query
    ip_adress = request.client.host 
    try:
        recommendation = utils.popcornai_recommendation(user_query) #Recommendation of the llm
        recommendation_timestamp = datetime.now().isoformat() #Date/Time in which the llm sends the recommendation to the user
        answer_time = (datetime.fromisoformat(recommendation_timestamp) - datetime.fromisoformat(query_timestamp)).total_seconds() #Time taken by the llm (in seconds) to give a recommendation
        utils.insert_query_recommendation(user_query, query_timestamp, recommendation, recommendation_timestamp, answer_time, ip_adress) #Inserting the information in the cloud database
        #We render the response in index.html
        return templates.TemplateResponse(
            "index.html", 
            {"request": request, "user_query": user_query, "recommendation": markdown.markdown(recommendation)} 
            ) #We formatted the recommendation to convert line breaks and bold text into HTML tags
    except Exception as e:
        utils.insert_query_recommendation(user_query, query_timestamp, str(e), query_timestamp, 0, ip_adress) #Inserting the information in the cloud database
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "recommendation": f"An error has occurred: {str(e)}"}
        )