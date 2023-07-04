# Импорты библиотек
import telebot
import typing as tp

# Импорты файлов
import get_token
import text
from portfolio_database import PortfolioDatabase
from bot_chat_session import BotChatSession

# Получаем токен для бота
bot_token = get_token.TOKEN

# Создаём экземпляр бота
bot = telebot.TeleBot(bot_token)

# Создаём базу данных для хранения информации о портфелях пользователя
portfolio_database = PortfolioDatabase()

# Словарь для хранения сессий пользователей
chat_dict: dict[int, BotChatSession] = {}


@bot.message_handler(content_types=["text"])
def message_handler(message: telebot.types.Message):
    """
    Функция для обработки пользовательского ввода.

    :param message: Сообщение пользователя, содержащее текст ввода.
    """
    
    # Если ID данного чата не содержится в списке текущих сессий, то создаём новую сессию для данного чата
    if message.chat.id not in chat_dict:
        chat_dict[message.chat.id] = BotChatSession(message.chat.id, portfolio_database)

    # Отправляем боту сообщение пользователя и получаем список с ответами на него
    bot_outputs: list[str] = chat_dict[message.chat.id].processing(message.text)

    # Перебираем все ответы бота и отправляем их в чат пользователю
    for bot_output in bot_outputs:
        bot.send_message(message.chat.id, bot_output)


# Запускаем бота
if __name__ == "__main__":
    print("Telegram-бот запущен...")
    bot.infinity_polling()


#* ------------------------------------------------------------------------------------------------

# Данная функция вызывается при текстовом вводе пользователя
@bot.message_handler(content_types=["text"])
def main_menu(message: telebot.types.Message, action: tp.Union[str, None] = None) -> None:
    """
    Главное меню: функция для обработки текстового ввода пользователя.

    :param message: Сообщение пользователя.
    :param action: Действие для главного меню.
    """

    # Начало работы с ботом и базовое главное меню
    if (message.text == "/start") or (message.text == "/main_menu") or (action == "main_menu"):
    
        # Получаем ID пользователя
        user_id: int = message.from_user.id

        # Если текущий пользователь уже имеет хотя бы один портфель
        if portfolio_database.is_user_has_portfolio(user_id):
            
            # Отправляем приветственное сообщение для уже зарегистрированного пользователя
            user_input = bot.send_message(message.chat.id, text.start_main_menu)

            # Обрабатываем ответ пользователя в этой же функции
            bot.register_next_step_handler(user_input, main_menu)

        # Иначе (если у пользователя нет ни одного портфеля)
        else:
            
            # Отправляем приветственное сообщение с предложением создать новый портфель и ждём ответа от пользователя
            user_input = bot.send_message(message.chat.id, text.start_new_user)

            # Отправляем ответ пользователя текущей функции
            bot.register_next_step_handler(user_input, main_menu)

    # Создание нового портфеля
    elif message.text == "/create_new_portfolio":
        
        # Запускаем функцию для создания нового портфеля
        create_new_portfolio(message)

    # Удаление доступного портфеля
    elif message.text == "/delete_portfolio":
        
        # Запускаем функцию для удаления доступного портфеля
        delete_portfolio(message)


def create_new_portfolio(message: telebot.types.Message, action: tp.Union[str, None] = None) -> None:
    """
    Функция для создания нового портфеля.

    :param message: Сообщение пользователя.
    :param action: Действие при создании портфеля.
    """

    # Вернуться в главное меню
    if message.text == "/main_menu":
        
        # Возвращаемся в главное меню
        main_menu(message, "main_menu")
    
    # Начало создания нового портфеля
    elif message.text == "/create_new_portfolio":
        
        # Выводим сообщение с просьбой ввести имя нового портфеля
        user_input = bot.send_message(message.chat.id, text.ask_new_portfolio_name)

        # Отправляем ответ пользователя текущей функции, указывая, что реализуется действие задания имени портфелю
        bot.register_next_step_handler(user_input, create_new_portfolio, "set_new_portfolio_name")

    # Задание имени портфеля
    elif action == "set_new_portfolio_name":
        
        # Получаем имя нового портфеля
        new_portfolio_name = message.text

        # Добавляем новый портфель в базу данных и получаем результат
        result = portfolio_database.add_new_portfolio(new_portfolio_name, message.from_user.id)

        # Если добавление портфеля прошло успешно
        if result == 0:
            
            # Отправляем пользователю сообщение об успешном создании портфеля
            bot.send_message(message.chat.id, 
                             text.successful_new_portfolio_creation.format(new_portfolio_name = new_portfolio_name))

            # Возвращаемся в главное меню
            main_menu(message, "main_menu")
        
        # Если портфель с таким именем уже есть у пользователя
        elif result == 1:
            
            # Отправляем пользователю сообщение о повторяющемся имени портфеля
            user_input = bot.send_message(message.chat.id, text.repeated_portfolio_name_error)

            # Повторяем цикл задания имени портфеля
            bot.register_next_step_handler(user_input, create_new_portfolio, "set_new_portfolio_name")


def delete_portfolio(message: telebot.types.Message, action: tp.Union[str, None] = None) -> None:
    """
    Функция для удаления доступного портфеля.

    :param message: Сообщение пользователя.
    :param action: Действие при удалении портфеля.
    """
    
    # Начало процесса удаления портфеля
    if message.text == "/delete_portfolio":
        pass


