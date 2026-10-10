from dataclasses import dataclass


@dataclass(frozen=True)
class Review:
    user_id: int
    appid: int
    rating: int | None
    text: str | None
