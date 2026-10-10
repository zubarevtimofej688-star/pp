import telebot

from api.gameapi import GameAPI
from repositories.database import Database
from repositories.game_repository import GameRepository
from service.services import GameService
from ua.screen_1 import setup_handlers

TOKEN = "8677993611:AAGbl47ereWmkAj3NrexMbaKkFIHz0IrohA"
DATABASE_PATH = "C:/pp/project/data/games.sqlite3"


def main():
    bot = telebot.TeleBot(TOKEN)
    service = GameService(GameAPI(), GameRepository(Database(DATABASE_PATH)))
    setup_handlers(bot, service)

    print("Бот запущен. Остановка — Ctrl+C.")
    try:
        # Пропускаем старые апдейты. Сбой здесь (409, нет сети) не должен ронять бота:
        # внутри telebot skip_pending=True выполняется вне try/except.
        bot.get_updates(offset=-1)
    except Exception as exc:
        print("Не удалось сбросить старые сообщения:", exc)

    try:
        bot.infinity_polling(timeout=30)
    except KeyboardInterrupt:
        print("\nБот остановлен.")


if __name__ == "__main__":
    main()
