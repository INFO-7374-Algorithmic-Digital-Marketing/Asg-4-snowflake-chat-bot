from openai import OpenAI
import streamlit as st
import database as db
import json

st.title("Course Assistant")
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

json_file_path = "context.json"
with open(json_file_path, "r") as f:
    query_data = str(json.load(f))

# query_metadata = json_content.dumps()

def select_query_func(query_nuymber)

prompt_init = f'''Hello You are a chatbot acting as an interface between dataware house and user. 
                Accoring to the prompt use the following information to select query most similar to user prompt: {query_data}. 
                If value of the query parameters is given then use that value in the outpu otherwise use the default value.
                Return the query number and the value for query parameters in a json format.
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
    # st.write(response['query_number'], response['query_params'])