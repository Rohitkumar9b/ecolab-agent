# from langchain.tools import tool


# # @tool
# # def sql_query_tool(query: str):
# #     """
# #     Execute a SQL query on Databricks and return results.
# #     """
# #     return f"Executed SQL query on Databricks: {query}"


# # @tool
# # def vector_search_tool(query: str):
# #     """
# #     Perform semantic search and return relevant documents.
# #     """
# #     return f"Top documents related to: {query}"

# from langchain.tools import tool
# from langchain_openai import ChatOpenAI

# llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)

# @tool
# def sql_query_tool(query: str):
#     """
#     Convert natural language to SQL and simulate execution.
#     """
#     return f"[SIMULATED DB RESULT] Query executed: {query}"

# @tool
# def vector_search_tool(query: str):
#     """
#     Perform semantic search and return AI-generated answer.
#     """
#     response = llm.invoke(query)
#     return response.content


from langchain.tools import tool
from langchain_openai import ChatOpenAI

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
    Convert natural language into SQL and simulate database response.
    """

    # Step 1: Convert to SQL
    sql_prompt = f"""
    Convert the following natural language query into SQL:

    Query: {query}

    Only return SQL query.
    """

    sql_response = llm.invoke(sql_prompt)
    sql_query = sql_response.content

    # Step 2: Simulate execution (since no DB connected)
    result = f"""
    Generated SQL:
    {sql_query}

    [SIMULATED RESULT]
    - Row 1: Sample Data
    - Row 2: Sample Data
    """

    return result