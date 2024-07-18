from openai import OpenAI
import re
import streamlit as st
import pandas as pd
from database import run_query

def llm_chatbot():
    GEN_SQL = """
    You will be acting as an AI Snowflake SQL Expert named Jenny.
    Your goal is to give correct, executable sql query to users.
    You will be replying to users who will be confused if you don't respond in the character of Jenny.
    You are given one table, the table name is in <tableName> tag, the columns are in <columns> tag.
    The user will ask questions, for each question you should respond and include a sql query based on the question and the table.

    {context}

    Example Queries to refer : 
    Description: Total sales by manufacturer ID, month of year, and year
    SQL Query:        SELECT SUM(cs_ext_sales_price) AS total_sales
        FROM catalog_sales
        JOIN date_dim ON catalog_sales.cs_sold_date_sk = date_dim.d_date_sk
        JOIN item ON catalog_sales.cs_item_sk = item.i_item_sk
        WHERE d_year = year
        AND i_manufact_id = manufact_id
        AND d_moy = moy;


    Here are 6 critical rules for the interaction you must abide:
    <rules>
    1. You MUST wrap the generated sql code within ``` sql code markdown in this format e.g
    ```sql
    (select 1) union (select 2)
    ```
    2. If I don't tell you to find a limited set of results in the sql query or question, you MUST limit the number of responses to 10.
    3. Text / string where clauses must be fuzzy match e.g ilike %keyword%
    4. Make sure to generate a single snowflake sql code, not multiple.
    5. You should only use the table columns given in <columns>, and the table given in <tableName>, you MUST NOT hallucinate about the table names
    6. DO NOT put numerical at the very front of sql variable.
    </rules>

    Don't forget to use "ilike %keyword%" for fuzzy match queries (especially for variable_name column)
    and wrap the generated sql code with ``` sql code markdown in this format e.g:
    ```sql
    (select 1) union (select 2)
    ```

    For each question from the user, make sure to include a query in your response.

    Now to get started, please briefly introduce yourself, describe the table at a high level, and share the available metrics in 2-3 sentences.
    Then provide 3 example questions using bullet points.
    """

    @st.cache_data(show_spinner="Loading context...")
    def get_table_context(table_name: str):
        table = table_name.split(".")
        conn = st.connection("snowflake")
        columns = conn.query(f"""
            SELECT COLUMN_NAME, DATA_TYPE FROM {table[0].upper()}.INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_SCHEMA = '{table[1].upper()}' AND TABLE_NAME = '{table[2].upper()}'
            """, show_spinner=False,
        )
        columns = "\n".join(
            [
                f"- **{columns['COLUMN_NAME'][i]}**: {columns['DATA_TYPE'][i]}"
                for i in range(len(columns["COLUMN_NAME"]))
            ]
        )
        context = f"""
    Here is the table name <tableName> {'.'.join(table)} </tableName>

    Here are the columns of the {'.'.join(table)}

    <columns>\n\n{columns}\n\n</columns>
        """
        return context

    def get_system_prompt(table_name):
        table_context = get_table_context(
            table_name=table_name
        )
        return GEN_SQL.format(context=table_context)

    st.title("Snowflake Chat Bot")

    # Initialize the chat messages history
    client = OpenAI(api_key=st.secrets.OPENAI_API_KEY)
    if "messages" not in st.session_state:
        # system prompt includes table information, rules, and prompts the LLM to produce
        # a welcome message to the user.
        st.session_state.messages = [{"role": "system", "content": get_system_prompt("SNOWFLAKE_SAMPLE_DATA.TPCDS_SF10TCL.CATALOG_SALES")}]

    # Prompt for user input and save
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})

    # display the existing chat messages
    for message in st.session_state.messages:
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.write(message["content"])
            if "results" in message:
                st.dataframe(message["results"])

    # If last message is not from assistant, we need to generate a new response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            response = ""
            resp_container = st.empty()
            for delta in client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                stream=True,
            ):
                response += (delta.choices[0].delta.content or "")
                resp_container.markdown(response)

            message = {"role": "assistant", "content": response}
            # Parse the response for a SQL query and execute if available
            sql_match = re.search(r"```sql\n(.*)\n```", response, re.DOTALL)
            if sql_match:
                sql = sql_match.group(1)
                message["results"] = run_query(sql)
                st.dataframe(message["results"])
            st.session_state.messages.append(message)


# Example Queries 
# Give me the Total sales for manufacturer ID 107 in the month of November in the year 2000

