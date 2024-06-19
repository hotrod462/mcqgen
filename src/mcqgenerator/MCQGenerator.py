import os
import json
import pandas as pd
import traceback
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from src.mcqgenerator.logger import logging
from src.mcqgenerator.utils import read_file, get_table_data


from operator import itemgetter

import langchain
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import JsonOutputParser



#Load env variables
load_dotenv()

chat_model = ChatGroq(
    temperature=0.2,
    model="mixtral-8x7b-32768",
     api_key=os.getenv("GROQ_API_KEY") # Optional if not set as an environment variable
)
gen_template="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like the json format given below  and use it as a guide.
Ensure to make {number} MCQs

{response_json}

The json keys and values MUST be in double quotes(""). Ensure once again that the json keys and values are encased in double quotes("")

"""



quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "subject", "tone", "response_json"],
    template=gen_template
    )

quiz_chain= quiz_generation_prompt | chat_model
