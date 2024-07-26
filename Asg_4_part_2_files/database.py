from sqlalchemy import create_engine, text
import pandas as pd
import os
from dotenv import load_dotenv
import logging

# Load environment variables from a .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Retrieve Snowflake credentials from environment variables
user = os.getenv("MY_SNOWFLAKE_USER")
password = os.getenv("MY_SNOWFLAKE_PASSWORD")
account = os.getenv("MY_SNOWFLAKE_ACCOUNT")

# Log the user, account, and password
logging.info(f"User: {user}, Account: {account}, Password: {password}")

# Create the Snowflake engine
engine = create_engine(
    f'snowflake://{user}:{password}@{account}/'
)

def run_query(query):
    connection = engine.connect()
    logging.info("Connected to Snowflake")
    
    try:
        connection.execute(text("USE ASG_4_P2.PUBLIC;"))
        logging.info("Switched to ASG_4_P2.PUBLIC")
        
        # Make parameterized query such that no DELETE / UPDATE queries can be run
        query = text(query)
        result = connection.execute(query).fetchall()
        
        try:
            result_df = pd.DataFrame(result)
            logging.info("Query executed successfully and results fetched")
            return result_df
        except Exception as e:
            logging.error(f"Error converting query results to DataFrame: {e}")
            return None
    except Exception as e:
        logging.error(f"Error executing query: {e}")
        return None
    finally:
        connection.close()
        logging.info("Connection closed")
