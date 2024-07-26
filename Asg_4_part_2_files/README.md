# Assignment-4-P2 Overview

This project is a product recommendation and review generation system that uses Snowflake, FastAPI, and OpenAI's API. The system allows users to get product recommendations based on their review history, generate high-level summary reviews of products, and summarize product features.

## Prerequisites
- Python 3.10
- Docker
- Snowflake account
- OpenAI API key
- GROQ API key (optional)

## Setup

Clone the repository:

```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

Create a .env file in the root directory of the project with the following environment variables:

```bash
OPENAI_API_KEY="your-openai-api-key"
GROQ_API_KEY="your-groq-api-key"
MY_SNOWFLAKE_ACCOUNT="your-snowflake-account"
MY_SNOWFLAKE_USER="your-snowflake-user"
MY_SNOWFLAKE_PASSWORD="your-snowflake-password"
SNOWFLAKE_ROLE="your-snowflake-role"
SNOWFLAKE_DATABASE="your-snowflake-database"
SNOWFLAKE_SCHEMA="your-snowflake-schema"
SNOWFLAKE_WAREHOUSE="your-snowflake-warehouse"
```

Replace the placeholders with your actual values.

Navigate to the data folder and run the 01_create_data.py and 02_insert_data.py scripts to create and insert the data into Snowflake:

```bash
cd data
python 01_create_data.py
python 02_insert_data.py
```

Run the FastAPI application:

```bash
uvicorn app:app --reload
```

Open your browser and go to http://localhost:8000/docs to view the API documentation and test the endpoints.

To use the Snowpark functionality, open the sql_worksheet.sql file in Snowflake and run the queries.

## Usage
The system provides the following endpoints:

- /make_review: Generates a high-level summary review of a product based on its reviews.
- /pointwise_recommender: Recommends a product for a user based on their review history.
- /pairwise_recommender: Compares two products and recommends the one that a user is more likely to prefer based on their review history.
- /listwise_recommender: Ranks a list of products based on a user's review history.
- /summarize_product_features: Summarizes the main features of a product.

You can test these endpoints using the API documentation or a tool like Postman.

## Snowpark Functionality
The sql_worksheet.sql file contains SQL queries that demonstrate how to use Snowpark to interact with the data in Snowflake. The queries include creating a network rule and secret to allow the application to access the OpenAI API, creating a service and UDF to test the application, and cleaning up resources.

## Limitations
The system is not working due to misconfigurations in Egress