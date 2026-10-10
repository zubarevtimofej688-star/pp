from telebot import types


def menu():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(
        types.InlineKeyboardButton("🔎 Поиск", callback_data="nav:search"),
        types.InlineKeyboardButton("🏆 Топ игр", callback_data="nav:top"),
    )
    keyboard.row(types.InlineKeyboardButton("⭐ Избранное", callback_data="nav:fav"))
    return keyboard


def game_button(appid: int):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Подробнее", callback_data=f"game:{appid}"))
    return keyboard


def actions(appid: int):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("⭐ В избранное", callback_data=f"fav:{appid}"))
    keyboard.add(types.InlineKeyboardButton("✍️ Отзыв", callback_data=f"review:{appid}"),
                 types.InlineKeyboardButton("🌟 Оценить", callback_data=f"rate:{appid}"))
    return keyboard


def rating(appid: int):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(*(types.InlineKeyboardButton(str(i), callback_data=f"score:{appid}:{i}") for i in range(1, 6)))
    return keyboard
