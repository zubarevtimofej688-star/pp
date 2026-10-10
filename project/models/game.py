from dataclasses import dataclass


@dataclass(frozen=True)
class Game:
    appid: int
    name: str
    description: str = ""
    playtime_minutes: int = 0
