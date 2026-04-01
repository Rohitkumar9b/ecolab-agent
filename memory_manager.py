import os

BASE_PATH = "memory"

def get_user_memory(user_id):
    path = f"{BASE_PATH}/{user_id}/memory.md"
    if not os.path.exists(path):
        return []
    
    with open(path, "r") as f:
        return f.readlines()

def save_memory(user_id, text):
    os.makedirs(f"{BASE_PATH}/{user_id}", exist_ok=True)
    path = f"{BASE_PATH}/{user_id}/memory.md"

    with open(path, "a") as f:
        f.write(text + "\n")