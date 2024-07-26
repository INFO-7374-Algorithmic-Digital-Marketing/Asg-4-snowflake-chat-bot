from sqlalchemy import create_engine, text
import pandas as pd
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

engine = create_engine(
    'snowflake://{user}:{password}@{account}/'.format(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
    )
)

def run_query(query):
    try:
        # with st.spinner("Running query..."):
        connection = engine.connect()
        print("Connection successful")
        connection.execute(text("USE SNOWFLAKE_SAMPLE_DATA.TPCDS_SF10TCL;")) # Do we need this? DB is passed as connection parameter
        # Make parameterized query such that no DELETE / UPDATE queries can be run
        query = text(query)
        result = connection.execute(query).fetchall()
        try:
            result = pd.DataFrame(result)
        except Exception as e:
            print(e)            
        finally:
            return result
    except Exception as e:
        return str(e)
    finally:
        connection.close()


#############################################Query Template Functions####################################################
import random
def load_template(template_path):
    with open(template_path, 'r') as file:
        template = file.read()
    return template

# # Function to generate and run the query with provided parameters
# def generate_and_run_query1(year=2000, agg_field="SR_RETURN_AMT", state="TN", limit=10):
#     query_template = load_template('query_templates/query1.tpl')
#     # Load the query template
#     query_template = load_template('query_templates/query1.tpl')
    
#     # Prepare the query by replacing placeholders
#     query = query_template.format(agg_field=agg_field, year=year, state=state, limit=limit)

#     # Run the query
#     # results = run_query(query)
#     return query

# def generate_and_run_query2(year=2001):
#     # Load the query template
#     query_template = load_template('query_templates/query2.tpl')
    
#     # Prepare the query by replacing placeholders
#     query = query_template.format(year=year)

#     # Run the query
#     # results = run_query(query)
#     return query

# # Function to generate and run the query with provided parameters
# def generate_and_run_query3(aggc="ss_ext_sales_price", month="11", manufact="128", limit=10):
#     # Load the query template
#     query_template = load_template('query_templates/query3.tpl')
    
#     # Prepare the query by replacing placeholders
#     query = query_template.format(aggc=aggc, month=month, manufact=manufact, limit=limit)

#     # Run the query
#     # results = run_query(query)
#     return query


def generate_and_run_query1(YEAR=2000, AGG_FIELD="SR_RETURN_AMT", STATE="TN", LIMIT=10):
    query_template = load_template('query_templates/query1.tpl')
    # Load the query template
    query_template = load_template('query_templates/query1.tpl')
    
    # Prepare the query by replacing placeholders
    query = query_template.format(agg_field=AGG_FIELD, year=YEAR, state=STATE, limit=LIMIT)

    # Run the query
    # results = run_query(query)
    return query

def generate_and_run_query2(YEAR=2001):
    # Load the query template
    query_template = load_template('query_templates/query2.tpl')
    
    # Prepare the query by replacing placeholders
    query = query_template.format(year=YEAR)

    # Run the query
    # results = run_query(query)
    return query

# Function to generate and run the query with provided parameters
def generate_and_run_query3(AGGC="ss_ext_sales_price", MONTH="11", MANUFACT="128", LIMIT=10):
    # Load the query template
    query_template = load_template('query_templates/query3.tpl')
    
    # Prepare the query by replacing placeholders
    query = query_template.format(aggc=AGGC, month=MONTH, manufact=MANUFACT, limit=LIMIT)

    # Run the query
    # results = run_query(query)
    return query