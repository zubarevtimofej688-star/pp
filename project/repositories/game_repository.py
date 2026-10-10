from repositories.database import Database


class GameRepository:
    def __init__(self, db: Database):
        self.db = db

    def add_favorite(self, user_id: int, appid: int, name: str):
        with self.db.connect() as conn:
            conn.execute("INSERT OR REPLACE INTO favorites VALUES (?, ?, ?)", (user_id, appid, name))

    def favorites(self, user_id: int):
        with self.db.connect() as conn:
            return conn.execute("SELECT appid, name FROM favorites WHERE user_id=? ORDER BY name", (user_id,)).fetchall()

    def save_rating(self, user_id: int, appid: int, rating: int):
        if not 1 <= rating <= 5:
            raise ValueError("Оценка должна быть от 1 до 5")
        with self.db.connect() as conn:
            conn.execute("INSERT INTO reviews(user_id,appid,rating) VALUES (?,?,?) ON CONFLICT(user_id,appid) DO UPDATE SET rating=excluded.rating", (user_id, appid, rating))

    def save_review(self, user_id: int, appid: int, text: str):
        with self.db.connect() as conn:
            conn.execute("INSERT INTO reviews(user_id,appid,text) VALUES (?,?,?) ON CONFLICT(user_id,appid) DO UPDATE SET text=excluded.text", (user_id, appid, text))
