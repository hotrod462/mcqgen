import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st
from src.mcqgenerator.logger import logging
from src.mcqgenerator.MCQGenerator import quiz_chain

#Load json file to be used in prompt
with open("Z:\mcqgen\Response.json", 'r') as file:
    json_format_template= json.load(file)

#Create a title for the app
st.title("MCQ Creator w/ Langchain :) ")

#Create a form using st.form
with st.form("user_inputs"):
    #File upload
    uploaded_file = st.file_uploader("Upload a pdf or text file")

    #Input fields
    mcq_count= st.number_input("No of MCQs", min_value=3, max_value=50)

    #Subject
    subject = st.text_input("Insert Subject", max_chars=20)

    #Quiz Tone
    tone = st.text_input("Difficulty lvl of qns", max_chars=20, placeholder="Simple")

    #Add Button
    button = st.form_submit_button("Create MCQs")

    #Check if button is clicked and all fields have input

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading :)....."):
            try:
                text=read_file(uploaded_file)
                
                response= quiz_chain.invoke(
                    {
                        "text":text,
                        "number":mcq_count,
                        "subject":subject,
                        "tone":tone,
                        "response_json": json.dumps(json_format_template)

                    }
                )

            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("error :( ")

            else:
                if isinstance(response,dict):
                    #extract quiz data from response
                    quiz=response.content
                    if quiz is not None:
                        table_data= get_table_data(quiz)
                        if table_data is not None:
                            df= pd.DataFrame(table_data)
                            df.index += 1
                            st.table(df)

                        else:
                            st.error("Error in the table data")

                else:
                    st.write(response)                        
