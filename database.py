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
