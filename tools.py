#tools.py

from langchain.tools import tool
from langchain_openai import ChatOpenAI
from databricks import sql

import os
from dotenv import load_dotenv

load_dotenv()

# Initialize LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
    api_key=os.getenv("OPENAI_API_KEY")
)


@tool
def vector_search_tool(query: str):
    """
    Answer general user questions using AI (acts like a chatbot / knowledge assistant).
    """
    prompt = f"""
    You are an intelligent assistant. Answer the user's question clearly and concisely.

    Question: {query}
    """

    response = llm.invoke(prompt)
    return response.content

@tool
def sql_query_tool(query: str):
    """
    Convert natural language to SQL and execute on Databricks.
    """

    # Step 1: Convert NL → SQL
    sql_prompt = f"""
        You are a SQL expert.

        Database: demo_db
        Table: demo_db.users(id, name, age)

        Convert the user query into SQL.

        Rules:
        - ALWAYS use full table name: demo_db.users
        - Only return SQL
        - No explanation

        User Query: {query}

        SQL:
        """

    sql_response = llm.invoke(sql_prompt)
    sql_query = sql_response.content.strip().replace("```sql", "").replace("```", "")

    # Step 2: Execute on Databricks
    try:
        with sql.connect(
            server_hostname=os.getenv("DATABRICKS_HOST").replace("https://", "").replace("/", ""),
            http_path=os.getenv("DATABRICKS_HTTP_PATH"),
            access_token=os.getenv("DATABRICKS_TOKEN"),
        ) as connection:

            with connection.cursor() as cursor:
                cursor.execute(sql_query)
                result = cursor.fetchall()

        return f"""
        Generated SQL:
        {sql_query}

        Result:
        {result}
        """

    except Exception as e:
        return f"Error executing query: {str(e)}"

