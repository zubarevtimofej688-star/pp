from api.gameapi import GameAPI
from repositories.game_repository import GameRepository


class GameService:
    def __init__(self, store: GameAPI, repo: GameRepository):
        self.store, self.repo = store, repo
