from langchain_openai import ChatOpenAI
from tools import sql_query_tool, vector_search_tool
import os
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3,
    api_key=os.getenv("OPENAI_API_KEY")
)


def databricks_agent():
    def run(query: str):
        # Directly call tool (you can later add reasoning here)
        return sql_query_tool.invoke(query)

    return run


def vector_agent():
    def run(query: str):
        return vector_search_tool.invoke(query)

    return run