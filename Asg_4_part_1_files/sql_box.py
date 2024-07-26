import streamlit as st
from database import run_query

def sql_box():
    st.title("Assg-4 : Part 1.0 : Basic SQL Alchemy Snowflake Query Box")
    st.write("Enter a SQL query and run it against the Snowflake database")

    text_ar = st.text_area("Enter SQL Query", "SELECT SS_ADDR_SK FROM SNOWFLAKE_SAMPLE_DATA.TPCDS_SF10TCL.STORE_SALES LIMIT 10;")
    if st.button("Run Query"):
        try:
            result_df = run_query(text_ar)
            st.write(result_df)
        except Exception as e:
            st.write("Error: " + str(e))
