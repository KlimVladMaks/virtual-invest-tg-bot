# Импорты
import sys
sys.path.append("./token")
import telebot
import get_token

# Получаем токен для бота
bot_token = get_token.TOKEN

# Создаём экземпляр бота
bot = telebot.TeleBot(bot_token)

# Обработчик команды "/start"
@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message) -> None:
    """
    Функция для начала работы бота с пользователем.

    :param message: Сообщение пользователя.
    """
    
    # Получаем ID пользователя
    user_id: int = message.from_user.id


# Запускаем бота
if __name__ == "__main__":
    bot.infinity_polling()
