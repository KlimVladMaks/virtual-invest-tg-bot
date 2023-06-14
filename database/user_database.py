# Импорты
import sqlite3


class UserDatabase:
    """
    Класс для реализации базы данных пользователей бота.
    """
    
    def __init__(self) -> None:
        """
        Функция для инициализации класса.
        """
        
        # Создаём подключение к базе данных
        self.connection = sqlite3.connect("users.db")

        # Создаём для реализации запросов к базе данных
        self.cursor = self.connection.cursor()

        # Если таблицы "users" не существует, то создаём её
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY)""")
        self.connection.commit()
    
    def is_user_in_database(self, user_id: int) -> bool:
        """
        Функция для проверки существования пользователя в базе данных.

        :param user_id: ID пользователя.
        :return: True - если пользователь есть в базе данных, False - если нет.
        """
        
        # Проверяем существование пользователя в базе данных и возвращаем результат
        self.cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
        return bool(self.cursor.fetchone())

    def add_user(self, user_id: int) -> None:
        """
        Функция для добавления пользователя в базу данных.

        :param user_id: ID пользователя.
        """
        
        # Если пользователя ещё нет в базе данных
        if not self.is_user_in_database(user_id):
            
            # Добавляем пользователя в базу данных
            self.cursor.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
            self.connection.commit()


# Область для отладки
if __name__ == "__main__":
    pass
