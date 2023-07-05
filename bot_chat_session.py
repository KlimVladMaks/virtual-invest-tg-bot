# Импорты библиотек
import typing as tp

# Импорты файлов
import text

# Импорты файлов для задания типов
if tp.TYPE_CHECKING:
    from portfolio_database import PortfolioDatabase


class BotChatSession:
    """"
    Класс для реализации сессии бота с одним чатом пользователя.
    (Это позволяет использовать бота в многопользовательском режиме).
    """

    def __init__(self, user_id: int, portfolio_database: 'PortfolioDatabase') -> None:
        """
        Функция для инициализации сессии с пользователем.

        :param user_id: ID пользователя.
        :param portfolio_database: База данных с портфелями пользователя.
        """

        # Сохраняем ID пользователя
        self.user_id = user_id
        
        # Сохраняем базу данных с портфелями пользователей
        self.portfolio_database = portfolio_database

        # Указатель того, какое действие сейчас реализуется
        # По-умолчанию реализуется цикл главного меню
        self.action_list = ["main_menu"]
    
    def processing(self, user_message_text: str) -> list[str]:
        """
        Функция для обработки пользовательского ввода.

        :param user_message_text: Строка, содержащая сообщение пользователя.
        :return: Список, содержащий строки с ответами бота.
        """

        # Главное меню
        if self.get_action(0) == "main_menu":

            # Первый запуск бота
            if user_message_text == "/start":
                
                # Возвращаем приветственное сообщение для пользователя
                return [text.welcome_message]

            # Запуск главного меню
            elif user_message_text == "/main_menu":
                
                # Возвращаем информацию для главного меню
                return [text.start_main_menu]

            # Создание нового портфеля
            elif user_message_text == "/create_new_portfolio":
                
                # Переводим пользователя в цикл создания портфеля
                self.action_list = ["create_new_portfolio"]
                return self.processing(user_message_text)
    
            # Удаление портфеля
            elif user_message_text == "/delete_portfolio":
                
                # Переводим пользователя в цикл удаления портфеля
                self.action_list = ["delete_portfolio"]
                return self.processing(user_message_text)

            # Если не удалось распознать пользовательский ввод
            else:
                
                # Возвращаем сообщение об ошибке
                return [text.main_menu_failed_recognize_input]

        # Создание нового портфеля
        elif self.get_action(0) == "create_new_portfolio":
            
            # Начало создания нового портфеля
            if user_message_text == "/create_new_portfolio":

                # Добавляем действие получения имени нового портфеля
                self.action_list.append("set_new_portfolio_name")
                
                # Возвращаем сообщение с просьбой ввести имя нового портфеля
                return [text.ask_new_portfolio_name]

            # Возвращение в главное меню
            elif user_message_text == "/main_menu":
                
                # Возвращаем пользователя в главное меню
                self.action_list = ["main_menu"]
                bot_outputs = [text.stop_portfolio_creation]
                bot_outputs.append(self.processing("/main_menu"))
                return bot_outputs

            # Задание имени нового портфеля
            elif self.get_action(1) == "set_new_portfolio_name":
                
                # Получаем имя нового портфеля
                new_portfolio_name = user_message_text

                # Добавляем новый портфель в базу данных и получаем результат данной операции
                result = self.portfolio_database.add_new_portfolio(new_portfolio_name, self.user_id)

                # Если добавление портфеля прошло успешно
                if result == 0:

                    # Сообщаем пользователю об успешном создании портфеля и переводим его в главное меню
                    self.action_list = ["main_menu"]
                    bot_outputs = [text.successful_new_portfolio_creation.format(new_portfolio_name=new_portfolio_name)]
                    bot_outputs.append(self.processing("/main_menu"))
                    return bot_outputs

                # Если портфель с таким именем уже есть у пользователя
                elif result == 1:

                    # Сообщаем пользователю о данной ошибке и остаёмся в том же цикле
                    return [text.repeated_portfolio_name_error]

        # Удаление портфеля
        elif self.get_action(0) == "delete_portfolio":
            pass


    def get_action(self, position: int) -> str:
        """
        Функция для получения текущего действия с заданной позицией.

        :param position: Позиция действия в списке действий.
        :return: Строка с действием с заданной позицией или строка "none", если действия с заданной позицией не найдено.
        """
        
        # Возвращаем действие с заданной позицией
        try:
            return self.action_list[position]
        
        # При выходе за пределы диапазона возвращаем строку "none"
        except IndexError:
            return "none"


# Область для отладки
if __name__ == "__main__":
    pass
