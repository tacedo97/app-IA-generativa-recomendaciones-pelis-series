import os
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException, Form
import cohere  #LLLM used for the development of the application
from langchain_cohere import ChatCohere
from langchain_core.prompts import ChatPromptTemplate
import pymysql
import markdown

#We load the environment variables from the .env file.
load_dotenv()
trial_api_key = os.getenv("COHERE_TRIAL_API_KEY") #Free API key of Cohere llm
aws_password = os.getenv("DB_PASSWORD") #AWS database password

def popcornai_recommendation(user_input:str):
    '''
    Function which returns a recommendation of a series or a film depending on the
    details described in the 'user_input'. This function is based on the Cohere LLM
    '''
    #We define the Cohere llm
    llm = ChatCohere(cohere_api_key=trial_api_key, max_tokens=100)

    #We create the prompt template
    template = ChatPromptTemplate([
        ("system", '''You are an expert of series and films of all times (both old and new) name PopCornAI, who recommends series or films
         to users based on what they tell you they want to watch. You are helpful, inclusive, nice, educated and polite. If users don't indicate you key words as "films", "series" or similars, 
         you will tell them that you need more information in the query to give them an appropiate recommedation.'''),
        ("ai", "Hello, I'm PopcornAI and I'm here to recommend you a film or a serie based on what you introduce below:)"),
        ("human", user_input),
    ])
    try:
        if len(user_input.strip()) != 0:
            #We generate the prompt with the user input, passing it to the previously defined template.
            prompt_value = template.invoke({"user_input":user_input})

            #The prompt is sent to the model
            response = llm.invoke(prompt_value)

            return response.content
        else:
            return "Empty query. Please, include some details in order to be able to recommend you a movie/series based on these details"
        
    except HTTPException as e:
        return

def aws_instance_connection():
    '''
    Function we use to connect to the AWS instance
    '''
    popcornai_instance = pymysql.connect(host = "popcornai.crkoiw80araw.eu-west-1.rds.amazonaws.com",
                                        user = "admin",
                                        password = aws_password,
                                        charset="utf8mb4",
                                        cursorclass = pymysql.cursors.DictCursor
                                        )
    return popcornai_instance

def insert_query_recommendation(user_query, query_timestamp, recommendation, recommendation_timestamp, answer_time, ip_adress):
    '''
    Function which insert all the information related to the users queries and the
    correspondant recommendations of the LLM that we want to save in our cloud database
    '''
    popcornai_instance = aws_instance_connection() #Instance connection
    try:
        cursor = popcornai_instance.cursor()
        cursor.execute('''USE popcornai_db''')
        insert_data = '''
                        INSERT INTO user_query_recommendation (user_query, query_timestamp, recommendation, recommendation_timestamp, answer_time, ip_adress)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    '''
        cursor.execute(insert_data, (user_query, query_timestamp, recommendation, recommendation_timestamp, answer_time, ip_adress))
        popcornai_instance.commit()
    finally:
        popcornai_instance.close() #We close MySQL connection