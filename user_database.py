# Импорты
import sqlite3
import hashlib
import secrets


class PortfolioDatabase:
    """
    Класс для реализации базы данных виртуальных инвестиционных портфелей.
    """
    
    def __init__(self) -> None:
        """
        Функция для инициализации класса.
        """
        
        # Создаём подключение к базе данных
        # (Указываем, что данное подключение может работать из разных потоков)
        self.connection = sqlite3.connect("portfolios.db", check_same_thread=False)

        # Создаём для реализации запросов к базе данных
        self.cursor = self.connection.cursor()

        # Создаём таблицу с общей информацией о портфелях (ID портфеля, имя портфеля, ID владельца)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS portfolio_info (
            portfolio_id TEXT PRIMARY KEY,
            portfolio_name TEXT,
            user_id INTEGER
        )
        """)
        self.connection.commit()
    
    def is_portfolio_id_in_database(self, portfolio_id: str) -> bool:
        """
        Функция для проверки, существует ли уже портфель с заданным ID в базе данных.

        :param portfolio_id: ID портфеля.
        :return: True - если портфель с заданным ID уже существует в базе данных, False - если нет.
        """
        
        # Проверяем, существует ли уже заданный портфель в базе данных и возвращаем результат
        self.cursor.execute("SELECT EXISTS(SELECT 1 FROM portfolio_info WHERE portfolio_id = ? LIMIT 1)", 
                            (portfolio_id,))
        return bool(self.cursor.fetchone()[0])

    def is_user_has_portfolio_name(self, portfolio_name: str, user_id: int) -> bool:
        """
        Функция для проверки, имеет ли уже пользователь портфель с заданным именем.

        :param portfolio_name: Имя портфеля.
        :param user_id: ID пользователя.
        :return: True - если портфель с заданным именем уже имеется у пользователя, False - если нет.
        """

        # Проверяем, имеет ли пользователь уже портфель с заданным именем и возвращаем результат
        self.cursor.execute("""
        SELECT EXISTS(SELECT 1 FROM portfolio_info WHERE portfolio_name = ? AND user_id = ? LIMIT 1)
        """, (portfolio_name, user_id))
        return bool(self.cursor.fetchone()[0])

    def is_user_has_portfolio(self, user_id: int) -> bool:
        """
        Функция для проверки, владеет ли пользователь хотя бы одним портфелем.

        :param user_id: ID пользователя.
        :return: True - если пользователь владеет хотя бы одним портфелем, False - если нет.
        """
        
        # Проверяем, владеет ли пользователь хотя бы одним портфелем и возвращаем результат
        self.cursor.execute("SELECT EXISTS(SELECT 1 FROM portfolio_info WHERE user_id = ? LIMIT 1)", (user_id,))
        return bool(self.cursor.fetchone()[0])

    def get_portfolio_id(self, portfolio_name: str, user_id: int) -> str:
        """
        Функция для генерации уникального ID портфеля по его имени и ID его владельца.

        :param portfolio_name: Имя портфеля.
        :param user_id: ID владельца портфеля.
        """

        # Генерируем соль для обеспечения уникальности хеша
        salt = secrets.token_hex(10)
        
        # Создаём базовую строку для генерации ID портфеля
        id_str = f"{portfolio_name}_{user_id}_{salt}"

        # Генерируем ID портфеля, используя базовую строку
        hash_object = hashlib.sha256(id_str.encode())
        id_hash = hash_object.hexdigest()

        # Возвращаем первые 10 символов ID-хеша портфеля
        return id_hash[:10]

    def add_new_portfolio(self, new_portfolio_name: str, user_id: int) -> int:
        """
        Функция для добавления нового портфеля в базу данных.

        :param new_portfolio_name: Название нового портфеля.
        :param user_id: ID пользователя владельца портфеля.
        :return: Код результата действия: 0 - если портфель успешно добавлен, 1 - если портфель с таким именем уже 
        существует у пользователя.
        """

        # Если у пользователя уже есть портфель с таким именем, то возвращаем 1 (портфель с таким именем уже существует)
        if self.is_user_has_portfolio_name(new_portfolio_name, user_id):
            return 1

        # Генерируем ID для нового портфеля
        new_portfolio_id = self.get_portfolio_id(new_portfolio_name, user_id)

        # Добиваемся того, что ID нового портфеля ещё не было в базе данных
        while self.is_portfolio_id_in_database(new_portfolio_id):
            new_portfolio_id = self.get_portfolio_id(new_portfolio_name, user_id)
        
        # Добавляем новый портфель в базу данных
        self.cursor.execute("INSERT INTO portfolio_info (portfolio_id, portfolio_name, user_id) VALUES (?, ?, ?)", 
                            (new_portfolio_id, new_portfolio_name, user_id))
        self.connection.commit()

        # Возвращаем 0 (добавление прошло успешно)
        return 0


# Область для отладки
if __name__ == "__main__":
    pass
