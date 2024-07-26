from openai import OpenAI
import re
import streamlit as st
import pandas as pd
import database as db
import json

def llm_chatbot():
    st.title("SQL Chatbot")
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    json_file_path = "context.json"
    with open(json_file_path, "r") as f:
        query_data = str(json.load(f))

    # query_metadata = json_content.dumps()

    #Func to execurte the correct function
    def execute_query_func(query_number, params):
        if query_number == 'query1.tpl':
            return db.run_query(db.generate_and_run_query1(**params))
        elif query_number == 'query2.tpl':
            return db.run_query(db.generate_and_run_query2(**params))
        elif query_number == 'query3.tpl':
            return db.run_query(db.generate_and_run_query3(**params))
        elif query_number == 'query4.tpl':
            return db.run_query(db.generate_and_run_query4(**params))
        elif query_number == 'query7.tpl':
            return db.run_query(db.generate_and_run_query7(**params))
        else:
            raise ValueError(f"Invalid query number: {query_number}")
        

    prompt_init = f'''Hello You are a chatbot acting as an interface between datawarehoue and user. 
                    Accoring to following information to select query most similar to user prompt: {query_data}. 
                    If value of the query parameters is in the prompt then use that value in the output otherwise use the default value.
                    Return the query number and the value for query parameters in a json format. A sample output is as follows:''' + '''
                    {
                        "query_number": "query1.tpl",
                        "query_params": {
                            "YEAR": 2000,
                            "AGG_FIELD": "SR_RETURN_AMT",
                            "STATE": "TN",
                            "LIMIT": 10
                        }
                    }
                    '''

    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"
        

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": prompt_init}
        ]

    for message in st.session_state.messages:
        if message["role"] in ["user", "assistant"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            stream = client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )
            response = st.write_stream(stream)

        st.session_state.messages.append({"role": "assistant", "content": response})
        response = json.loads(response)
        query_number = response['query_number']
        query_params = response['query_params']
        print(query_params)
        st.write(execute_query_func(query_number, query_params))


# Example Queries 
# Give me the Total sales for manufacturer ID 107 in the month of November in the year 2000

