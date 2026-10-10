import html
import logging

import requests

from telebot import types

from models.game import Game
from ua.keyboard import actions, game_button, menu, rating
from ua.states import States
from ua.text import HELP, WELCOME

log = logging.getLogger(__name__)

# Список команд в меню Telegram (то, что видно на экране команд бота).
BOT_COMMANDS = [
    types.BotCommand("start", "Открыть главное меню"),
    types.BotCommand("search", "Найти игру"),
    types.BotCommand("favorites", "Показать избранное"),
    types.BotCommand("help", "Показать справку"),
]


def setup_handlers(bot, service):
    states = States()

    try:
        bot.set_my_commands(BOT_COMMANDS)
    except Exception:
        log.exception("Не удалось обновить список команд бота")

    def show_list(chat_id, games, heading):
        text = heading if games else f"{heading}\nПока ничего нет."
        bot.send_message(chat_id, text, reply_markup=menu())
        for game in games[:50]:
            bot.send_message(chat_id, html.escape(game.name), reply_markup=game_button(game.appid), parse_mode="HTML")

    def ask_search(user_id, chat_id):
        states.set(user_id, "search")
        bot.send_message(chat_id, "Введите название игры:", reply_markup=menu())

    def show_top(user_id, chat_id):
        try:
            show_list(chat_id, service.store.top50(), "🏆 Текущие лидеры продаж:")
        except (requests.RequestException, ValueError, KeyError):
            log.exception("Top request failed")
            bot.send_message(chat_id, "Не удалось загрузить топ. Попробуйте позже.", reply_markup=menu())

    def show_favorites(user_id, chat_id):
        games = [Game(appid, name) for appid, name in service.repo.favorites(user_id)]
        show_list(chat_id, games, "⭐ Избранное:")

    @bot.message_handler(commands=["start"])
    def start(message):
        states.pop(message.from_user.id)
        bot.send_message(message.chat.id, WELCOME, reply_markup=menu())

    @bot.message_handler(commands=["help"])
    def help_command(message):
        states.pop(message.from_user.id)
        bot.send_message(message.chat.id, HELP, reply_markup=menu(), parse_mode="HTML")

    @bot.message_handler(commands=["search"])
    def search_command(message):
        states.pop(message.from_user.id)
        ask_search(message.from_user.id, message.chat.id)

    @bot.message_handler(commands=["favorites", "fav"])
    def favorites_command(message):
        states.pop(message.from_user.id)
        show_favorites(message.from_user.id, message.chat.id)

    @bot.message_handler(commands=["top"])
    def top_command(message):
        # Скрытая команда: кнопка «Топ игр» есть, но в списке команд её нет.
        states.pop(message.from_user.id)
        show_top(message.from_user.id, message.chat.id)

    @bot.message_handler(content_types=["text"])
    def text_handler(message):
        user_id, chat_id, value = message.from_user.id, message.chat.id, message.text.strip()
        state = states.pop(user_id)
        if state and state[0] == "search":
            if len(value) < 2:
                bot.send_message(chat_id, "Введите минимум 2 символа.", reply_markup=menu())
                states.set(user_id, "search")
                return
            try:
                show_list(chat_id, service.store.search(value), "🔎 Результаты поиска:")
            except (requests.RequestException, ValueError, KeyError):
                log.exception("Search failed")
                bot.send_message(chat_id, "Не удалось найти игры. Попробуйте позже.", reply_markup=menu())
        elif state and state[0] == "review":
            if not 3 <= len(value) <= 1000:
                states.set(user_id, "review", state[1])
                bot.send_message(chat_id, "Напишите отзыв от 3 до 1000 символов.", reply_markup=menu())
                return
            service.repo.save_review(user_id, state[1], value)
            bot.send_message(chat_id, "Отзыв сохранён. Спасибо!", reply_markup=menu())
        elif value.startswith("/"):
            bot.send_message(chat_id,
                             "Неизвестная команда. Доступны: /start /search /favorites /help",
                             reply_markup=menu())
        else:
            bot.send_message(chat_id, "Выберите действие кнопками под сообщением или напишите /start.",
                             reply_markup=menu())

    def navigate(call, target):
        user_id, chat_id = call.from_user.id, call.message.chat.id
        states.pop(user_id)
        if target == "search":
            ask_search(user_id, chat_id)
        elif target == "top":
            show_top(user_id, chat_id)
        elif target == "fav":
            show_favorites(user_id, chat_id)
        else:
            bot.answer_callback_query(call.id, "Неизвестная кнопка")
            return False
        return True

    @bot.callback_query_handler(func=lambda call: bool(call.data))
    def callback(call):
        try:
            action, *args = call.data.split(":")
            if action == "nav":
                if navigate(call, args[0]):
                    bot.answer_callback_query(call.id)
                return
            appid = int(args[0])
            if action == "game":
                game = service.store.details(appid)
                if game is None:
                    bot.answer_callback_query(call.id, "Игра не найдена")
                    return
                # Обрезаем до экранирования: нарезанная entities строка ломает разбор HTML.
                description = html.escape((game.description or "Описание отсутствует")[:1800])
                bot.send_message(call.message.chat.id,
                                 f"🎮 <b>{html.escape(game.name)}</b>\n{description}\n"
                                 f"https://store.steampowered.com/app/{appid}/",
                                 reply_markup=actions(appid), parse_mode="HTML")
            elif action == "fav":
                game = service.store.details(appid)
                if game is None:
                    bot.answer_callback_query(call.id, "Игра не найдена")
                    return
                service.repo.add_favorite(call.from_user.id, appid, game.name)
                bot.send_message(call.message.chat.id, "Добавлено в избранное ⭐", reply_markup=menu())
            elif action == "review":
                states.set(call.from_user.id, "review", appid)
                bot.send_message(call.message.chat.id, "Напишите ваш отзыв об игре (3–1000 символов):",
                                 reply_markup=menu())
            elif action == "rate":
                bot.send_message(call.message.chat.id, "Оцените игру от 1 до 5:", reply_markup=rating(appid))
            elif action == "score":
                score = int(args[1])
                service.repo.save_rating(call.from_user.id, appid, score)
                bot.send_message(call.message.chat.id, f"Оценка {score}/5 сохранена 🌟", reply_markup=menu())
            else:
                bot.answer_callback_query(call.id, "Неизвестная кнопка")
                return
            bot.answer_callback_query(call.id)
        except (ValueError, IndexError, requests.RequestException, KeyError):
            log.exception("Callback failed")
            bot.answer_callback_query(call.id, "Не удалось выполнить действие. Попробуйте позже.")
