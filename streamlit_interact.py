import streamlit as st
# from database import run_query
import database

def interact_streamlit():
    st.title("Assg-4 : Part 1.1 : Interactive Streamlit Page")
    st.write("Using Streamlit to dynamically change values and run queries")

    # User input for query selection
    query_options = [
        "Query1", 
        "Query2",
        "Query3"
    ]
    selected_query = st.selectbox("Select a query:", query_options)

    if selected_query == "Query1":
        agg_field = st.text_input("Enter Agg Field", "SR_RETURN_AMT")
        state = st.text_input("Enter State", "CA")
        year = st.text_input("Enter Year:", "2001")
        query_to_run = database.generate_and_run_query1(year, agg_field, state, 10)
    elif selected_query == "Query2":
        year = st.text_input("Enter Year:", "2001")
        query_to_run = database.generate_and_run_query2(year)
    elif selected_query == "Query3":
        aggc = st.text_input("Enter Agg Column", "ss_ext_sales_price")
        month = st.text_input("Enter Month (1-12):", "11")
        manufact = st.text_input("Enter Manufacturer ID:", "100")
        query_to_run = database.generate_and_run_query3(aggc, month, manufact)
    

    if st.button("Run Query"):
        result = database.run_query(query_to_run)
        st.write("Query Result:")
        st.write(result)
