from sqlalchemy import MetaData, Table, Column, Integer, String, Float, Boolean, DateTime, Sequence, ForeignKey
from sqlalchemy import create_engine
from snowflake.sqlalchemy import URL
import os
from dotenv import load_dotenv
import pandas as pd

# Load environment variables
load_dotenv()

# Create a Snowflake engine
engine = create_engine(URL(
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    role=os.getenv("SNOWFLAKE_ROLE"),
))

# Connect to the engine
connection = engine.connect()

# Create metadata object
metadata = MetaData()

# Define the Product table
product_table = Table('Product', metadata,
    Column('ProductID', String, primary_key=True),
    Column('ProductName', String),
    Column('AboutProduct', String),
    Column('ProductRating', Float),
    Column('Price', String)
)

# Define the User table
user_table = Table('User', metadata,
    Column('UserID', String, primary_key=True),
    Column('UserName', String),
    Column('UserEmail', String)
)

# Define the Review table
review_table = Table('Review', metadata,
    Column('ReviewID', String, primary_key=True),
    Column('UserID', String, ForeignKey('User.UserID')),
    Column('ProductID', String, ForeignKey('Product.ProductID')),
    Column('ReviewText', String),
    Column('Rating', Float)
)

# Create all tables
metadata.create_all(engine)

# Function to insert data into the table
def insert_data(df, table):
    df.to_sql(table.name, con=engine, index=False, if_exists='append')

# Load the prepared CSV files
product_data = pd.read_csv('final_product_data.csv')
user_data = pd.read_csv('final_user_data.csv')
review_data = pd.read_csv('final_review_data.csv')

# Insert data into the tables
insert_data(product_data, product_table)
insert_data(user_data, user_table)
insert_data(review_data, review_table)
