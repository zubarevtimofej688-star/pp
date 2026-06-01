@dataclass
class Game:
    id: int = field(default_factory=next_id)
    name: str
    genre: str
    platform: str
    age_rating: int = field(default=0)
    price: int = field(default=0)
    player_ratings: float = field(default=0.0)
    status: str = field(default="")
    number_of_copies: int = field(default=0)
    id = 0
    def id():
        global id_counted
        id_counted +=1
        return id_counted


game_list[    Game(name="The Witcher 3: Wild Hunt", genre="RPG", platform="PC", age_rating=18, price=1200, player_ratings=4.9, status="Available", number_of_copies=10),
    Game(name="Cyberpunk 2077", genre="RPG", platform="PC", age_rating=18, price=2000, player_ratings=4.2, status="Available", number_of_copies=15),
    Game(name="Warcraft III: Reign of Chaos", genre="RTS", platform="PC", age_rating=16, price=600, player_ratings=4.7, status="Available", number_of_copies=5),
    Game(name="The Elder Scrolls V: Skyrim", genre="RPG", platform="PC", age_rating=16, price=1000, player_ratings=4.8, status="Available", number_of_copies=20),
    Game(name="Red Dead Redemption 2", genre="Action-Adventure", platform="PC", age_rating=18, price=2500, player_ratings=4.9, status="Available", number_of_copies=12),
    Game(name="Grand Theft Auto V", genre="Action-Adventure", platform="PC", age_rating=18, price=1500, player_ratings=4.6, status="Available", number_of_copies=8),
]

    


#1. поиск игр по части названия (подстрока)
def search_games_by_partial_name(game_list: list[Game], search_term: str) -> list[Game]:
    "name" in "game_list"
    Search: game in game_list 
    prefix = search_query[3].lower()
    result = [g for g in games if g.lower().startswith(prefix)]
    if not found:
        reture
        print(f"result")
#2. фильтрация игр





#3. сортировка игр
def sort_game(game):
    is_sorted = False
    offser = 0
    while is_sorted == False:
        is_sorted = True
        for i in range(len(game)-1-offser): 
            if game[i+1].id < game[i].id:
                temp = game[i + 1]
                game[i + 1] = game[i]
                game[i] = temp
                is_sorted = False

        offser += 1
#4. изменить цену всех игр выбранного жанра (например, скидка −20%)






#5. подсчитать среднюю цену всех игр
def game_price(price,game):
    total_sum = sum(game["price"] for game in games)
    if len(games) > 0:
        average_price = total_sum / len(games)
        print(f"Средняя цена игр: {average_price:.2f}")
    else:
        print("Список игр пуст")


#6. найти игру с максимальной оценкой
def game_player_ratings(player_ratings,game):
    if game["player_ratings"] == max_player_ratings:
        print ("game")

#7. пометить игру как «хит», если оценка ≥ 8.5
def game_player_ratings(player_ratings,game):
    if game["player_ratings"] >= 8.5:
        Move (game) in "хит"
        print("эта игра в хите")
#8. удалить все игры, у которых количество копий равно 0
def game_number_of_copies(number_of_copies,game):
    if game["number_of_copies"] == 0:
        del game
        print("игра удалина")