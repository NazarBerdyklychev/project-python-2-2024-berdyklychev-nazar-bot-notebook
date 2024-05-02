    Описание проекта:
В рамках данного проекта я поставил цель сделать телеграм бота, который будет выполнять функцию заметок.


    Реализуемый функционал:
-Регистрация и удаление пользователя
-Возможность создания, редактирования, удаления, просмотра заметок
-Наличие базовых полей для объектов


    Архитектура:

-add_user(user_name)
-del_user(user_name)

 User:
user_name
notes
-create_note(user_name, note_name)
-edit_note(user_name, note_name)
-del_note(user_name, note_name)
-read_note(user_name, note_name)

 Note:
note_name
data


    Технологии:
Python3, библиотеки:
-telebot (pyTelegramBotAPI)


    Программы используемые при реализации:
Pycharm
Telegram
