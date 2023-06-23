"""
Запуск программы: 'python -B .\main.py'
"""

# Импорты
import telebot
import typing as tp
import get_token
import text
from user_database import PortfolioDatabase

# Получаем токен для бота
bot_token = get_token.TOKEN

# Создаём экземпляр бота
bot = telebot.TeleBot(bot_token)

# Создаём базу данных для хранения информации о портфелях пользователя
portfolio_database = PortfolioDatabase()

# Данная функция вызывается при текстовом вводе пользователя
@bot.message_handler(content_types=["text"])
def text_input_processing(message: telebot.types.Message) -> None:
    """
    Функция для обработки текстового ввода пользователя.

    :param message: Сообщение пользователя.
    """

    # Если введена команда "/start" (начало работы с ботом)
    if message.text == "/start":
    
        # Получаем ID пользователя
        user_id: int = message.from_user.id

        # Если текущий пользователь уже имеет хотя бы один портфель
        if portfolio_database.is_user_has_portfolio(user_id):
            pass

        # Иначе (если у пользователя нет ни одного портфеля)
        else:
            
            # Отправляем приветственное сообщение с предложением создать новый портфель и ждём ответа от пользователя
            user_input = bot.send_message(message.chat.id, text.start_new_user)

            # Отправляем ответ пользователя текущей функции
            bot.register_next_step_handler(user_input, text_input_processing)

    # Если введена команда "/create_new_portfolio" (создание нового портфеля)
    elif message.text == "/create_new_portfolio":
        
        # Запускаем функцию для создания нового портфеля
        create_new_portfolio(message)


def create_new_portfolio(message: telebot.types.Message, action: tp.Union[str, None] = None) -> None:
    """
    Функция для создания нового портфеля.

    :param message: Сообщение пользователя.
    :param action: Действие при создании портфеля.
    """
    
    # Если введена команда "/create_new_portfolio" (начало создание нового портфеля)
    if message.text == "/create_new_portfolio":
        
        # Выводим сообщение с просьбой ввести имя нового портфеля
        user_input = bot.send_message(message.chat.id, text.ask_new_portfolio_name)

        # Отправляем ответ пользователя текущей функции, указывая, что реализуется действие задания имени портфелю
        bot.register_next_step_handler(user_input, create_new_portfolio, "set_new_portfolio_name")

    # Если реализуется действие задания имени портфелю
    elif action == "set_new_portfolio_name":
        
        # Получаем имя нового портфеля
        new_portfolio_name = message.text

        # Добавляем новый портфель в базу данных и получаем результат
        result = portfolio_database.add_new_portfolio(new_portfolio_name, message.from_user.id)


# Запускаем бота
if __name__ == "__main__":
    print("Telegram-бот запущен...")
    bot.infinity_polling()
