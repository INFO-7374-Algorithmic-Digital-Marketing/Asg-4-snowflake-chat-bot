# Snowflake Chat Bot

This is a Streamlit application that uses the OpenAI API to generate SQL queries based on user input. The application is named "Snowflake Chat Bot" and it has a chat interface where the user can input their questions and the chat bot will generate a SQL query based on the question and the table schema.

## Features

* Uses the OpenAI API to generate SQL queries based on user input
* Chat interface for user input and output
* System prompt based approach to provide context about the table and its columns to the LLM
* Uses the `run_query` function to execute SQL queries against a Snowflake database
* Displays the results of the SQL query in a dataframe

## Requirements

* Python 3.7 or higher
* Streamlit
* OpenAI API key
* Snowflake account credentials
* SQLAlchemy
* pandas
* python-dotenv

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/snowflake-chat-bot.git
```

2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory of the project and add the following environment variables:

```bash
OPENAI_API_KEY=your_openai_api_key
SNOWFLAKE_ACCOUNT=your_snowflake_account
SNOWFLAKE_USER=your_snowflake_user
SNOWFLAKE_PASSWORD=your_snowflake_password
SNOWFLAKE_DATABASE=your_snowflake_database
SNOWFLAKE_SCHEMA=your_snowflake_schema
```

4. Create a '.streamlit' directory and a 'secrets.toml' file in it

```bash
PENAI_API_KEY = ""

[connections.snowflake]
user = ""
password = ""
warehouse = ""
role = ""
account = ""
```

5. Run the Streamlit application:

```bash
streamlit run app.py
```


## Usage

1. Open the application in your web browser.
2. Input your question in the chat interface.
3. The chat bot will generate a SQL query based on your question and the table schema.
4. The SQL query will be executed against the Snowflake database.
5. The results of the SQL query will be displayed in a dataframe.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

