# Conversation state stays in memory; SQLite holds permanent data.
from threading import Lock


class States:
    def __init__(self):
        self._values = {}
        self._lock = Lock()

    def set(self, user_id: int, action: str, appid: int | None = None):
        with self._lock:
            self._values[user_id] = (action, appid)

    def pop(self, user_id: int):
        with self._lock:
            return self._values.pop(user_id, None)
