def validate_input(query: str):
    if len(query) == 0:
        raise ValueError("Empty query not allowed")

    if "hack" in query.lower():
        raise ValueError("Unsafe input detected")

    return query


def validate_output(response: str):
    if response is None:
        return "Something went wrong"

    return response