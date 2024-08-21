import hashlib
import time


def get_aceess_token_for_settings(user_id: int):
    return hashlib.sha256(f"{user_id}{time.time()}".encode()).hexdigest()
