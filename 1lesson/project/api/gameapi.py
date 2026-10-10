import requests
from models.game import Game


class GameAPI:
    BASE = "https://store.steampowered.com/api"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "SteamGamesTelegramBot/1.0"})

    def _get(self, path, **params):
        response = self.session.get(f"{self.BASE}/{path}", params=params, timeout=12)
        response.raise_for_status()
        return response.json()

    def search(self, query: str) -> list[Game]:
        # Steam's storefront search endpoint is public but undocumented.
        data = self._get("storesearch/", term=query, l="russian", cc="ru")
        return [Game(int(item["id"]), item["name"]) for item in data.get("items", [])[:10]]

    def details(self, appid: int) -> Game | None:
        data = self._get("appdetails/", appids=appid, l="russian", cc="ru")
        entry = data.get(str(appid), {})
        if not entry.get("success"):
            return None
        item = entry["data"]
        return Game(appid, item.get("name", str(appid)), item.get("short_description", ""))

    def top50(self) -> list[Game]:
        # The public featured categories endpoint exposes current top sellers.
        data = self._get("featuredcategories/", l="russian", cc="ru")
        items = data.get("top_sellers", {}).get("items", [])
        return [Game(int(item["id"]), item.get("name", str(item["id"]))) for item in items[:50]]
