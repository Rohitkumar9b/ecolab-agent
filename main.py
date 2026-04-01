
from graph import build_graph
from guardrails import validate_input, validate_output
from memory_manager import get_user_memory

graph = build_graph()

def run(user_id, query):
    query = validate_input(query)

    state = {
        "user_id": user_id,
        "query": query,
        "response": "",
        "memory": get_user_memory(user_id),
        "next_agent": ""
    }

    result = graph.invoke(state)

    response = validate_output(result["response"])
    return response

def main():
    print("Hello from ecolab!")




if __name__ == "__main__":
    user_id = "user_001"

    while True:
        query = input("User: ")
        print("AI:", run(user_id, query))